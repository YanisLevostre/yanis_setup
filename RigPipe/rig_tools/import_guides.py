import maya.cmds as cmds
import json

with open("D:/Mon Drive/rig/templates/characater/toonGirl/guides.json") as json_data:
    data = json.load(json_data)
    json_data.close()
for grp in cmds.ls(sl=True):
    if "_guide_grp" in grp:
        if grp in data:
            cmds.setAttr(grp+'.translate',data[grp]['translate'][0],data[grp]['translate'][1],data[grp]['translate'][2])
            cmds.setAttr(grp + '.rotate', data[grp]['rotate'][0], data[grp]['rotate'][1],
                         data[grp]['rotate'][2])
            cmds.setAttr(grp + '.scale', data[grp]['scale'][0], data[grp]['scale'][1],
                         data[grp]['scale'][2])

        for node in cmds.listRelatives(grp,ad = True):
            if cmds.objExists(node) and node in data:
                cmds.setAttr(node + '.translate', data[node]['translate'][0], data[node]['translate'][1],
                             data[node]['translate'][2])
                cmds.setAttr(node + '.rotate', data[node]['rotate'][0], data[node]['rotate'][1],
                             data[node]['rotate'][2])
                cmds.setAttr(node + '.scale', data[node]['scale'][0], data[node]['scale'][1],
                             data[node]['scale'][2])
print ('done')