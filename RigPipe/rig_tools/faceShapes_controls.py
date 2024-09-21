import maya.cmds as cmds
import maya.api.OpenMaya as om

import sys
sys.path.insert(0, 'C:/Users/Yanis/PycharmProjects/yanis_setup/' )

from RigPipe.lib.constraint import *
import json

folder = 'C:/Users/Yanis/PycharmProjects/yanis_setup/datas/'
base_name = 'cartoon_hiRes'
with open(folder+base_name+'.json') as json_data:
    data = json.load(json_data)
    json_data.close()

rig_grp = cmds.group(em = True, n = 'faceRig_grp')
input_grp = cmds.group(em = True, n = 'faceRig_input_grp')
guide_grp = cmds.group(em=True, n='faceRig_guide_grp')
input_datas_grp = cmds.group(em=True, n='faceRig_inputDatas_grp')
controls_grp = cmds.group(em=True, n='faceRig_controls_grp')
setup_grp = cmds.group(em=True, n='faceRig_setup_grp')
output_grp = cmds.group(em=True, n='faceRig_output_grp')
parent_grp = cmds.group(em = True, n = 'faceRig_parent_input' )
offset_grp = cmds.group(em=True, n= 'faceRig_parent_offset')

L_upperLid = data['L_upperLid']
L_lowerLid = data['L_lowerLid']
R_upperLid = data['R_upperLid']
R_lowerLid = data['R_lowerLid']
cmds.parent(input_grp,guide_grp,controls_grp,setup_grp,output_grp,rig_grp)
cmds.parent(parent_grp,offset_grp,input_datas_grp,input_grp)

def controls_from_shapes(shape_grp,base_mesh,scale_control):
    control_mesh = cmds.duplicate(base_mesh, n = base_mesh+'_constraintControlsDuplicate')
    ref_mesh = cmds.duplicate(base_mesh, n=base_mesh + '_ref_Duplicate')
    control_mesh_shape = cmds.listRelatives(control_mesh, s=True)[0]
    ref_mesh_shape = cmds.listRelatives(ref_mesh, s=True)[0]
    cmds.parent(control_mesh_shape,ref_mesh,setup_grp)
    control_bs = cmds.blendShape(base_mesh,control_mesh)[0]

    cmds.setAttr(control_bs+'.'+base_mesh,1)

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


        guide = cmds.spaceLocator(n = shape_list[index]+'_guide')[0]

        transform_grp = cmds.group(em=True, n=shape_list[index] + '_transform_input')
        input_loc = cmds.spaceLocator(n = shape_list[index]+'_input_loc')[0]
        cmds.parent(input_loc,parent_grp)
        cmds.parent(transform_grp,input_datas_grp)
        multMatrix(source = guide, target = input_loc, offset = offset_grp )
        parentMatrix(source= input_loc, target= transform_grp)

        cmds.parent(guide,guide_grp)
        cmds.xform(guide, ws=True, m=xform_matrix)

        grp = cmds.group(em = True, n= shape_list[index]+'_ctrl_offset')
        inverse_grp =  cmds.group(em = True, n= shape_list[index]+'_ctrl_inverseOffset')
        loc = cmds.spaceLocator(n = shape_list[index]+'_ctrl')[0]
        cmds.parent(loc, inverse_grp )
        cmds.parent(inverse_grp,grp)
        cmds.parent(grp,controls_grp)
        parentOffsetMatrix(source= transform_grp, target = grp)
        closestPointOnMesh = cmds.createNode('closestPointOnMesh', n =  shape_list[index]+'_CPOM')
        follicle = cmds.createNode('follicle', n =  shape_list[index]+'_follicle')
        follicle_grp = cmds.listRelatives(follicle, p = True)
        cmds.parent(follicle_grp,setup_grp)

        cmds.connectAttr(closestPointOnMesh + '.parameterU', follicle + '.parameterU')
        cmds.connectAttr(closestPointOnMesh + '.parameterV', follicle + '.parameterV')

        cmds.connectAttr(ref_mesh_shape+'.outMesh', closestPointOnMesh+'.inMesh')
        cmds.connectAttr(control_mesh_shape + '.outMesh', follicle + '.inputMesh')
        cmds.connectAttr(guide+'.translate', closestPointOnMesh+'.inPosition')
        decMx = cmds.createNode('decomposeMatrix', n = shape_list[index]+'_inverse_decMx')
        rivet_loc = cmds.spaceLocator(n = shape_list[index]+'_inverse_loc')[0]
        cmds.parent(rivet_loc,setup_grp)
        cmds.connectAttr(follicle + '.outTranslate', rivet_loc + '.translate')
        cmds.connectAttr(loc+'.inverseMatrix', decMx+'.inputMatrix')
        cmds.connectAttr(decMx+'.outputTranslate', inverse_grp+'.translate')
        multMx = cmds.createNode('multMatrix',n =  shape_list[index]+'_inverse_multMx')
        decMx2 = cmds.createNode('decomposeMatrix', n = shape_list[index]+'_inverse2_decMx')
        cmds.connectAttr(rivet_loc+'.worldMatrix[0]',multMx+'.matrixIn[0]')
        cmds.connectAttr(guide + '.worldInverseMatrix[0]', multMx + '.matrixIn[1]')
        cmds.connectAttr(multMx+'.matrixSum', decMx2+'.inputMatrix')
        cmds.connectAttr(decMx2+'.outputTranslate', grp+'.translate')

        cmds.xform(guide,ws = True, m = xform_matrix)

        target = cmds.blendShape(bs, query = True, target = True)[-1]
        cmds.connectAttr(loc+'.tx',bs[0]+'.'+target)
        cmds.transformLimits(loc, tx = [0,1], etx = [1,1])

#def tweakers(base_mesh):



controls_from_shapes('group3','_kevin',0.1)

