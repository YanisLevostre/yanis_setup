import maya.cmds as cmds
import json

data = {}
for grp in cmds.ls():

    if "_guide_grp" in grp:
        print('ok')
        data[grp] = {'translate':cmds.getAttr(grp+'.translate')[0],'rotate':cmds.getAttr(grp+'.rotate')[0],'scale':cmds.getAttr(grp+'.scale')[0]}
        for node in cmds.listRelatives(grp, ad = True):
            if cmds.objectType(node,isType = 'transform'):
                data[node] = {'translate': cmds.getAttr(node + '.translate')[0], 'rotate': cmds.getAttr(node + '.rotate')[0],
                             'scale': cmds.getAttr(node + '.scale')[0]}



json_object = json.dumps(data, indent=4)

with open("D:/Mon Drive/rig/templates/characater/toonGirl/guides.json", "w") as outfile:
    outfile.write(json_object)
print(data)
print ('done')