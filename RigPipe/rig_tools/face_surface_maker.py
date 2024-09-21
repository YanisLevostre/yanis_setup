import maya.cmds as cmds
import json
#from skinToCurves import curvePoints

f = open('C:/Users/Yanis/PycharmProjects/yanis_setup/RigPipe/rig_tools/face_surfaces.json')
data = json.load(f)
f.close()

for surface in data:
    if "up_curve" in data[surface]:
        in_curve_data = data[surface]['in_curve']
        in_curve = curvePoints('skinCluster1', in_curve_data[0], in_curve_data[1], in_curve_data[2], in_curve_data[3])
        out_curve_data = data[surface]['out_curve']
        out_curve = curvePoints('skinCluster1', out_curve_data[0], out_curve_data[1], out_curve_data[2],
                                out_curve_data[3])
        up_curve_data = data[surface]['up_curve']
        up_curve = curvePoints('skinCluster1', up_curve_data[0], up_curve_data[1], up_curve_data[2], up_curve_data[3])
        down_curve_data = data[surface]['down_curve']
        down_curve = curvePoints('skinCluster1', down_curve_data[0], down_curve_data[1], down_curve_data[2],
                                out_curve_data[3])
        cmds.boundary(in_curve, up_curve, out_curve, down_curve, order=True, ep=0,po=1)
        cmds.delete(in_curve, up_curve, out_curve, down_curve)
    else:
        in_curve_data = data[surface]['in_curve']
        in_curve = curvePoints('skinCluster1', in_curve_data[0], in_curve_data[1], in_curve_data[2], in_curve_data[3])
        out_curve_data = data[surface]['out_curve']
        out_curve = curvePoints('skinCluster1', out_curve_data[0], out_curve_data[1], out_curve_data[2], out_curve_data[3])
        cmds.loft(in_curve,out_curve, po=1, ss = 2)
        cmds.delete(in_curve,out_curve)
