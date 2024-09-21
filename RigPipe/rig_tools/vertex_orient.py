import maya.cmds as cmds
import maya.api.OpenMaya as om
def vertex_orient(sourceMesh,targetMesh):

    vertices = cmds.polyEvaluate(sourceMesh, vertex = True)
    grp = cmds.group(em = True, n = 'morph_attr')
    cmds.addAttr( grp, shortName='morph', longName='morph', defaultValue=0, minValue=0, maxValue=1, k = True )
    reverse = cmds.createNode('reverse')
    cmds.connectAttr(grp+'.morph',reverse+'.inputX')
    joints = []


    for vtx_num in range (vertices):
        vtx = '{}.vtx[{}]'.format(sourceMesh,vtx_num)
        vtx_target = '{}.vtx[{}]'.format(targetMesh, vtx_num)
        pos = cmds.xform(vtx,ws= True, q = True, t = True)
        vtx_target_pos = cmds.xform(vtx_target, ws=True, q=True, t=True)
        cmds.select(vtx)
        vtx_up = cmds.pickWalk(d = 'up')[0]
        if vtx_up != vtx:
            pos_up = cmds.xform(vtx_up,ws= True, q = True, t = True)
        else:
            vtx_up = cmds.pickWalk(d='down')[0]
            pos_up = cmds.xform(vtx_up, ws=True, q=True, t=True)


        vtx_target_up = vtx_up.replace(sourceMesh,targetMesh)
        vtx_target_pos_up = cmds.xform(vtx_target_up,ws= True, q = True, t = True)


        for vertex,position,position_up,mesh in [[vtx,pos,pos_up,sourceMesh],[vtx_target,vtx_target_pos,vtx_target_pos_up,targetMesh]]:

            vert_normal = cmds.polyNormalPerVertex(vertex, query=True, normalXYZ=True)
            normals_x = []
            normals_y = []
            normals_z = []
            normal_num = len(vert_normal)/3
            for i in range(int(normal_num)):
                x = vert_normal[0 + 3*i]
                y = vert_normal[1 + 3*i]
                z = vert_normal[2 + 3*i]

                normals_x.append(x)
                normals_y.append(y)
                normals_z.append(z)

            moyenneNormal_x = sum(normals_x)/len(normals_x)
            moyenneNormal_y = sum(normals_y) / len(normals_y)
            moyenneNormal_z = sum(normals_z) / len(normals_z)

            normal = om.MVector(moyenneNormal_x,moyenneNormal_y,moyenneNormal_z)
            sceneUp = om.MVector(position_up[0]-position[0],position_up[1]-position[1],position_up[2]-position[2])
            normal.normalize()
            sceneUp.normalize()
            vector_y = normal^sceneUp
            vector_y.normalize()
            vector_z = normal^vector_y
            vector_z.normalize()

            matrix = (normal.x,normal.y,normal.z,0,
                      vector_y.x,vector_y.y,vector_y.z,0,
                      vector_z.x,vector_z.y,vector_z.z,0,
                      position[0],position[1],position[2],1
                      )

            loc = cmds.spaceLocator( n = '{}_{}_loc'.format(mesh,vtx_num))
            cmds.xform(loc,ws = True, m = matrix)
            cmds.parent(loc,grp)
        cmds.select(cl=True)
        jnt = cmds.joint(n='{}_{}_jnt'.format(sourceMesh, vtx_num))
        joints.append(jnt)
        constraint = cmds.parentConstraint('{}_{}_loc'.format(sourceMesh,vtx_num),'{}_{}_loc'.format(targetMesh,vtx_num),jnt, mo = False)[0]
        cmds.connectAttr(grp+'.morph',constraint+'.'+'{}_{}_locW1'.format(targetMesh,vtx_num))
        cmds.connectAttr(reverse+'.outputX', constraint + '.' + '{}_{}_locW0'.format(sourceMesh, vtx_num))
        cmds.parent(jnt, grp)

    sourceSkinMesh = cmds.duplicate(sourceMesh)
    targetSkinMesh = cmds.duplicate(targetMesh)
    cmds.select(cl=True)

    for i in joints:
        cmds.select(i,add = True)
    cmds.select(sourceSkinMesh,add= True)
    cmds.skinCluster()

vertex_orient('polySurface2','polySurface1')
