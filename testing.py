import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import math
from maya.api.OpenMaya import MVector, MPoint, MMatrix

point1 = OpenMaya.MPoint(0,0,0)
point2 = OpenMaya.MPoint(0,1.5,0.5)
point3 = OpenMaya.MPoint(0,1,5)
points = (point1,point2,point3)
vect1 = OpenMaya.MVector(0,1.5,0.5)
vect2 = OpenMaya.MVector(0,-1.5,1.5)
vect3 = OpenMaya.MVector(0,1,3)
vecs = (vect1,vect2)
length_list = []
length =0
vector_inflist = []
for vect in (vect1,vect2):
    length_list.append(vect.length())
    vector_inflist.append([length, length + vect.length()])
    length+=vect.length()


print (vector_inflist)
def getCurvePoint(param):
    vec_param = param * length
    for i in range(2):
        #if vec_param > vector_inflist[i][0] and vec_param < vector_inflist[i][1]:
            #local_param = (vec_param - vector_inflist[i][0]) / (vector_inflist[i][1]-vector_inflist[i][0] )
            #point = points[0]+vecs[i]*local_param
        point = point1 + vect1 * (param) +vect2 * (param**2) + vect3 * (param**4)

        return (point.x,point.y,point.z)

for i in range(10**3):
    cmds.spaceLocator(p = getCurvePoint(i/10**3))


