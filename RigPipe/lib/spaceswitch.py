import maya.cmds as cmds
from constraint import multMatrix
def do_spaceswitch(module_name= None,guide = None,transform = None,parent_list = None):
    # create groups and add locators

    spaceOffsets = cmds.group(em=True, n=module_name + '_spaceOffsets_grp')
    spaceInputs = cmds.group(em=True, n=module_name + '_spaceInputs_grp')
    cmds.parent(spaceOffsets, spaceInputs, module_name + '_input_grp')
    blendMatrix = cmds.createNode('blendMatrix', n=module_name + '_blendMatrix')
    follow = cmds.createNode('transform', n=module_name + "_followPlug_input")
    outNode = transform
    drivers = parent_list
    enum_list = ":".join(drivers)
    cmds.addAttr(follow, ln='follow', k=True, at='enum', en=enum_list)

    for i,driver in enumerate(drivers):
        grpOffset = cmds.group(em = True, n = '{}_{}_spaceOffset_grp'.format(module_name,driver))
        grpInput = cmds.group(em=True, n='{}_{}_spaceInput_grp'.format(module_name, driver))
        locSpace = cmds.spaceLocator(n = '{}_{}_loc,'.format(module_name, driver))[0]
        cmds.parent(locSpace,grpInput)
        cmds.parent(grpOffset,spaceOffsets)
        cmds.parent(grpInput, spaceInputs)

        # connect guide to space input
        multMatrix(source = guide, target = locSpace,offset = grpOffset)

        # create choices and blend
        cmds.connectAttr( locSpace+ '.worldMatrix[0]', blendMatrix + '.target[' + str(i) + '].targetMatrix')
        cond = cmds.createNode('condition', n=module_name + driver + '_condition')
        cmds.setAttr(cond + '.secondTerm', i)
        cmds.setAttr(cond + '.colorIfTrueR', 1)
        cmds.setAttr(cond + '.colorIfFalseR', 0)
        cmds.connectAttr(follow + '.follow', cond + '.firstTerm')
        cmds.connectAttr(cond + '.outColorR', blendMatrix + '.target[' + str(i) + '].useMatrix')

    # connect to the out transform
    dec = cmds.createNode('decomposeMatrix', n=module_name + 'follow_decomposeMatrix')
    cmds.connectAttr(blendMatrix + '.outputMatrix', dec + '.inputMatrix')

    cmds.connectAttr(dec + '.outputTranslate', outNode + '.translate', f = True)
    cmds.connectAttr(dec + '.outputRotate', outNode + '.rotate', f = True)
    cmds.connectAttr(dec + '.outputScale', outNode + '.scale', f = True)
