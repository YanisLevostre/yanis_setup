import maya.cmds as cmds
import maya.api.OpenMaya as om
import json

def controls_from_shapes(shape_grp,base_mesh,scale_control):
    vertex_count = cmds.polyEvaluate(base_mesh,v = True)
    shape_list = cmds.listRelatives(shape_grp, children = True)
    bs = cmds.blendShape(base_mesh, n = 'head_bs')
    for index in range(len(shape_list)):
        cmds.blendShape(bs,edit = True ,t = [base_mesh, index, shape_list[index], 1])
        vertex_pos_list = {}
        for vtx in range(vertex_count):

            base_vtx_pos = cmds.xform('{}.vtx[{}]'.format(base_mesh,vtx),q = True, ws = True, t = True)
            shape_vtx_pos = cmds.xform('{}.vtx[{}]'.format(shape_list[index], vtx), q=True, ws=True, t=True)
            if base_vtx_pos != shape_vtx_pos:
                vector = om.MVector(shape_vtx_pos[0] - base_vtx_pos[0],
                                    shape_vtx_pos[1] - base_vtx_pos[1],
                                    shape_vtx_pos[2] - base_vtx_pos[2])
                distance = vector.length()
                vertex_pos_list[distance] = vtx
        sorted_vertices_pos = sorted(vertex_pos_list)
        sum_vertices = sum(sorted_vertices_pos)
        x=  0
        y = 0
        z = 0
        x_end = 0
        y_end = 0
        z_end = 0
        for inf_vtx in sorted_vertices_pos:

            inf = inf_vtx / sum_vertices
            pos = cmds.xform('{}.vtx[{}]'.format(base_mesh, vertex_pos_list[inf_vtx]), q=True, ws=True, t=True)
            pos_end = cmds.xform('{}.vtx[{}]'.format(shape_list[index],vertex_pos_list[inf_vtx]), q = True, ws =  True, t = True)
            x_end += pos_end[0] * inf
            y_end += pos_end[1] * inf
            z_end += pos_end[2] * inf
            x += pos[0] * inf
            y += pos[1] * inf
            z += pos[2] * inf

        start = [x,y,z]
        end = [x_end, y_end, z_end]

        primary_axis = om.MVector(x_end-x,
                                  y_end-y,
                                  z_end-z)

        scale = primary_axis.length()

        vert_normal = cmds.polyNormalPerVertex('{}.vtx[{}]'.format(base_mesh,vertex_pos_list[sorted_vertices_pos[-1]]), query=True, normalXYZ=True)
        normals_x = []
        normals_y = []
        normals_z = []
        normal_num = len(vert_normal) / 3
        for i in range(int(normal_num)):
            x = vert_normal[0 + 3 * i]
            y = vert_normal[1 + 3 * i]
            z = vert_normal[2 + 3 * i]

            normals_x.append(x)
            normals_y.append(y)
            normals_z.append(z)

        moyenneNormal_x = sum(normals_x) / len(normals_x)
        moyenneNormal_y = sum(normals_y) / len(normals_y)
        moyenneNormal_z = sum(normals_z) / len(normals_z)

        normal = om.MVector(moyenneNormal_x, moyenneNormal_y, moyenneNormal_z)
        start_point = om.MPoint(start[0],start[1],start[2])
        controls_ext_normal = normal.normalize()
        control_point =  start_point + (controls_ext_normal * scale_control)
        print(control_point.x)

        primary_axis = primary_axis.normalize()
        tertiary_axis = primary_axis.normalize() ^ normal.normalize()

        secondary_axis = primary_axis.normalize() ^ tertiary_axis.normalize()

        matrix = om.MMatrix(((primary_axis.x,primary_axis.y,primary_axis.z,0),
                             (secondary_axis.x,secondary_axis.y,secondary_axis.z,0),
                             (tertiary_axis.x,tertiary_axis.y,tertiary_axis.z,0),
                             (control_point.x,control_point.y,control_point.z,1)))

        scale_matrix = om.MMatrix(((scale,0,0,0),(0,scale,0,0),(0,0,scale,0),(0,0,0,1)))

        scaled_matrix = scale_matrix * matrix
        xform_matrix = [scaled_matrix[0],scaled_matrix[1],scaled_matrix[2],scaled_matrix[3],
                        scaled_matrix[4],scaled_matrix[5],scaled_matrix[6],scaled_matrix[7],
                        scaled_matrix[8],scaled_matrix[9],scaled_matrix[10],scaled_matrix[11],
                        scaled_matrix[12],scaled_matrix[13],scaled_matrix[14],scaled_matrix[15]]
        grp = cmds.group(em = True, n= shape_list[index]+'_ctrl_offset')

        loc = cmds.spaceLocator(n = shape_list[index]+'_ctrl')[0]
        cmds.parent(loc,grp)
        cmds.xform(grp,ws = True, m = xform_matrix)
        target = cmds.blendShape(bs, query = True, target = True)[-1]
        cmds.connectAttr(loc+'.tx',bs[0]+'.'+target)
        cmds.transformLimits(loc, tx = [0,1], etx = [1,1])



controls_from_shapes('group3','_kevin',0.1)
