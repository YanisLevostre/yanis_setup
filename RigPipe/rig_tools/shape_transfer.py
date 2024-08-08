import maya.cmds as cmds
import maya.api.OpenMaya as om
import json

folder = 'C:/Users/Yanis/PycharmProjects/yanis_setup/datas/'
base_name = 'cartoon'
with open(folder+base_name+'.json') as json_data:
    data = json.load(json_data)
    json_data.close()


vertex_exception = [60,111,57,56,58,115,59,253,203,201,202,249,52,112,51]

lower_mouth = [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 53, 54, 55, 56, 58, 59, 71, 72, 73, 83, 84,
               85, 93, 94, 95, 115, 116, 117, 118, 119, 120, 121, 138, 139, 140, 141, 186, 187, 188, 189, 190, 191, 192,
               193, 194, 195, 196, 197, 199, 200, 201, 203, 213, 214, 224, 225, 233, 234, 235, 253, 254, 255, 256, 257,
               258, 259, 274, 275, 276]

def shape_transfer(target_topo_mesh,target_mesh,target_side_mesh,target_mouth_mesh,smooth):
    shapesList = data['shapeList']
    vertex_count = data['vertexCount']
    target_vertex_count = cmds.polyEvaluate(target_mesh, v=True)
    target_vertex_bind = {}
    side_skinCluster = mel.eval('findRelatedSkinCluster '+target_side_mesh)
    mouth_skinCluster = mel.eval('findRelatedSkinCluster ' + target_mouth_mesh)

    for target_mesh_vtx in range(target_vertex_count):
        target_mesh_vtx_pos = cmds.xform('{}.vtx[{}]'.format(target_mesh, target_mesh_vtx), ws=True, t=True, q=True)
        distance_list = {}
        for target_topo_mesh_vtx in range(vertex_count):
            target_topo_mesh_vtx_pos = cmds.xform('{}.vtx[{}]'.format(target_topo_mesh, target_topo_mesh_vtx), ws=True,
                                                  t=True, q=True)
            vector = om.MVector(target_topo_mesh_vtx_pos[0] - target_mesh_vtx_pos[0],
                                target_topo_mesh_vtx_pos[1] - target_mesh_vtx_pos[1],
                                target_topo_mesh_vtx_pos[2] - target_mesh_vtx_pos[2])
            distance_list [vector.length()] = target_topo_mesh_vtx

        sorted_distance = sorted(distance_list)
        inf_short_list = sorted_distance[:smooth]
        target_vertex_bind[target_mesh_vtx] = {}

        for influence in inf_short_list:
            target_vertex_bind[target_mesh_vtx][distance_list[influence]] = inf_short_list[-1] - influence

    for shape in shapesList:
        # get ref vertex

        vertex_pos = {}
        ref_vertex_dict = {}
        vertex_scale_list = []
        source_matrix_list = {}
        target_matrix_list = {}
        deformed_shape = {}

        # get target_mesh binding
        for shape_vtx_id in range(vertex_count):
            distance_dict = {}
            shape_vtx_pos = data[shape][str(shape_vtx_id)]
            temp_source_vtx_pos = data['baseMesh'][str(shape_vtx_id)]
            if shape_vtx_pos != temp_source_vtx_pos:
                for source_vtx_id in range(vertex_count):
                    source_vtx_pos = data['baseMesh'][str(source_vtx_id)]
                    vector = om.MVector(source_vtx_pos[0] - shape_vtx_pos[0],
                                        source_vtx_pos[1] - shape_vtx_pos[1],
                                        source_vtx_pos[2] - shape_vtx_pos[2])

                    distance = vector.length()
                    distance_dict[distance] = source_vtx_id

                if shape_vtx_id in vertex_exception:
                    for id in vertex_exception:
                        if id in distance_dict:
                            del distance_dict[id]

                sorted_distance = sorted(distance_dict)
                if shape_vtx_id != distance_dict[sorted_distance[0]]:
                    ref_vertex_dict[shape_vtx_id] = distance_dict[sorted_distance[0]]
                else:
                    ref_vertex_dict[shape_vtx_id] = distance_dict[sorted_distance[1]]
                # get source matrix direction

                source_vtx_pos = data['baseMesh'][str(shape_vtx_id)]
                source_ref_vtx_pos = data['baseMesh'][str(ref_vertex_dict[shape_vtx_id])]

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

                target_vtx_pos = cmds.xform('{}.vtx[{}]'.format(target_topo_mesh, shape_vtx_id), q=True, ws=True, t=True)
                target_ref_vtx_pos = cmds.xform('{}.vtx[{}]'.format(target_topo_mesh, ref_vertex_dict[shape_vtx_id]), q=True,
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
                source_matrix_list[shape_vtx_id] = source_matrix
                target_matrix_list[shape_vtx_id] = target_matrix

                # get new shape point
                scale = target_size / source_size
                vertex_scale_list.append(scale)

        for shape_vtx_id in range(vertex_count):
            if shape_vtx_id in source_matrix_list:
                shape_vtx_pos = data[shape][str(shape_vtx_id)]
                source_matrix = source_matrix_list[shape_vtx_id]
                target_matrix = target_matrix_list[shape_vtx_id]
                scale = sum(vertex_scale_list)/len(vertex_scale_list)
                scale = 1
                shape_point_matrix = om.MMatrix(((1,0,0,0),(0,1,0,0),(0,0,1,0),(shape_vtx_pos[0],shape_vtx_pos[1],shape_vtx_pos[2],1)))
                scale_matrix = om.MMatrix(((scale,0,0,0),(0,scale,0,0),(0,0,scale,0),(0,0,0,1)))
                inverted_source_matrix = source_matrix.inverse()
                shape_deplacement = shape_point_matrix * inverted_source_matrix
                scaled_shape = shape_deplacement* scale_matrix
                new_point = scaled_shape * target_matrix
                vertex_pos[shape_vtx_id] = (new_point.getElement(3,0),new_point.getElement(3,1),new_point.getElement(3,2))


        L_shape = None
        R_shape = None
        C_shape = None
        shapes_to_build = []
        if shape.split('_')[0] == 'side':
            name = shape.replace('side_','L_')
            L_shape = cmds.duplicate(target_mesh, n =name + '_transfered')[0]
            shapes_to_build.append(L_shape)
            name = shape.replace('side_', 'R_')
            R_shape = cmds.duplicate(target_mesh, n=name + '_transfered')[0]
            shapes_to_build.append(R_shape)
        else:
            C_shape = cmds.duplicate(target_mesh, n=shape + '_transfered')[0]
            shapes_to_build.append(C_shape)

        for vtx in range(target_vertex_count):
            target_mesh_vtx_pos = cmds.xform('{}.vtx[{}]'.format(target_mesh, vtx), ws=True, t=True, q=True)

            for new_shape in shapes_to_build:
                inf_dict = {}
                inf_list = []
                inf_mouth_dict = {}
                x = target_mesh_vtx_pos[0]
                y = target_mesh_vtx_pos[1]
                z = target_mesh_vtx_pos[2]
                if new_shape.split('_')[0] == 'L':
                    inf_side = cmds.skinPercent(side_skinCluster,'{}.vtx[{}]'.format(target_side_mesh, vtx),query=True, value=True)[1]
                elif new_shape.split('_')[0] == 'R':
                    inf_side = cmds.skinPercent(side_skinCluster, '{}.vtx[{}]'.format(target_side_mesh, vtx), query=True,
                                           value=True)[0]

                else:
                    inf_side = 1

                for topo_vtx in target_vertex_bind[vtx]:
                    if topo_vtx in vertex_pos:
                        if topo_vtx in lower_mouth:
                            inf_mouth = cmds.skinPercent(mouth_skinCluster,'{}.vtx[{}]'.format(target_mouth_mesh, vtx),query=True, value=True)[1]
                        else:
                            inf_mouth = cmds.skinPercent(mouth_skinCluster, '{}.vtx[{}]'.format(target_mouth_mesh, vtx), query=True,
                                             value=True)[0]
                        if inf_side * inf_mouth != 0:
                            inf_mouth_dict[topo_vtx] = inf_mouth
                            inf_dict[topo_vtx] = target_vertex_bind[vtx][topo_vtx]
                            inf_list.append(target_vertex_bind[vtx][topo_vtx])

                if inf_dict != {}:
                    if len(inf_list) != 1:
                        sum_inf = sum(inf_list)
                        for topo_vtx in inf_dict:
                            inf_transfer = inf_dict[topo_vtx] / sum_inf
                            inf_mouth = inf_mouth_dict[topo_vtx]
                            base = cmds.xform('{}.vtx[{}]'.format(target_topo_mesh, topo_vtx), ws=True, t=True, q=True)
                            target = vertex_pos[topo_vtx]
                            x += (target[0] - base[0]) * inf_transfer * inf_side * inf_mouth
                            y += (target[1] - base[1]) * inf_transfer * inf_side * inf_mouth
                            z += (target[2] - base[2]) * inf_transfer * inf_side * inf_mouth
                    else:
                        for topo_vtx in inf_dict:
                            inf_transfer = 1
                            inf_mouth = inf_mouth_dict[topo_vtx]
                            base = cmds.xform('{}.vtx[{}]'.format(target_topo_mesh, topo_vtx), ws=True, t=True, q=True)
                            target = vertex_pos[topo_vtx]
                            x += (target[0] - base[0]) * inf_transfer * inf_side * inf_mouth
                            y += (target[1] - base[1]) * inf_transfer * inf_side * inf_mouth
                            z += (target[2] - base[2]) * inf_transfer* inf_side * inf_mouth


                #deformed_shape[vtx] = vertex_pos[vtx]
                cmds.xform('{}.vtx[{}]'.format(new_shape,vtx),ws = True, t = (x,y,z))



shape_transfer('head_ref_topo3','_kevin','kevin_sides','kevin_mouth',6)