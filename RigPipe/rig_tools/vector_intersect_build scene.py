import maya.cmds as cmds

cmds.loadPlugin("C:/Users/Yanis/PycharmProjects/yanis_setup/RigPipe/rig_tools/YL_intersection.py")

InterIn = cmds.createNode('YL_intersection', n='YL_intersectionIn')
InterOut = cmds.createNode('YL_intersection', n='YL_intersectionOut')
InterInUp = cmds.createNode('YL_intersection', n='YL_intersectionInUp')
InterOutUp = cmds.createNode('YL_intersection', n='YL_intersectionOutUp')

for inter, locList in ('YL_intersectionIn', ['armIn_0_loc', 'armIn_1_loc','armIn_1bis_loc', 'armIn_2_loc','up_front']), (
'YL_intersectionOut', ['armOut_0_loc', 'armOut_1_loc','armOut_1bis_loc', 'armOut_2_loc','up_back']), (
'YL_intersectionInUp', ['armInUp_0_loc', 'armInUp_1_loc','armInUp_1bis_loc', 'armInUp_2_loc','up_front']), (
'YL_intersectionOutUp', ['armOutUp_0_loc', 'armOutUp_1_loc','armOutUp_1bis_loc', 'armOutUp_2_loc','up_back']):
    shape0 = cmds.listRelatives(locList[0], s=True)[0]
    shape1 = cmds.listRelatives(locList[1], s=True)[0]
    shape2 = cmds.listRelatives(locList[2], s=True)[0]
    shape3 = cmds.listRelatives(locList[3], s=True)[0]
    up = cmds.listRelatives(locList[4], s=True)[0]
    cmds.connectAttr(shape0+'.worldPosition[0]',inter+'.vect1_b')
    cmds.connectAttr(shape1 + '.worldPosition[0]', inter + '.vect1_a')
    cmds.connectAttr(shape2 + '.worldPosition[0]', inter + '.vect2_a')
    cmds.connectAttr(shape3 + '.worldPosition[0]', inter + '.vect2_b')
    cmds.connectAttr(up + '.worldPosition[0]', inter + '.up_point')
    curve = cmds.curve(n = inter+'_cv',p =([0,0,0],(0,1,0),(0,2,0),(0,3,0),(0,4,0)),d = 2)
    curveShape = cmds.listRelatives(curve,s = True)[0]
    #cmds.connectAttr(shape0+'.worldPosition[0]',curveShape+'.controlPoints[0]')
    #cmds.connectAttr(inter + '.vect1Pos', curveShape + '.controlPoints[1]')
    #cmds.connectAttr(inter + '.pushPos', curveShape + '.controlPoints[2]')
    #cmds.connectAttr(inter + '.vect2Pos', curveShape + '.controlPoints[3]')
    #cmds.connectAttr(shape3 + '.worldPosition[0]', curveShape + '.controlPoints[4]')




# out



