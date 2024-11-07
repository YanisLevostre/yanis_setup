import maya.cmds as cmds
import sys
sys.path.insert(0, 'C:/Users/Yanis/PycharmProjects/yanis_setup/' )
from RigPipe.lib.constraint import *

namespace = ''
switch_attr = 'limb_ikfk_switch_reverse.outputX'
ik_handle_input = 'C_hand_IkHandle_transform_input'
quadIk_handle_input = 'C_quadHand_IkHandle_transform_input'
pole_vector = 'C_limb_poleVector_limb02_ctrl'
ik_handle = 'C_limb_ikHandle'
joint_start = 'C_limb00_skin'
joint_end = 'C_limb02_skin'
joint_quad_start = 'C_quadLimb_driver00_jnt'
joint_quad_end = 'C_quadLimb_driver03_jnt'
setup_grp = 'C_limb_setup_grp'
quadIk_handle = 'C_quadLimb_driverIkHandle'
quad_pole_vector = 'C_quadLimb_poleVector_quadLimb02_ctrl'
quad_switch_attr = 'quadLimb_ikfk_switch_reverse.outputX'
quad_setup_grp = 'C_quadLimb_setup_grp'
pole_vector_ik_name = 'C_quadLimb_poleVector_ikHandle'
pole_vector_ik_grp = 'C_quadLimb_poleVector00_grp'
pole_Vector_ik_start = 'C_quadLimb_poleVector00_jnt'
pole_Vector_ik_end = 'C_quadLimb_poleVector03_jnt'
quad_RP_ik = "C_quadLimb_ikHandle"
quad_RP_parent = "C_quadLimb_driver02_Ik_loc"
quad_RP_joint_start = "C_quadLimb00_skin"
quad_RP_joint_end = "C_quadLimb02_skin"

def rebuild_iks(namespace):
    if cmds.objExists(namespace + ik_handle):
        cmds.delete(namespace + ik_handle)
    cmds.ikHandle(n = namespace + ik_handle, sj = namespace + joint_start, ee = namespace + joint_end, sol = 'ikRPsolver')
    cmds.poleVectorConstraint(namespace + pole_vector, namespace + ik_handle)
    cmds.connectAttr(namespace + switch_attr, namespace + ik_handle + '.ikBlend')
    parentMatrix(source=namespace + ik_handle_input, target=namespace + ik_handle)
    cmds.parent(namespace + ik_handle, namespace + setup_grp)


def rebuild_quadIks(namespace = '',ikHandle = None):
    if ikHandle:
        cmds.rename(ikHandle,namespace + quadIk_handle )
    else:
        if cmds.objExists(namespace + quadIk_handle):
            cmds.delete(namespace + quadIk_handle)
        cmds.setAttr(namespace + joint_quad_start + '.rotate', 0, 0, 0)
        cmds.ikHandle(n=namespace + quadIk_handle,
                      sj=namespace + joint_quad_start,
                      ee=namespace + joint_quad_end)
        cmds.ikHandle(namespace + quadIk_handle, edit = True, sol = 'ikSpringSolver')
    cmds.poleVectorConstraint(namespace + quad_pole_vector, namespace + quadIk_handle)
    cmds.connectAttr(namespace + quad_switch_attr, namespace + quadIk_handle + '.ikBlend')
    parentMatrix(source=namespace + quadIk_handle_input, target=namespace + quadIk_handle)
    cmds.parent(namespace + quadIk_handle, namespace + quad_setup_grp)

    if cmds.objExists(namespace + pole_vector_ik_name):
        cmds.delete(namespace + pole_vector_ik_name)
    cmds.ikHandle(n=namespace + pole_vector_ik_name,
                  sj=namespace + pole_Vector_ik_start,
                  ee=namespace + pole_Vector_ik_end)
    cmds.parent(namespace + pole_vector_ik_name,namespace + pole_vector_ik_grp)
    cmds.parentConstraint(namespace + quadIk_handle_input,namespace + pole_vector_ik_name, mo = True)

    if cmds.objExists(namespace + quad_RP_ik):
        cmds.delete(namespace + quad_RP_ik)
    cmds.ikHandle(n=namespace + quad_RP_ik, sj=namespace + quad_RP_joint_start, ee=namespace + quad_RP_joint_end, sol='ikRPsolver')
    cmds.parent(namespace+quad_RP_ik, namespace + quad_RP_parent)
    cmds.poleVectorConstraint(namespace + quad_pole_vector, namespace + quad_RP_ik)
    cmds.connectAttr(namespace + quad_switch_attr, namespace + quad_RP_ik + '.ikBlend')




def delete_iks(namespace = ''):
    for ik in [namespace + pole_vector_ik_name,namespace + quadIk_handle,namespace + ik_handle, namespace + quad_RP_ik]:
        if cmds.objExists(ik):
            cmds.delete(ik)





