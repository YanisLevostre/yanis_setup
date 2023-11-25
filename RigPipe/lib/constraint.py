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

def directConnection(source = None, target = None):
    cmds.connectAttr(source + '.translate', target + '.translate')
    cmds.connectAttr(source + '.rotate', target + '.rotate')
    cmds.connectAttr(source + '.scale', target + '.scale')

