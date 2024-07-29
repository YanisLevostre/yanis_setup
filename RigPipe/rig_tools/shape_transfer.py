import maya.cmds as cmds
import maya.api.OpenMaya as om

source_mesh = 'source1'
target_mesh = 'target'
shape_mesh = 'shape'

def shape_transfer(source_mesh,target_mesh,shape_mesh):
    # get ref vertex
    vertex_count = cmds.polyEvaluate(source_mesh, vertex=True)
    vertex_pos = {}
    ref_vertex_dict = {}
    for shape_vtx_id in range(vertex_count):
        distance_dict = {}
        shape_vtx_pos = cmds.xform('{}.vtx[{}]'.format(shape_mesh, shape_vtx_id), q=True, ws=True, t=True)
        temp_source_vtx_pos = cmds.xform('{}.vtx[{}]'.format(source_mesh, shape_vtx_id), q=True, ws=True, t=True)
        if shape_vtx_pos != temp_source_vtx_pos:
            for source_vtx_id in range(vertex_count):
                source_vtx_pos = cmds.xform('{}.vtx[{}]'.format(source_mesh, source_vtx_id), q=True, ws=True, t=True)
                vector = om.MVector(source_vtx_pos[0] - shape_vtx_pos[0],
                                    source_vtx_pos[1] - shape_vtx_pos[1],
                                    source_vtx_pos[2] - shape_vtx_pos[2])

                distance = vector.length()
                distance_dict[distance] = source_vtx_id

            sorted_distance = sorted(distance_dict)
            if shape_vtx_id != distance_dict[sorted_distance[0]]:
                ref_vertex_dict[shape_vtx_id] = distance_dict[sorted_distance[0]]
            else:
                ref_vertex_dict[shape_vtx_id] = distance_dict[sorted_distance[1]]

            # get source matrix direction

            source_vtx_pos = cmds.xform('{}.vtx[{}]'.format(source_mesh, shape_vtx_id), q=True, ws=True, t=True)
            source_ref_vtx_pos = cmds.xform('{}.vtx[{}]'.format(source_mesh, ref_vertex_dict[shape_vtx_id]), q=True,
                                            ws=True, t=True)

            vector_primary = om.MVector(source_ref_vtx_pos[0] - source_vtx_pos[0],
                                        source_ref_vtx_pos[1] - source_vtx_pos[1],
                                        source_ref_vtx_pos[2] - source_vtx_pos[2])
            source_size = vector_primary.length()
            vector_primary = vector_primary.normalize()
            vector_up = om.MVector(0, 1, 1)
            vector_secondary = vector_primary.normalize() ^ vector_up.normalize()
            vector_tertiary = vector_primary.normalize() ^ vector_secondary.normalize()

            source_matrix = om.MMatrix(((vector_primary.x, vector_primary.y, vector_primary.z, 0),
                                        (vector_secondary.x, vector_secondary.y, vector_secondary.z, 0),
                                        (vector_tertiary.x, vector_tertiary.y, vector_tertiary.z, 0),
                                        (source_vtx_pos[0], source_vtx_pos[1], source_vtx_pos[2], 1)
                                       ))
            # get target matrix direction

            target_vtx_pos = cmds.xform('{}.vtx[{}]'.format(target_mesh, shape_vtx_id), q=True, ws=True, t=True)
            target_ref_vtx_pos = cmds.xform('{}.vtx[{}]'.format(target_mesh, ref_vertex_dict[shape_vtx_id]), q=True,
                                            ws=True, t=True)

            vector_primary = om.MVector(target_ref_vtx_pos[0] - target_vtx_pos[0],
                                        target_ref_vtx_pos[1] - target_vtx_pos[1],
                                        target_ref_vtx_pos[2] - target_vtx_pos[2])
            target_size = vector_primary.length()
            vector_primary = vector_primary.normalize()

            vector_up = om.MVector(0, 1, 1)
            vector_secondary = vector_primary.normalize() ^ vector_up.normalize()
            vector_tertiary = vector_primary.normalize() ^ vector_secondary.normalize()

            target_matrix = om.MMatrix(((vector_primary.x, vector_primary.y, vector_primary.z, 0),
                                        (vector_secondary.x, vector_secondary.y, vector_secondary.z, 0),
                                        (vector_tertiary.x, vector_tertiary.y, vector_tertiary.z, 0),
                                        (target_vtx_pos[0], target_vtx_pos[1], target_vtx_pos[2], 1)
                                        ))


            # get new shape point
            scale = target_size / source_size
            shape_point_matrix = om.MMatrix(((1,0,0,0),(0,1,0,0),(0,0,1,0),(shape_vtx_pos[0],shape_vtx_pos[1],shape_vtx_pos[2],1)))
            scale_matrix = om.MMatrix(((scale,0,0,0),(0,scale,0,0),(0,0,scale,0),(0,0,0,1)))
            inverted_source_matrix = source_matrix.inverse()
            shape_deplacement = shape_point_matrix * inverted_source_matrix
            scaled_shape = shape_deplacement* scale_matrix



            new_point = scaled_shape * target_matrix
            vertex_pos[shape_vtx_id] = (new_point.getElement(3,0),new_point.getElement(3,1),new_point.getElement(3,2))

    new_shape = cmds.duplicate(target_mesh, n = target_mesh+'_shapeTransfer')[0]

    for vtx in vertex_pos:
        cmds.xform('{}.vtx[{}]'.format(new_shape,vtx),ws = True, t = vertex_pos[vtx])


for shape in cmds.ls(sl = True):
    shape_transfer('head_ref_topo','head_ref_topo2',shape)