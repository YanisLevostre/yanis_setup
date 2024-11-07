import maya.cmds as cmds
import sys
sys.path.insert(0, 'C:/Users/Yanis/PycharmProjects/yanis_setup/' )
from RigPipe.lib.constraint import *

def do_spaceswitch(module_name=None,node_name = None, guideList=None, parent_list=None,
                   channel=['translate', 'rotate', 'scale']):

    ''' module_name = C_module
        guideList = {guide:transform_input}
        parentList = [local, layout, global, world]'''


    # create groups and add locators
    space_offsets = cmds.group(em=True, n=node_name + '_spaceOffsets_grp')
    space_inputs = cmds.group(em=True, n=node_name + '_spaceInputs_grp')
    follow = cmds.createNode('transform', n=node_name + "_followPlug_input")
    cmds.parent(space_offsets, space_inputs,follow, module_name + '_plugs_grp')


    drivers = parent_list
    enum_list = ":".join(drivers)
    cmds.addAttr(follow, ln='follow', k=True, at='enum', en=enum_list)
    for i, driver in enumerate(drivers):
        grp_offset = cmds.group(em=True, n='{}_{}_spaceOffset_grp'.format(node_name, driver))
        grp_input = cmds.group(em=True, n='{}_{}_spaceInput_grp'.format(node_name, driver))
        cmds.parent(grp_offset, space_offsets)
        cmds.parent(grp_input, space_inputs)
    for guide in guideList:
        print (guide)
        print(guideList)
        name = guide.strip('_guide')
        blend_matrix = cmds.createNode('blendMatrix', n=name + '_blendMatrix')
        out_node = guideList[guide]
        for i, driver in enumerate(drivers):
            grp_offset = '{}_{}_spaceOffset_grp'.format(node_name, driver)
            grp_input = '{}_{}_spaceInput_grp'.format(node_name, driver)
            loc_space = cmds.spaceLocator(n='{}_{}_loc'.format(name, driver))[0]
            cmds.parent(loc_space, grp_input)

            # connect guide to space input
            multMatrix(source=guide, target=loc_space, offset=grp_offset)

            # create choices and blend
            cmds.connectAttr(loc_space + '.worldMatrix[0]', blend_matrix + '.target[' + str(i) + '].targetMatrix')
            cond = cmds.createNode('condition', n=name + driver + '_condition')
            cmds.setAttr(cond + '.secondTerm', i)
            cmds.setAttr(cond + '.colorIfTrueR', 1)
            cmds.setAttr(cond + '.colorIfFalseR', 0)
            cmds.connectAttr(follow + '.follow', cond + '.firstTerm')
            cmds.connectAttr(cond + '.outColorR', blend_matrix + '.target[' + str(i) + '].useMatrix')

        # connect to the out transform
        dec = cmds.createNode('decomposeMatrix', n=name + 'follow_decomposeMatrix')
        cmds.connectAttr(blend_matrix + '.outputMatrix', dec + '.inputMatrix')

        if 'translate' in channel:
            cmds.connectAttr(dec + '.outputTranslate', out_node + '.translate', f=True)
        if 'rotate' in channel:
            cmds.connectAttr(dec + '.outputRotate', out_node + '.rotate', f=True)
        if 'scale' in channel:
            cmds.connectAttr(dec + '.outputScale', out_node + '.scale', f=True)
