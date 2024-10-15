import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
from maya.api.OpenMaya import MVector, MPoint, MMatrix
import math

sys.path.insert(0, 'C:/Users/Yanis/PycharmProjects/yanis_setup/')
from RigPipe.rig_tools.vectorIntersect_math import quadratic_bezier_curve, vector_intersect
nodeName = "YL_intersection"
nodeId = OpenMaya.MTypeId(0x200fff)


class YL_intersection(OpenMayaMPx.MPxNode):
    inPinch = OpenMaya.MObject()
    inBind = OpenMaya.MObject()
    inPushLimit = OpenMaya.MObject()
    inOutJointsNumber = OpenMaya.MObject()
    inDirection = OpenMaya.MObject()
    inVec1_a = OpenMaya.MObject()
    inVec1_b = OpenMaya.MObject()
    inVec2_a = OpenMaya.MObject()
    inVec2_b = OpenMaya.MObject()
    inBindVec1_a = OpenMaya.MObject()
    inBindVec1_b = OpenMaya.MObject()
    inBindVec2_a = OpenMaya.MObject()
    inBindVec2_b = OpenMaya.MObject()
    outPoint0 = OpenMaya.MObject()
    outMatrix = OpenMaya.MObject()
    outPoint1 = OpenMaya.MObject()
    outPoint2 = OpenMaya.MObject()
    outPoint3 = OpenMaya.MObject()
    outPoint4 = OpenMaya.MObject()
    outPoint5 = OpenMaya.MObject()
    outPoint6 = OpenMaya.MObject()
    outPoint7 = OpenMaya.MObject()
    outPoint8 = OpenMaya.MObject()
    outPoint9 = OpenMaya.MObject()

    bind_vect1_a = []
    bind_vect1_b = []
    bind_vect2_a = []
    bind_vect2_b = []

    nbr_output = 1
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, dataBlock):







        dataHandlePinch = dataBlock.inputValue(YL_intersection.inPinch)
        dataHandlePushLimit = dataBlock.inputValue(YL_intersection.inPushLimit)
        dataHandleDirection = dataBlock.inputValue(YL_intersection.inDirection)
        dataHandleVec1_a = dataBlock.inputValue(YL_intersection.inVec1_a)
        dataHandleVec1_b = dataBlock.inputValue(YL_intersection.inVec1_b)
        dataHandleVec2_a = dataBlock.inputValue(YL_intersection.inVec2_a)
        dataHandleVec2_b = dataBlock.inputValue(YL_intersection.inVec2_b)
        dataHandleBindVec1_a = dataBlock.inputValue(YL_intersection.inBindVec1_a)
        dataHandleBindVec1_b = dataBlock.inputValue(YL_intersection.inBindVec1_b)
        dataHandleBindVec2_a = dataBlock.inputValue(YL_intersection.inBindVec2_a)
        dataHandleBindVec2_b = dataBlock.inputValue(YL_intersection.inBindVec2_b)





        pinch = dataHandlePinch.asFloat()
        pushLimit = dataHandlePushLimit.asFloat()
        direction = dataHandleDirection.asFloat()
        vect1_a = []
        vect1_b = []
        vect2_a = []
        vect2_b = []
        bind_vect1_a = []
        bind_vect1_b = []
        bind_vect2_a = []
        bind_vect2_b = []

        for list,matrix in ((vect1_a,dataHandleVec1_a),
                            (vect1_b, dataHandleVec1_b),
                            (vect2_a, dataHandleVec2_a),
                            (vect2_b, dataHandleVec2_b),
                            (bind_vect1_a, dataHandleBindVec1_a),
                            (bind_vect1_b, dataHandleBindVec1_b),
                            (bind_vect2_a, dataHandleBindVec2_a),
                            (bind_vect2_b, dataHandleBindVec2_b),
                            ):
            for i in range(4):
                for j in range(4):
                    list.append(matrix.asMatrix()(i,j))

        dataHandleBind = dataBlock.inputValue(YL_intersection.inBind)
        bind = dataHandleBind.asInt()

        if bind == 1:
            for list, matrix in (
                                 (YL_intersection.bind_vect1_a, dataHandleVec1_a),
                                 (YL_intersection.bind_vect1_b, dataHandleVec1_b),
                                 (YL_intersection.bind_vect2_a, dataHandleVec2_a),
                                 (YL_intersection.bind_vect2_b, dataHandleVec2_b)
                                 ):
                for i in range(4):
                    for j in range(4):
                        list.append(matrix.asMatrix()(i, j))
            dataHandleBind.setInt(2)
        elif bind ==2:
            bind_vect1_a = YL_intersection.bind_vect1_a
            bind_vect1_b = YL_intersection.bind_vect1_b
            bind_vect2_a = YL_intersection.bind_vect2_a
            bind_vect2_b = YL_intersection.bind_vect2_b


        dataHandleNumber = dataBlock.inputValue(YL_intersection.inOutJointsNumber)
        nbr = dataHandleNumber.asInt()



        matrixArrayHandle = dataBlock.outputArrayValue(YL_intersection.outMatrix)
        matrixArrayBuilder = matrixArrayHandle.builder()
        point2 = \
            vector_intersect(vect1_a, vect1_b, vect2_a, vect2_b, direction, pinch, pushLimit, bind_vect1_a,
                             bind_vect1_b,
                             bind_vect2_a, bind_vect2_b, nbr)["points"]
        for i in range(nbr):

            out_matrix = OpenMaya.MMatrix()
            OpenMaya.MScriptUtil.createMatrixFromList(point2[i], out_matrix)
            elementHandle = matrixArrayBuilder.addElement(i)
            elementHandle.setMMatrix(out_matrix)

        matrixArrayHandle.set(matrixArrayBuilder)





        points = vector_intersect(vect1_a,vect1_b,vect2_a,vect2_b,direction,pinch,pushLimit,bind_vect1_a,bind_vect1_b,bind_vect2_a,bind_vect2_b,10)["points"]

        out_matrix_0 = OpenMaya.MMatrix()
        out_matrix_1 = OpenMaya.MMatrix()
        out_matrix_2 = OpenMaya.MMatrix()
        out_matrix_3 = OpenMaya.MMatrix()
        out_matrix_4 = OpenMaya.MMatrix()
        out_matrix_5 = OpenMaya.MMatrix()
        out_matrix_6 = OpenMaya.MMatrix()
        out_matrix_7 = OpenMaya.MMatrix()
        out_matrix_8 = OpenMaya.MMatrix()
        out_matrix_9 = OpenMaya.MMatrix()
        for list,matrix in ((points[0],out_matrix_0),
                            (points[1], out_matrix_1),
                            (points[2], out_matrix_2),
                            (points[3], out_matrix_3),
                            (points[4], out_matrix_4),
                            (points[5], out_matrix_5),
                            (points[6], out_matrix_6),
                            (points[7], out_matrix_7),
                            (points[8], out_matrix_8),
                            (points[9], out_matrix_9)
                            ):
            OpenMaya.MScriptUtil.createMatrixFromList(list, matrix)


        dataHandleOutMatrix0 = dataBlock.outputValue(YL_intersection.outPoint0)
        dataHandleOutMatrix0.setMMatrix(out_matrix_0)
        dataHandleOutMatrix1 = dataBlock.outputValue(YL_intersection.outPoint1)
        dataHandleOutMatrix1.setMMatrix(out_matrix_1)
        dataHandleOutMatrix2 = dataBlock.outputValue(YL_intersection.outPoint2)
        dataHandleOutMatrix2.setMMatrix(out_matrix_2)
        dataHandleOutMatrix3 = dataBlock.outputValue(YL_intersection.outPoint3)
        dataHandleOutMatrix3.setMMatrix(out_matrix_3)
        dataHandleOutMatrix4 = dataBlock.outputValue(YL_intersection.outPoint4)
        dataHandleOutMatrix4.setMMatrix(out_matrix_4)
        dataHandleOutMatrix5 = dataBlock.outputValue(YL_intersection.outPoint5)
        dataHandleOutMatrix5.setMMatrix(out_matrix_5)
        dataHandleOutMatrix6 = dataBlock.outputValue(YL_intersection.outPoint6)
        dataHandleOutMatrix6.setMMatrix(out_matrix_6)
        dataHandleOutMatrix7 = dataBlock.outputValue(YL_intersection.outPoint7)
        dataHandleOutMatrix7.setMMatrix(out_matrix_7)
        dataHandleOutMatrix8 = dataBlock.outputValue(YL_intersection.outPoint8)
        dataHandleOutMatrix8.setMMatrix(out_matrix_8)
        dataHandleOutMatrix9 = dataBlock.outputValue(YL_intersection.outPoint9)
        dataHandleOutMatrix9.setMMatrix(out_matrix_9)



        dataBlock.setClean(plug)






