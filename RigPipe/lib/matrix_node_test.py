import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

nodeName = "YanisNode"
nodeId = OpenMaya.MTypeId(0x200fff)


class YanisNode(OpenMayaMPx.MPxNode):
    inMatrix = OpenMaya.MObject()
    outMatrix = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, dataBlock):


        if plug == YanisNode.outMatrix:

            valueList = [1,0,0,0,
                         0,1,0,0,
                         0,0,1,0,
                         2,4,0,1]
            matrix = OpenMaya.MMatrix()
            OpenMaya.MScriptUtil.createMatrixFromList(valueList, matrix)

            dataHandleOutMatrix = dataBlock.outputValue(YanisNode.outMatrix)
            dataHandleOutMatrix.setMMatrix(matrix)
            dataBlock.setClean(plug)
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    return OpenMayaMPx.asMPxPtr(YanisNode())


def nodeInitializer():
    mFnAttr = OpenMaya.MFnMatrixAttribute()

    YanisNode.inMatrix = mFnAttr.create("inMatrix", "inMatrix", OpenMaya.MFnMatrixData.kMatrix)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(0)


    YanisNode.outMatrix = mFnAttr.create("outMatrix", "outMatrix", OpenMaya.MFnMatrixData.kMatrix)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YanisNode.addAttribute(YanisNode.inMatrix)
    YanisNode.addAttribute(YanisNode.outMatrix)

    YanisNode.attributeAffects(YanisNode.inMatrix, YanisNode.outMatrix)


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
        sys.stderr.write("Failed to de-register command: %s\n" %  nodeName)