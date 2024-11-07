import json
import maya.cmds as cmds
namespace = ""

with open("C:/Users/Yanis/PycharmProjects/yanis_setup/RigPipe/rig_tools/rigSetup_naming.json") as json_data:
    data = json.load(json_data)
    json_data.close()

def import_reference(namespace):
    side = namespace.split("_")[0]
    name = namespace.split("_")[1]
    side = side + "_"

    cmds.file(rfn = namespace + 'RN',importReference = True)
    node_list = cmds.ls(namespace + ':*')
    for node in node_list:
        shapes = cmds.listRelatives(node, s=True)
        if shapes:
            for shape in shapes:
                node_list.remove(shape)


    for node in node_list:
        if node =='C_quadLimb:limb_ikfk_switch_reverse':
            print ('ok')
        new_name = node
        new_name = new_name.replace(namespace, "")
        for nom in data[name]:
            if nom in node:
                new_name = new_name.replace(nom,data[name][nom])
                if "C_" in new_name:
                    new_name = new_name.replace("C_",side)

        cmds.rename(node,new_name)
    cmds.namespace( removeNamespace = ":"+namespace, mergeNamespaceWithRoot = True)