def nodeCreator():
    return OpenMayaMPx.asMPxPtr(YL_intersection())


def nodeInitializer():
    mFnAttr = OpenMaya.MFnMatrixAttribute()
    mFnAttrNum = OpenMaya.MFnNumericAttribute()
    mFnAttrEnum = OpenMaya.MFnEnumAttribute()

    YL_intersection.inBind = mFnAttrEnum.create('bind', 'bind')
    mFnAttrEnum.addField('off',0)
    mFnAttrEnum.addField('bind', 1)
    mFnAttrEnum.addField('binded', 2)

    mFnAttrEnum.setReadable(1)
    mFnAttrEnum.setWritable(1)
    mFnAttrEnum.setStorable(1)
    mFnAttrEnum.setKeyable(1)

    YL_intersection.inVec1_a = mFnAttr.create('vect_1_a', 'vect_1_a')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(0)

    YL_intersection.inVec1_b = mFnAttr.create('vect_1_b', 'vect_1_b')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(0)

    YL_intersection.inVec2_a = mFnAttr.create('vect_2_a', 'vect_2_a')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(0)

    YL_intersection.inVec2_b = mFnAttr.create('vect_2_b', 'vect_2_b')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(0)

    YL_intersection.inBindVec1_a = mFnAttr.create('bind_vect_1_a', 'bind_vect_1_a')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(0)

    YL_intersection.inBindVec1_b = mFnAttr.create('bind_vect_1_b', 'bind_vect_1_b')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(0)

    YL_intersection.inBindVec2_a = mFnAttr.create('bind_vect_2_a', 'bind_vect_2_a')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(0)

    YL_intersection.inBindVec2_b = mFnAttr.create('bind_vect_2_b', 'bind_vect_2_b')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(0)

    YL_intersection.inPinch = mFnAttrNum.create("pinch", "pinch", OpenMaya.MFnNumericData.kFloat, 0.1)

    mFnAttrNum.setReadable(1)
    mFnAttrNum.setWritable(1)
    mFnAttrNum.setStorable(1)
    mFnAttrNum.setKeyable(1)

    YL_intersection.inOutJointsNumber = mFnAttrNum.create("outJointsNumber", "outJointsNumber", OpenMaya.MFnNumericData.kInt, 5)

    mFnAttrNum.setReadable(1)
    mFnAttrNum.setWritable(1)
    mFnAttrNum.setStorable(1)
    mFnAttrNum.setKeyable(0)

    YL_intersection.inPushLimit = mFnAttrNum.create("pushLimit", "pushLimit", OpenMaya.MFnNumericData.kFloat, 10)

    mFnAttrNum.setReadable(1)
    mFnAttrNum.setWritable(1)
    mFnAttrNum.setStorable(1)
    mFnAttrNum.setKeyable(1)

    YL_intersection.inDirection = mFnAttrNum.create("direction", "direction", OpenMaya.MFnNumericData.kFloat, 1)

    mFnAttrNum.setReadable(1)
    mFnAttrNum.setWritable(1)
    mFnAttrNum.setStorable(1)
    mFnAttrNum.setKeyable(1)

    YL_intersection.outMatrix = mFnAttr.create('outMatrix', 'outMatrix')

    mFnAttr.setArray(True)
    mFnAttr.setUsesArrayDataBuilder(True)
    mFnAttr.setKeyable(False)
    mFnAttr.setWritable(False)
    mFnAttr.setStorable(False)

    YL_intersection.outPoint0 = mFnAttr.create('outMatrix_0', 'outMatrix_0')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPoint1 = mFnAttr.create('outMatrix_1', 'outMatrix_1')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPoint2 = mFnAttr.create('outMatrix_2', 'outMatrix_2')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPoint3 = mFnAttr.create('outMatrix_3', 'outMatrix_3')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPoint4 = mFnAttr.create('outMatrix_4', 'outMatrix_4')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPoint5 = mFnAttr.create('outMatrix_5', 'outMatrix_5')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPoint6 = mFnAttr.create('outMatrix_6', 'outMatrix_6')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPoint7 = mFnAttr.create('outMatrix_7', 'outMatrix_7')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPoint8 = mFnAttr.create('outMatrix_8', 'outMatrix_8')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPoint9 = mFnAttr.create('outMatrix_9', 'outMatrix_9')

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.addAttribute(YL_intersection.inVec1_a)
    YL_intersection.addAttribute(YL_intersection.inVec1_b)
    YL_intersection.addAttribute(YL_intersection.inVec2_a)
    YL_intersection.addAttribute(YL_intersection.inVec2_b)

    YL_intersection.addAttribute(YL_intersection.inBindVec1_a)
    YL_intersection.addAttribute(YL_intersection.inBindVec1_b)
    YL_intersection.addAttribute(YL_intersection.inBindVec2_a)
    YL_intersection.addAttribute(YL_intersection.inBindVec2_b)


    YL_intersection.addAttribute(YL_intersection.inPinch)
    YL_intersection.addAttribute(YL_intersection.inOutJointsNumber)
    YL_intersection.addAttribute(YL_intersection.inPushLimit)
    YL_intersection.addAttribute(YL_intersection.inDirection)
    YL_intersection.addAttribute(YL_intersection.inBind)

    for attr in (YL_intersection.outPoint0,YL_intersection.outPoint1,YL_intersection.outPoint2,YL_intersection.outPoint3,
                 YL_intersection.outPoint4,YL_intersection.outPoint5,YL_intersection.outPoint6,YL_intersection.outPoint7,
                 YL_intersection.outPoint8,YL_intersection.outPoint9,YL_intersection.outMatrix):
        YL_intersection.addAttribute(attr)
        for in_attr in (YL_intersection.inVec1_a,YL_intersection.inVec1_b,YL_intersection.inVec2_a,YL_intersection.inVec2_b,
                        YL_intersection.inBindVec1_a,YL_intersection.inBindVec1_b,YL_intersection.inBindVec2_a,YL_intersection.inBindVec2_b,
                        YL_intersection.inPinch,YL_intersection.inPushLimit,YL_intersection.inDirection):

            YL_intersection.attributeAffects(in_attr, attr)



def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(nodeName, nodeId, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write("Failed to register command : %s\n" % nodeName)


def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(nodeName)
    except:
        sys.stderr.write("Failed to de-register command: %s\n" % nodeName)
