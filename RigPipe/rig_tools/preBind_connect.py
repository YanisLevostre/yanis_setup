import maya.cmds as cmds

def connectBindPreMatrix(joints):
    for jnt in joints:
        connections = cmds.connectionInfo( jnt+'.worldMatrix[0]', dfs=True)
        for node in connections:
            if cmds.objectType(node.split('.')[0]) == 'skinCluster':
                if cmds.objExists(jnt.replace('_skin','PreBind_jnt')):
                    cmds.connectAttr(jnt.replace('_skin','PreBind_jnt.worldInverseMatrix[0]'),node.replace('matrix','bindPreMatrix'),f = True)

