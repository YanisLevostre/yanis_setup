import json
import maya.cmds as cmds
namespace = ""

with open("C:/Users/Yanis/PycharmProjects/yanis_setup/RigPipe/rig_tools/rigSetup_naming.json") as json_data:
    data = json.load(json_data)
    json_data.close()

def import_reference(namespace):
    side = namespace.split("_")[0]
    name = namespace.split("_")[1]

    cmds.file(rfn = namespace + 'RN',importReference = True)
    node_list = cmds.ls(namespace + ':*',tr=True)

    for node in node_list:
        new_name = node
        for nom in data[name]:
            if nom in node:
                new_name = new_name.replace(nom,data[name][nom])
        cmds.rename(node,new_name)
    cmds.namespace( removeNamespace = ":"+namespace, mergeNamespaceWithRoot = True)
