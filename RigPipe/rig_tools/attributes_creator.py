import maya.cmds as cmds
import json
import sys

with open("C:/Users/Yanis/PycharmProjects/yanis_setup/RigPipe/rig_tools/attributes_naming.json") as json_data:
    data = json.load(json_data)
    json_data.close()

def attributes_connector(namespace):
    side = namespace.split('_')[0]
    name = namespace.split('_')[1]
    for name in data:
        attribute_grp = []
        controls = {}
        attr_dict = {}
        for grp in data[name]:
            attribute_grp.append(grp)
        for grp in attribute_grp:
            for attr in data[name][grp]:
                for control in data[name][grp][attr]['controls']:
                    separator = data[name][grp][attr]['separator']
                    if control not in controls:
                        controls[control] = {}
                    if separator not in controls[control]:
                        controls[control][separator] = {}
                    controls[control][separator][grp + '.' + attr] = data[name][grp][attr]

        for control in controls:
            for separator in controls[control]:
                cmds.addAttr(namespace + ':' + control, ln=separator, k=True, r=True, at='enum', en="__________", )
                cmds.setAttr(namespace + ':' + control + '.' + separator, k=False, cb=True)
                for attr in controls[control][separator]:
                    attr_info = controls[control][separator][attr]
                    if attr_info['type'] == 'enum':
                        cmds.addAttr(namespace + ':' + control, at='enum', en=attr_info["enum"], ln=attr_info['name'],
                                     k=True)

                    if attr_info['type'] == "bool":
                        cmds.addAttr(namespace + ':' + control, at='bool', ln=attr_info['name'],
                                     k=True)

                    if attr_info['type'] == "float":
                        cmds.addAttr(namespace + ':' + control, at='float', min=attr_info["min"], max=attr_info["max"],
                                     ln=attr_info['name'],
                                     k=True)

                    cmds.connectAttr(namespace + ':' + control + "." + attr_info['name'], namespace + ":" + attr)
