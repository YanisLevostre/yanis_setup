import maya.cmds as cmds
import sys
sys.path.insert(0, 'C:/Users/Yanis/PycharmProjects/yanis_setup/' )
from RigPipe.lib.constraint import *

namespace = ''
switch_attr = 'limb_ikfk_switch_reverse.outputX'
ik_handle_input = 'C_hand_IkHandle_transform_input'
pole_vector = 'C_limb_poleVector_limb02_ctrl'
ik_handle = 'C_limb_ikHandle'
joint_start = 'C_limb00_skin'
joint_end = 'C_limb02_skin'
setup_grp = 'C_limb_setup_grp'
def rebuild_iks(namespace):
    cmds.delete(namespace + ik_handle)
    cmds.ikHandle(n = namespace + ik_handle, sj = namespace + joint_start, ee = namespace + joint_end, sol = 'ikRPsolver')
    cmds.poleVectorConstraint(namespace + pole_vector, namespace + ik_handle)
    cmds.connectAttr(namespace + switch_attr, namespace + ik_handle + '.ikBlend')
    parentMatrix(source=namespace + ik_handle_input, target=namespace + ik_handle)
    cmds.parent(namespace + ik_handle, namespace + setup_grp)
