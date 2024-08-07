import maya.cmds as cmds
import json


mesh = 'base_head'
shape_grp = 'shapes'
vertex_count = cmds.polyEvaluate(mesh, vertex=True)
name = 'cartoon'
folder = 'C:/Users/Yanis/PycharmProjects/yanis_setup/datas/'
shapes_list = cmds.listRelatives(shape_grp,children = True)

data = {}

data['baseMesh'] = {}
for shape in shapes_list:
    data[shape] = {}

for vtx in range(vertex_count):

    data['baseMesh'][vtx] = cmds.xform('{}.vtx[{}]'.format(mesh,vtx), q = True, ws = True, t = True)
    for shape in shapes_list:

        data[shape][vtx] = cmds.xform('{}.vtx[{}]'.format(shape,vtx) , q = True, ws = True, t = True)

json_object = json.dumps(data, indent=4)
with open(folder + name + '.json', "w") as outfile:
    outfile.write(json_object)

print ('shape export done')