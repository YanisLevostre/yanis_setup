import json
import maya.cmds as cmds
sys.path.append('C:/Users/Yanis/PycharmProjects/yanis_setup/RigPipe/lib')
import constraint
with open("C:/Users/Yanis/PycharmProjects/yanis_setup/RigPipe/rig_tools/rigSetup_naming.json") as json_data:
    data = json.load(json_data)
    json_data.close()


ref_list = cmds.ls(type = 'reference')
class reference():

    def __init__(self,refName):
        self.refName = refName
        self.side = refName[:2]
        self.name = refName[2:-2]
        self.nodeList = cmds.referenceQuery(refName,nodes = True)

    def inputs(self):
        inputList = {}
        for node in self.nodeList:
            if 'plugInput' in node:

                node_without_reference = node.split(':')[1].replace('C_',self.side)
                node_rename = node_without_reference
                if self.name in data:
                    for name in data[self.name]:
                        node_rename = node_rename.replace(name,data[self.name][name])
                inputList[node_rename] = node
        return inputList

    def outputs(self):
        outputList = {}
        for node in self.nodeList:
            if 'output' in node:

                node_without_reference = node.split(':')[1].replace('C_', self.side)
                node_rename = node_without_reference
                if self.name in data:
                    for name in data[self.name]:
                        node_rename = node_rename.replace(name, data[self.name][name])
                outputList[node_rename] = node



        return outputList



a = reference(ref_list[1])
c= reference(ref_list[0])
for input in (a.inputs()):
    for ref in ref_list:
        b = reference(ref)
        if b.side == 'C_' or b.side == a.side:
            for output in b.outputs():
                if input.split('_')[-2]== output.split('_')[-2]:
                    directConnection(source=b.outputs()[output], target=a.inputs()[input])
                    if cmds.objExists(b.outputs()[output].replace('output','offsetOutput')):
                        inputOffset = a.inputs()[input].replace('plugInput','plugOffset')
                        outputOffset = b.outputs()[output].replace('output','offsetOutput')
                        directConnection(source=outputOffset, target=inputOffset)





