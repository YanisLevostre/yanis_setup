import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

nodeName = "YanisNode"
nodeId = OpenMaya.MTypeId(0x200fff)


class YanisNode(OpenMayaMPx.MPxNode):
    inRadius = OpenMaya.MObject()
    inTranslate = OpenMaya.MObject()
    outRotate = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, dataBlock):


        if plug == YanisNode.outRotate:

            dataHandleRadius = dataBlock.inputValue(YanisNode.inRadius)
            dataHandleTranslate = dataBlock.inputValue(YanisNode.inTranslate)

            inRadiusVal = dataHandleRadius.asFloat()
            inTranslate = dataHandleTranslate.asFloat()

            outRotate = float(inRadiusVal) * float(inTranslate)

            dataHandleRotate = dataBlock.outputValue(YanisNode.outRotate)
            dataHandleRotate.setFloat(outRotate)
            dataBlock.setClean(plug)
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    return OpenMayaMPx.asMPxPtr(YanisNode())


def nodeInitializer():
    mFnAttr = OpenMaya.MFnNumericAttribute()

    YanisNode.inRadius = mFnAttr.create("radius", "r", OpenMaya.MFnNumericData.kFloat, 0.0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)

    YanisNode.inTranslate = mFnAttr.create("translate", "t", OpenMaya.MFnNumericData.kFloat, 0.0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)

    YanisNode.outRotate = mFnAttr.create("rotate", "ro", OpenMaya.MFnNumericData.kFloat)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YanisNode.addAttribute(YanisNode.inTranslate)
    YanisNode.addAttribute(YanisNode.inRadius)
    YanisNode.addAttribute(YanisNode.outRotate)

    YanisNode.attributeAffects(YanisNode.inTranslate, YanisNode.outRotate)
    YanisNode.attributeAffects(YanisNode.inRadius, YanisNode.outRotate)


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




