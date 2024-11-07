import maya.cmds as cmds
import sys
sys.path.insert(0, 'C:/Users/Yanis/PycharmProjects/yanis_setup/')

from RigPipe.modules.module_tools import Module
from RigPipe.lib.controls import Control
from RigPipe.lib.constraint import multMatrix, directConnection,parentOffsetMatrix,aimMatrix,parentMatrix
import maya.api.OpenMaya as om


def do_tail(fk_nbr=5,ik_nbr=None, name='C_tail', curve=None,local_nbr = None,size = 1):
    # initialize module tail
    tail_module = Module(name='C_tail')
    tail_module.create_groups()
    tail_module.set_axis(primary=[0,1,0],secondary=[1,0,0], tertiary=[0,0,1])

    # create Fk chain control
    if fk_nbr:
        fk_chain = Control(name=name, shape='circle_lolipop')
        fk_chain.control_chain(fk_nbr)
        cmds.parent(fk_chain.groups[0],tail_module.control_grp)

    # get curve points
    fk_curve_points = []
    fk_pos_curve = []
    fk_normal_axis = []

    def get_point_on_curve(nbr,list,pos_list,normal_axis_list,ik = False):
        if curve:
            for index in range(nbr):
                if index == 0:
                    index =0.01
                denominator = nbr -1
                if ik:
                    denominator = nbr -1

                pos = cmds.pointOnCurve(curve, pr=index / denominator, p=True, top = True)
                normal = cmds.getAttr(tail_module.secondaryAxis+'.translate')[0]
                tangent = cmds.pointOnCurve(curve,pr=index / denominator, nt = True, top = True)
                vec_normal = om.MVector(normal)
                vec_tangent = om.MVector(tangent)
                vec = vec_tangent ^ vec_normal
                primaryAxis = cmds.getAttr(tail_module.primaryAxis+'.translate')[0]
                secondary = cmds.getAttr(tail_module.secondaryAxis + '.translate')[0]
                tertiary = cmds.getAttr(tail_module.tertiaryAxis + '.translate')[0]
                old_matrix = om.MMatrix(((vec_tangent[0],vec_tangent[1],vec_tangent[2],0),
                                         (vec_normal[0],vec_normal[1],vec_normal[2],0),
                                         (vec[0],vec[1],vec[2],0),
                                         (pos[0],pos[1],pos[2],1)
                                         ))
                ref_matrix = om.MMatrix(((primaryAxis[0],primaryAxis[1],primaryAxis[2],0),
                                         (secondary[0],secondary[1],secondary[2],0),
                                         (tertiary[0],tertiary[1],tertiary[2],0),
                                         (0,0,0,1)))

                new_matrix = ref_matrix * old_matrix

                matrix = [new_matrix[0],new_matrix[1],new_matrix[2],new_matrix[3],
                          new_matrix[4],new_matrix[5],new_matrix[6],new_matrix[7],
                          new_matrix[8],new_matrix[9],new_matrix[10],new_matrix[11],
                          new_matrix[12],new_matrix[13],new_matrix[14],new_matrix[15]]

                list.append(matrix)
                pos_list.append(pos)
                normal_axis_list.append(normal)
    if fk_nbr:
        get_point_on_curve(fk_nbr,fk_curve_points,fk_normal_axis,fk_pos_curve)
        first_point = fk_curve_points[0]
        last_point = cmds.pointOnCurve(curve, pr=0.98, p=True, top = True)
        last_point_matrix =[]
        for i in range(16):
            last_point_matrix.append(fk_curve_points[-1][i])
        last_point_matrix[12] = last_point[0]
        last_point_matrix[13] = last_point[1]
        last_point_matrix[14] = last_point[2]


    # create base inputs


    tail_module.create_input(name="C_tailBase", space_switch_list=['hip', 'root', 'body', 'layout', 'general', 'world'],
                             matrix=first_point)
    tail_module.create_input(name="C_tailBaseParent", existingGuide=tail_module.inputs["C_tailBase"]["guide"])
    input_plug = tail_module.inputs["C_tailBaseParent"]["plug"]
    input_offset = tail_module.inputs["C_tailBaseParent"]["offset"]

    base_control = Control(name = "C_tailBase", shape="square")
    base_control.simple_control()
    parentOffsetMatrix(tail_module.inputs["C_tailBase"]['data'],base_control.group)
    base_control.make_reversible(controlMatrix=tail_module.controlMatrix_orient)
    cmds.parent(base_control.group,tail_module.control_grp)

    # connect base input to base Parent
    base_guide = tail_module.inputs["C_tailBase"]["guide"]
    parent_plug = tail_module.inputs["C_tailBaseParent"]["plug"]
    parent_offset = tail_module.inputs["C_tailBaseParent"]["offset"]
    parentMatrix(source=base_control.last, target=parent_plug)
    directConnection(source= base_guide,target=parent_offset)


    # create Fk chain inputs
    if fk_nbr:
        for index in range(len(fk_curve_points)):
            tail_module.create_input(name="C_tail_fk" + str(index), plugs={'input': input_plug, 'offset': input_offset},
                                     matrix=fk_curve_points[index])

        tail_module.create_input(name="C_tail_fkEnd", plugs={'input': input_plug, 'offset': input_offset},matrix=last_point_matrix)
        fk_transform_list = []
        for index in range(fk_nbr):
            transform_input = tail_module.inputs["C_tail_fk" + str(index)]["data"]
            fk_transform_list.append(transform_input)
        tail_module.attach_chain_inputs(node_list=fk_chain.groups, input_transform_list=fk_transform_list)
        fk_chain.make_reversible(controlMatrix=tail_module.controlMatrix_orient)

        fk_last_loc = cmds.spaceLocator(n = "C_tail_fkEnd_loc")[0]
        multMatrix(source=tail_module.inputs["C_tail_fkEnd"]['data'],offset=tail_module.inputs["C_tail_fk" + str(fk_nbr-1)]['data'],
                   target=fk_last_loc)

        cmds.parent(fk_last_loc,fk_chain.controls[-1])
        cmds.matchTransform(fk_last_loc,fk_chain.controls[-1])
        #cmds.xform(fk_last_loc, ws = True, t = last_point)

    def create_curves_from_controls(curve_name=None,nbr = None,control_list = None,point_list = None,last_point = None,last_parent = None):
        curve = cmds.curve(p = point_list, n = "C_tail_" +curve_name )
        curve_up = cmds.curve(p=point_list, n="C_tail_up_" + curve_name)
        cmds.parent(curve,curve_up,tail_module.guideSetup_group)

        def connect_curvePoints(control,index):
            multMatrix = cmds.createNode("multMatrix", n="C_tail_up_{}_{}_multMatrix".format(index,curve_name))
            decompose_up = cmds.createNode("decomposeMatrix", n="C_tail_up_{}_{}_decomposeMatrix".format(index,curve_name))
            decompose = cmds.createNode("decomposeMatrix", n="C_tail_{}_()_decomposeMatrix".format(index,curve_name))
            cmds.connectAttr(control+'.worldMatrix[0]',decompose+'.inputMatrix')
            cmds.connectAttr(tail_module.secondaryAxis + '.worldMatrix[0]', multMatrix + '.matrixIn[0]')
            cmds.connectAttr(control + '.worldMatrix[0]', multMatrix + '.matrixIn[1]')
            cmds.connectAttr(multMatrix + '.matrixSum', decompose_up + '.inputMatrix')
            curve_up_shape = cmds.listRelatives(curve_up, shapes=True)[0]
            curve_shape = cmds.listRelatives(curve, shapes=True)[0]
            cmds.connectAttr(decompose_up + '.outputTranslate', curve_up_shape + '.controlPoints[{}]'.format(index))
            cmds.connectAttr(decompose + '.outputTranslate', curve_shape + '.controlPoints[{}]'.format(index))

        for index in range(nbr):
            connect_curvePoints(control_list[index], index)
        if last_point !=None:
            print("yep yep")
            connect_curvePoints(last_parent, nbr)
        return {"curve":curve,"curve_up":curve_up}

    def attach_to_curve(name=None,curve = None,curve_up = None,nbr = None,add_joints = None,control_shape = 'cube'):
        if ik_nbr:
            pos_loc_list = []
            up_loc_list = []
            cmds.createNode('arcLengthDimension',n = "C_tail_{}_arcLength".format(name))
            curve_arcLength_shape = "C_tail_{}_arcLength".format(name)
            cmds.setAttr(curve_arcLength_shape+'.uParamValue',1)
            fk_curve_shape = cmds.listRelatives(curve, shapes=True)[0]
            fk_curve_up_shape = cmds.listRelatives(curve_up, shapes=True)[0]
            cmds.addAttr(tail_module.attr, ln ='{}_stretch'.format(name), at = "bool",k = True)
            scale_mult = cmds.createNode("multiplyDivide", n= "C_tail_{}_scaleMult".format(name))
            cmds.connectAttr(tail_module.inputs["C_tailBaseParent"]["data"]+'.scaleX',scale_mult+'.input1X')

            cond = cmds.createNode('condition', n = "C_tail_{}_stretch_cond".format(name))
            cond_limit = cmds.createNode('condition', n="C_tail_{}_stretchLimit_cond".format(name))
            lengthAttr = tail_module.attr+'.{}_stretch'.format(name)
            cmds.connectAttr(lengthAttr,cond+'.firstTerm')
            cmds.setAttr(cond+'.secondTerm', 1)

            cmds.connectAttr(curve_arcLength_shape + '.arcLength', cond_limit + '.firstTerm')
            cmds.connectAttr(scale_mult+'.outputX', cond_limit + '.secondTerm')
            cmds.connectAttr(scale_mult+'.outputX',cond_limit+'.colorIfFalseR')
            cmds.connectAttr(curve_arcLength_shape + '.arcLength', cond_limit + '.colorIfTrueR')
            cmds.setAttr(cond_limit+'.operation',2)

            cmds.connectAttr(fk_curve_shape+'.worldSpace[0]',curve_arcLength_shape+'.nurbsGeometry')
            cmds.setAttr(scale_mult + '.input2X', cmds.getAttr(curve_arcLength_shape + '.arcLength'))
            cmds.connectAttr(scale_mult+'.outputX',cond+'.colorIfFalseR')
            cmds.connectAttr(cond_limit+'.outColorR', cond + '.colorIfTrueR')
            length_ratio = cmds.createNode("multiplyDivide", n = "C_tail_{}_arcLength_multiplyDivide".format(name))
            cmds.connectAttr( cond+'.outColorR',length_ratio+'.input2X')
            cmds.connectAttr(scale_mult+'.outputX', length_ratio + '.input1X')
            cmds.setAttr(length_ratio+'.operation',2)
            ratio_data = cmds.group(em = True, n ="C_tail_{}_arcLength_ratio".format(name))
            cmds.connectAttr(length_ratio+'.outputX',ratio_data+'.translateX')


            denominator = nbr-1
            pos_list = []
            for index in range(nbr):
                poci = cmds.createNode("pointOnCurveInfo",n = "C_tail_{}_{}_poci".format(name,index))
                cmds.setAttr(poci+'.turnOnPercentage',1)
                poci_up = cmds.createNode("pointOnCurveInfo", n = "C_tail_{}_{}_up_poci".format(name,index))
                cmds.setAttr(poci_up + '.turnOnPercentage', 1)
                cmds.connectAttr(fk_curve_shape+'.worldSpace[0]',poci+'.inputCurve')
                cmds.connectAttr(fk_curve_up_shape + '.worldSpace[0]', poci_up + '.inputCurve')
                ratio_mult = cmds.createNode("multiplyDivide", n ="C_tail_{}_{}_multiplyDivide".format(name,index))
                cmds.connectAttr(ratio_data+'.translateX',ratio_mult+'.input1X')
                cmds.setAttr( ratio_mult + '.input2X',(index/denominator))
                cmds.connectAttr(ratio_mult+'.outputX',poci+'.parameter')
                cmds.connectAttr(ratio_mult + '.outputX', poci_up + '.parameter')

                pos_loc = cmds.spaceLocator(n = "C_tail_{}_{}_pos_loc".format(name,index))[0]
                up_loc = cmds.spaceLocator(n="C_tail_ik_{}_{}_up_loc".format(name,index))[0]
                cmds.parent(up_loc,pos_loc,tail_module.setup_grp)

                cmds.connectAttr(poci+'.position',pos_loc+'.translate' )
                cmds.connectAttr(poci_up + '.position', up_loc+'.translate')

                pos = cmds.xform(pos_loc,ws = True, q = True, t = True)
                pos_list.append(pos)

                pos_loc_list.append(pos_loc)
                up_loc_list.append(up_loc)
            control_list = []
            for index in range(nbr):

                transform = cmds.spaceLocator(n="C_tail_{}_{}_transform_loc".format(name,index))[0]
                if index!=nbr-1:

                    aimMatrix(point=pos_loc_list[index],
                              up_matrix=up_loc_list[index],
                              target_matrix=pos_loc_list[index+1],
                              primaryAxis= tail_module.primaryAxis,
                              secondaryAxis=tail_module.secondaryAxis,
                              destination= transform
                              )
                elif index == nbr-1:
                    aimMatrix(point=pos_loc_list[index],
                              up_matrix=up_loc_list[index],
                              target_matrix=pos_loc_list[index-1],
                              primaryAxis=tail_module.primaryAxis_reverse,
                              secondaryAxis=tail_module.secondaryAxis,
                              destination=transform
                              )

                control = Control(name="C_tail_{}_{}".format(name,index), shape=control_shape)
                control.simple_control()
                parentOffsetMatrix(source=transform,target=control.group)
                cmds.connectAttr(tail_module.inputs['C_tailBaseParent']['data']+'.scale',control.group+'.scale')
                cmds.parent(transform,tail_module.setup_grp)
                cmds.parent(control.group, tail_module.control_grp)
                control_list.append(control.last)
                if add_joints:
                    cmds.select(cl = True)
                    joint = cmds.joint(n ="C_tail_{}_{}_skn".format(name,index) )
                    parentMatrix(source=control.last,target=joint)
                    cmds.parent(joint,tail_module.bind_grp)

        return {"point_list":pos_list,"control_list":control_list}


    ik_datas = create_curves_from_controls(curve_name="fk_curve", nbr=fk_nbr, control_list=fk_chain.lasts,
                                point_list=fk_pos_curve + [last_point], last_parent=fk_last_loc,last_point=last_point)

    attach_ik_datas = attach_to_curve(name="ik", curve=ik_datas["curve"], curve_up=ik_datas["curve_up"], nbr=ik_nbr, add_joints=False,control_shape='sphere')

    local_data = create_curves_from_controls(curve_name="ik_curve", nbr=ik_nbr, control_list=attach_ik_datas["control_list"],
                                point_list=attach_ik_datas["point_list"] )

    attach_local_datas = attach_to_curve(name="local", curve=local_data["curve"], curve_up=local_data["curve_up"], nbr=local_nbr,
                                      add_joints=True)



