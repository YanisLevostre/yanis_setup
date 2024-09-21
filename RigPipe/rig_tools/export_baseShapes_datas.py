import maya.cmds as cmds
import json


mesh = 'base_head'
shape_grp = 'shapes'

folder = 'C:/Users/Yanis/PycharmProjects/yanis_setup/datas/'

data = {}
vtx_exception = []

lower_mouth = []

L_upperLid = []
L_lowerLid = []
R_upperLid = []
R_lowerLid = []


def export_shapes_datas(name):
    vertex_count = cmds.polyEvaluate(mesh, vertex=True)
    shapes_list = cmds.listRelatives(shape_grp, children=True)
    data['vertexCount'] = vertex_count
    data['exception'] = vtx_exception
    data['lowerMouth'] = lower_mouth
    data['L_upperLid'] = L_upperLid
    data['L_lowerLid'] = L_lowerLid
    data['R_upperLid'] = R_upperLid
    data['R_lowerLid'] = R_lowerLid
    data['shapeList'] = shapes_list
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

def export_vertex_list(list):
    selection = cmds.ls(sl = True, fl = True)
    for vtx in selection:
        list.append(int(vtx.split('[')[1][:-1]))
