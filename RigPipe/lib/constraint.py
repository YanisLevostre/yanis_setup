import maya.cmds as cmds
# mult matrix

nodes = cmds.ls(sl=True)
def multMatrix(source= None,target= None,offset = None):
    mult = cmds.createNode('multMatrix',n = source + '_'+ offset+'_multMatrix')
    cmds.connectAttr(source+'.worldMatrix[0]',mult + '.matrixIn[0]')
    cmds.connectAttr(offset+'.worldInverseMatrix[0]',mult + '.matrixIn[1]')
    cmds.connectAttr(mult+'.matrixSum',target+'.offsetParentMatrix')


def parentOffsetMatrix(source = None, target = None):
    cmds.connectAttr(source+'.worldMatrix[0]',target+'.offsetParentMatrix')

def parentMatrix(source = None, target = None):
    dec = cmds.createNode('decomposeMatrix',n = source+'_'+target+'_decomposeMatrix')
    cmds.connectAttr(source+'.worldMatrix[0]',dec+'.inputMatrix')
    cmds.connectAttr(dec+'.outputTranslate',target+'.translate')
    cmds.connectAttr(dec+'.outputRotate',target+'.rotate')
    cmds.connectAttr(dec+'.outputScale',target+'.scale')

def directConnection(source = None, target = None, force = True):
    cmds.connectAttr(source + '.translate', target + '.translate', f = force)
    cmds.connectAttr(source + '.rotate', target + '.rotate', f = force)
    cmds.connectAttr(source + '.scale', target + '.scale', f = force)

def aimMatrix(point = None,
              up_matrix = None,
              target_matrix =None,
              primaryAxis=None,
              secondaryAxis = None,
              destination = None,
              primaryVector = None,
              secondaryVector =None):
    aim = cmds.createNode("aimMatrix", n = point +'_'+destination +  '_aimMatrix')
    if point:
        cmds.connectAttr(point+'.worldMatrix[0]',aim+'.inputMatrix')

    cmds.connectAttr(target_matrix + '.worldMatrix[0]',aim+'.primaryTargetMatrix')
    cmds.connectAttr(up_matrix + '.worldMatrix[0]', aim + '.secondaryTargetMatrix')
    cmds.setAttr(aim+'.secondaryMode',1)
    if primaryVector:
        cmds.setAttr( aim + '.primaryTargetVector',primaryVector[0],primaryVector[1],primaryVector[2])
    if secondaryVector:
        cmds.setAttr( aim + '.secondaryTargetVector',secondaryVector[0],secondaryVector[1],secondaryVector[2])
    if primaryAxis:
        cmds.connectAttr(primaryAxis + '.translate', aim + '.primaryInputAxis')
    if secondaryAxis:
        cmds.connectAttr(secondaryAxis + '.translate', aim + '.secondaryInputAxis')
    cmds.connectAttr(aim+'.outputMatrix',destination+'.offsetParentMatrix')

