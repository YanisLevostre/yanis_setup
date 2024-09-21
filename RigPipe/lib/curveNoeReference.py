import math
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


class NurbsCircleNode(OpenMayaMPx.MPxNode):
    kPluginNodeName = "nurbsCircleNode"
    kPluginNodeId = OpenMaya.MTypeId(0x00000125)

    aRadius = OpenMaya.MObject()
    aOutputCurve = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    @staticmethod
    def creator():
        return OpenMayaMPx.asMPxPtr(NurbsCircleNode())

    @staticmethod
    def initialize():
        nAttr = OpenMaya.MFnNumericAttribute()
        tAttr = OpenMaya.MFnTypedAttribute()

        NurbsCircleNode.aRadius = nAttr.create("radius", "in", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)
        nAttr.setStorable(True)

        NurbsCircleNode.aOutputCurve = tAttr.create("outputCurve", "outCurve", OpenMaya.MFnData.kNurbsCurve)
        tAttr.setWritable(False)
        tAttr.setStorable(False)

        NurbsCircleNode.addAttribute(NurbsCircleNode.aRadius)
        NurbsCircleNode.addAttribute(NurbsCircleNode.aOutputCurve)

        NurbsCircleNode.attributeAffects(NurbsCircleNode.aRadius, NurbsCircleNode.aOutputCurve)

        def compute(self, plug, dataBlock):
            if plug == NurbsCircleNode.aOutputCurve:
                input_value = dataBlock.inputValue(NurbsCircleNode.aRadius).asFloat()

                num_points = 101
                points = OpenMaya.MPointArray([OpenMaya.MPoint(math.cos(math.radians(i * 360.0)) * input_value,
                                                               math.sin(math.radians(i * 360.0)) * input_value,
                                                               0.0) for i in range(num_points)])
                circle_data = OpenMaya.MFnNurbsCurveData().create()

                circle_fn = OpenMaya.MFnNurbsCurve()
                status = OpenMaya.MStatus()

                knots = OpenMaya.MDoubleArray(num_points + 2, 0.0)
                for i in range(num_points + 2):
                    knots[i] = float(i)

                circle_fn.create(points, knots, 1, OpenMaya.MFnNurbsCurve.kOpen, False, False, circle_data, status)

                output_curve_attr = dataBlock.outputValue(NurbsCircleNode.aOutputCurve)
                output_curve_attr.setMObject(circle_data)
                dataBlock.setClean(plug)
            else:
                return OpenMaya.kUnknownParameter


def initializePlugin(plugin):
    pluginFn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        pluginFn.registerNode(NurbsCircleNode.kPluginNodeName, NurbsCircleNode.kPluginNodeId,
                              NurbsCircleNode.creator, NurbsCircleNode.initialize)
    except Exception as e:
        OpenMaya.MGlobal.displayError(f"Failed to register node: {NurbsCircleNode.kPluginNodeName}\n{e}")
        raise


def uninitializePlugin(plugin):
    pluginFn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        pluginFn.deregisterNode(NurbsCircleNode.kPluginNodeId)
    except Exception as e:
        OpenMaya.MGlobal.displayError(f"Failed to deregister node: {NurbsCircleNode.kPluginNodeName}\n{e}")
        raise