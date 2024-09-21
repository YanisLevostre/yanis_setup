import maya.cmds as cmds
from math import sqrt


def distance(a, b):
    result = sqrt((a[0] - b[0]) ** 2 +
                  (a[1] - b[1]) ** 2 +
                  (a[2] - b[2]) ** 2)
    return result


def curvePoints(skinCluster, start_inf, inf_1, inf_2, end_inf):
    cmds.skinCluster(skinCluster, e=True, siv=start_inf)
    vertices_start = cmds.ls(sl=True, fl=True)

    cmds.skinCluster(skinCluster, e=True, siv=end_inf)
    vertices_end = cmds.ls(sl=True, fl=True)

    cmds.skinCluster(skinCluster, e=True, siv=inf_1)
    vertices_inf1 = cmds.ls(sl=True, fl=True)

    cmds.skinCluster(skinCluster, e=True, siv=inf_2)
    vertices_inf2 = cmds.ls(sl=True, fl=True)

    vertices_cross_start = []
    vertices_cross_end = []
    vertices_cross = []
    for vtx in vertices_start:
        if vtx in vertices_inf1 and vtx in vertices_inf2:
            vertices_cross_start.append(vtx)
    for vtx in vertices_end:
        if vtx in vertices_inf1 and vtx in vertices_inf2:
            vertices_cross_end.append(vtx)

    for vtx in vertices_inf1:
        if vtx in vertices_inf2:
            vertices_cross.append(vtx)

    cmds.select(cl=True)
    startPos = cmds.xform(vertices_cross_start[0], q=True, ws=True, t=True)



    point = startPos
    for vtx in vertices_cross:
        pos = cmds.xform(vtx, q=True, ws=True, t=True)
        if distance(point, pos) == 0:
            vertices_cross.remove(vtx)

    controlPoints = [startPos]
    for i in range(100):

        closePoint = {}
        closePointList = []
        for vtx in vertices_cross:
            pos = cmds.xform(vtx, q=True, ws=True, t=True)
            if distance(point, pos) < 0.16:
                closePoint[distance(point, pos)] = vtx
                closePointList.append(vtx)
        for v in closePointList:
            vertices_cross.remove(v)

        if closePoint != {}:
            posLoc = cmds.xform(closePoint[sorted(closePoint)[-1]],ws = True, t = True, q = True)
            controlPoints.append(posLoc)
            point = posLoc
        else:
            break

    curve = cmds.curve(p=controlPoints)
    cmds.rebuildCurve(curve,s =3)
    return curve


