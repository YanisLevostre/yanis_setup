import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
from maya.api.OpenMaya import MVector, MPoint, MMatrix
import math

nodeName = "YL_intersection"
nodeId = OpenMaya.MTypeId(0x200fff)


class YL_intersection(OpenMayaMPx.MPxNode):
    inScale = OpenMaya.MObject()
    inJoint1ratio = OpenMaya.MObject()
    inJoint2ratio = OpenMaya.MObject()
    inVec1_a = OpenMaya.MObject()
    inVec1_b = OpenMaya.MObject()
    inVec2_a = OpenMaya.MObject()
    inVec2_b = OpenMaya.MObject()
    inUp_point = OpenMaya.MObject()

    outPushPos = OpenMaya.MObject()
    outPushXAxis = OpenMaya.MObject()
    outPushYAxis = OpenMaya.MObject()
    outPushZAxis = OpenMaya.MObject()

    outPushJoint1Pos = OpenMaya.MObject()
    outPushJoint1XAxis = OpenMaya.MObject()
    outPushJoint1YAxis = OpenMaya.MObject()
    outPushJoint1ZAxis = OpenMaya.MObject()

    outPushJoint2Pos = OpenMaya.MObject()
    outPushJoint2XAxis = OpenMaya.MObject()
    outPushJoint2YAxis = OpenMaya.MObject()
    outPushJoint2ZAxis = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, dataBlock):

        def vector_intersect(vector_1_point_a, vector_1_point_b, vector_2_point_a, vector_2_point_b, up_point,
                             scale,
                             joint1_ratio, joint2_ratio):
            # temp maya import datas

            # vector 1
            # vector_1_point_a = (0, 0, -2)
            # vector_1_point_b = (-6, 0, -2)
            vector1 = MVector(vector_1_point_b[0] - vector_1_point_a[0],
                              vector_1_point_b[1] - vector_1_point_a[1],
                              vector_1_point_b[2] - vector_1_point_a[2]
                              )

            # vector 2
            # vector_2_point_a = (1.904, 0, -0.613)
            # vector_2_point_b = (3.436, 0, 4.146)
            vector2 = MVector(vector_2_point_b[0] - vector_2_point_a[0],
                              vector_2_point_b[1] - vector_2_point_a[1],
                              vector_2_point_b[2] - vector_2_point_a[2]
                              )

            # vector mid dir vec1
            vector_mid_dir1 = MVector(vector_1_point_a[0] - vector_2_point_a[0],
                                      vector_1_point_a[1] - vector_2_point_a[1],
                                      vector_1_point_a[2] - vector_2_point_a[2]
                                      )
            mid_point = (MPoint(vector_2_point_a) + (vector_mid_dir1 * 0.5))

            # vector mid dir vec2
            vector_mid_dir2 = MVector(vector_2_point_a[0] - vector_1_point_a[0],
                                      vector_2_point_a[1] - vector_1_point_a[1],
                                      vector_2_point_a[2] - vector_1_point_a[2]
                                      )

            mid_length = vector_mid_dir1.length()

            if vector_mid_dir1.length() != 0:
                # vec1_vec2 angle
                vec1_vec2_cos = vector1.normalize() * vector2.normalize()
                vec1_vec2_angle = math.acos(vec1_vec2_cos)
                # print('vec1_vec2 angle: {}'.format(math.degrees(vec1_vec2_angle)))

                # vec1_vecMid angle
                vec1_vecMid_cos = vector1.normalize() * vector_mid_dir1.normalize()
                vec1_vecMid_angle = math.acos(abs(vec1_vecMid_cos))
                # print('vec1_vecMid angle: {}'.format(math.degrees(vec1_vecMid_angle)))

                # vec2_vecMid angle
                vec2_vecMid_cos = vector2.normalize() * vector_mid_dir2.normalize()
                vec2_vecMid_angle = math.acos(abs(vec2_vecMid_cos))
                # print('vec2_vecMid angle: {}'.format(math.degrees(vec2_vecMid_angle)))

                if math.sin(vec1_vec2_angle) != 0:
                    rapport_sinus = (mid_length / 2.00) / math.sin(vec1_vec2_angle / 2.00)
                    push_length = rapport_sinus * math.sin(vec1_vecMid_angle)
                    # print(push_length)

                else:
                    # print('flat angle')
                    push_length = 0

            else:
                # print('bindPose')
                push_length = 0

            # mid point

            # mid-up axis
            vectorUp_temp = MVector(up_point[0] - mid_point[0],
                                    up_point[1] - mid_point[1],
                                    up_point[2] - mid_point[2]
                                    )
            vectorUp_temp.normalize()

            # mid-front temp axis
            vectorFront = MVector(vector_2_point_a[0] - mid_point[0],
                                  vector_2_point_a[1] - mid_point[1],
                                  vector_2_point_a[2] - mid_point[2]
                                  )
            vectorFront.normalize()

            # mid-side axis

            vectorSide = vectorFront ^ vectorUp_temp
            vectorSide.normalize()
            vectorUp = vectorSide ^ vectorFront

            # print (vectorUp,vectorSide,vectorFront)

            mid_matrix = MMatrix((vectorUp[0], vectorUp[1], vectorUp[2], 0,
                                  vectorSide[0], vectorSide[1], vectorSide[2], 0,
                                  vectorFront[0], vectorFront[1], vectorFront[2], 0,
                                  mid_point[0], mid_point[1], mid_point[2], 1
                                  ))
            push_matrix = MMatrix((1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, push_length, 0, 0, 1))
            vector_push = MVector(push_length, 0, 0)

            push_matrix *= mid_matrix

            push_point = (push_matrix[12], push_matrix[13], push_matrix[14])
            # find matrix joint vect1
            vector_1_pushtarget = MVector(vector_1_point_b[0] - push_point[0],
                                          vector_1_point_b[1] - push_point[1],
                                          vector_1_point_b[2] - push_point[2]
                                          )

            joint_vect1_pos = (MPoint(push_point) + (vector_1_pushtarget * joint1_ratio))

            joint_vect1_front = MVector(joint_vect1_pos[0] - push_point[0],
                                        joint_vect1_pos[1] - push_point[1],
                                        joint_vect1_pos[2] - push_point[2])
            joint_vect1_front.normalize()

            joint_vect1_up_temp = MVector(up_point[0] - joint_vect1_pos[0],
                                          up_point[1] - joint_vect1_pos[1],
                                          up_point[2] - joint_vect1_pos[2])

            joint_vect1_up_temp.normalize()

            joint_vect1_side = joint_vect1_up_temp ^ joint_vect1_front

            joint_vect1_side.normalize()

            joint_vect1_up = joint_vect1_side ^ joint_vect1_front

            joint1_matrix = (joint_vect1_up[0] * scale, joint_vect1_up[1] * scale, joint_vect1_up[2] * scale,
                             joint_vect1_side[0] * scale, joint_vect1_side[1] * scale,
                             joint_vect1_side[2] * scale,
                             joint_vect1_front[0] * scale, joint_vect1_front[1] * scale,
                             joint_vect1_front[2] * scale,
                             joint_vect1_pos[0], joint_vect1_pos[1], joint_vect1_pos[2]
                             )

            vector_2_pushtarget = MVector(vector_2_point_b[0] - push_point[0],
                                          vector_2_point_b[1] - push_point[1],
                                          vector_2_point_b[2] - push_point[2]
                                          )

            # find joint 2 matrix

            joint_vect2_pos = (MPoint(push_point) + (vector_2_pushtarget * joint2_ratio))

            joint_vect2_front = MVector(joint_vect2_pos[0] - push_point[0],
                                        joint_vect2_pos[1] - push_point[1],
                                        joint_vect2_pos[2] - push_point[2])
            joint_vect2_front.normalize()

            joint_vect2_up_temp = MVector(up_point[0] - joint_vect2_pos[0],
                                          up_point[1] - joint_vect2_pos[1],
                                          up_point[2] - joint_vect2_pos[2])

            joint_vect2_up_temp.normalize()

            joint_vect2_side = joint_vect2_up_temp ^ joint_vect2_front

            joint_vect2_side.normalize()

            joint_vect2_up = joint_vect2_side ^ joint_vect2_front

            joint2_matrix = (joint_vect2_up[0] * scale, joint_vect2_up[1] * scale, joint_vect2_up[2] * scale,
                             joint_vect2_side[0] * scale, joint_vect2_side[1] * scale,
                             joint_vect2_side[2] * scale,
                             joint_vect2_front[0] * scale, joint_vect2_front[1] * scale,
                             joint_vect2_front[2] * scale,
                             joint_vect2_pos[0], joint_vect2_pos[1], joint_vect2_pos[2]
                             )
            push_matrix_out = (
                push_matrix[0], push_matrix[1], push_matrix[2], push_matrix[4], push_matrix[5], push_matrix[6],
                push_matrix[8], push_matrix[9], push_matrix[10], push_matrix[12], push_matrix[13], push_matrix[14])

            return {'pushjoint': push_matrix_out, 'joint1': joint1_matrix, 'joint2': joint2_matrix}


        dataHandleScale = dataBlock.inputValue(YL_intersection.inScale)
        dataHandleJoint1ratio = dataBlock.inputValue(YL_intersection.inJoint1ratio)
        dataHandleJoint2ratio = dataBlock.inputValue(YL_intersection.inJoint2ratio)
        dataHandleVect1_a = dataBlock.inputValue(YL_intersection.inVec1_a)
        dataHandleVect1_b = dataBlock.inputValue(YL_intersection.inVec1_b)
        dataHandleVect2_a = dataBlock.inputValue(YL_intersection.inVec2_a)
        dataHandleVect2_b = dataBlock.inputValue(YL_intersection.inVec2_b)
        dataHandleUp_point = dataBlock.inputValue(YL_intersection.inUp_point)

        inScaleVal = dataHandleScale.asFloat()
        inJoint1ratioVal = dataHandleJoint1ratio.asFloat()
        inJoint2ratioeVal = dataHandleJoint2ratio.asFloat()
        inVect1_aVal = dataHandleVect1_a.asFloat3()
        inVect1_bVal = dataHandleVect1_b.asFloat3()
        inVect2_aVal = dataHandleVect2_a.asFloat3()
        inVect2_bVal = dataHandleVect2_b.asFloat3()
        inUp_pointVal = dataHandleUp_point.asFloat3()

        outPushjoint = \
            vector_intersect(inVect1_aVal, inVect1_bVal, inVect2_aVal, inVect2_bVal, inUp_pointVal, inScaleVal,
                             inJoint1ratioVal, inJoint2ratioeVal)['pushjoint']

        outPushjoint1 = \
            vector_intersect(inVect1_aVal, inVect1_bVal, inVect2_aVal, inVect2_bVal, inUp_pointVal, inScaleVal,
                             inJoint1ratioVal, inJoint2ratioeVal)['joint1']
        outPushjoint2 = \
            vector_intersect(inVect1_aVal, inVect1_bVal, inVect2_aVal, inVect2_bVal, inUp_pointVal, inScaleVal,
                             inJoint1ratioVal, inJoint2ratioeVal)['joint2']

        dataHandleOutPushJointPos = dataBlock.outputValue(YL_intersection.outPushPos)
        dataHandleOutPushJointXAxis = dataBlock.outputValue(YL_intersection.outPushXAxis)
        dataHandleOutPushJointYAxis = dataBlock.outputValue(YL_intersection.outPushYAxis)
        dataHandleOutPushJointZAxis = dataBlock.outputValue(YL_intersection.outPushZAxis)

        dataHandleOutPushJoint1Pos = dataBlock.outputValue(YL_intersection.outPushJoint1Pos)
        dataHandleOutPushJoint1XAxis = dataBlock.outputValue(YL_intersection.outPushJoint1XAxis)
        dataHandleOutPushJoint1YAxis = dataBlock.outputValue(YL_intersection.outPushJoint1YAxis)
        dataHandleOutPushJoint1ZAxis = dataBlock.outputValue(YL_intersection.outPushJoint1ZAxis)

        dataHandleOutPushJoint2Pos = dataBlock.outputValue(YL_intersection.outPushJoint2Pos)
        dataHandleOutPushJoint2XAxis = dataBlock.outputValue(YL_intersection.outPushJoint2XAxis)
        dataHandleOutPushJoint2YAxis = dataBlock.outputValue(YL_intersection.outPushJoint2YAxis)
        dataHandleOutPushJoint2ZAxis = dataBlock.outputValue(YL_intersection.outPushJoint2ZAxis)

        dataHandleOutPushJointPos.set3Float(outPushjoint[9], outPushjoint[10], outPushjoint[11])
        dataHandleOutPushJointXAxis.set3Float(outPushjoint[0], outPushjoint[1], outPushjoint[2])
        dataHandleOutPushJointYAxis.set3Float(outPushjoint[3], outPushjoint[4], outPushjoint[5])
        dataHandleOutPushJointZAxis.set3Float(outPushjoint[6], outPushjoint[7], outPushjoint[8])

        dataHandleOutPushJoint1Pos.set3Float(outPushjoint1[9], outPushjoint1[10], outPushjoint1[11])
        dataHandleOutPushJoint1XAxis.set3Float(outPushjoint1[0], outPushjoint1[1], outPushjoint1[2])
        dataHandleOutPushJoint1YAxis.set3Float(outPushjoint1[3], outPushjoint1[4], outPushjoint1[5])
        dataHandleOutPushJoint1ZAxis.set3Float(outPushjoint1[6], outPushjoint1[7], outPushjoint1[8])

        dataHandleOutPushJoint2Pos.set3Float(outPushjoint2[9], outPushjoint2[10], outPushjoint2[11])
        dataHandleOutPushJoint2XAxis.set3Float(outPushjoint2[0], outPushjoint2[1], outPushjoint2[2])
        dataHandleOutPushJoint2YAxis.set3Float(outPushjoint2[3], outPushjoint2[4], outPushjoint2[5])
        dataHandleOutPushJoint2ZAxis.set3Float(outPushjoint2[6], outPushjoint2[7], outPushjoint2[8])

        dataBlock.setClean(plug)


def nodeCreator():
    return OpenMayaMPx.asMPxPtr(YL_intersection())


def nodeInitializer():
    mFnAttr = OpenMaya.MFnNumericAttribute()

    # push joint
    # output attributes
    YL_intersection.outPushPos = mFnAttr.create("pushPos", "ppos", OpenMaya.MFnNumericData.k3Float, 0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPushXAxis = mFnAttr.create("pushAxisX", "pXaxis", OpenMaya.MFnNumericData.k3Float, 0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPushYAxis = mFnAttr.create("pushAxisY", "pYaxis", OpenMaya.MFnNumericData.k3Float, 0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPushZAxis = mFnAttr.create("pushAxisZ", "pZaxis", OpenMaya.MFnNumericData.k3Float, 0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    # push joint1
    YL_intersection.outPushJoint1Pos = mFnAttr.create("vect1Pos", "v1pos", OpenMaya.MFnNumericData.k3Float, 0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPushJoint1XAxis = mFnAttr.create("vect1XAxis", "v1Xaxis", OpenMaya.MFnNumericData.k3Float, 0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPushJoint1YAxis = mFnAttr.create("vect1YAxis", "v1Yaxis", OpenMaya.MFnNumericData.k3Float, 0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPushJoint1ZAxis = mFnAttr.create("vect1ZAxis", "v1Zaxis", OpenMaya.MFnNumericData.k3Float, 0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    # push joint2
    YL_intersection.outPushJoint2Pos = mFnAttr.create("vect2Pos", "v2pos", OpenMaya.MFnNumericData.k3Float, 0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPushJoint2XAxis = mFnAttr.create("vect2XAxis", "v2Xaxis", OpenMaya.MFnNumericData.k3Float, 0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPushJoint2YAxis = mFnAttr.create("vect2YAxis", "v2Yaxis", OpenMaya.MFnNumericData.k3Float, 0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPushJoint2ZAxis = mFnAttr.create("vect2ZAxis", "v2Zaxis", OpenMaya.MFnNumericData.k3Float, 0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    # input attributes
    YL_intersection.inScale = mFnAttr.create("scale", "s", OpenMaya.MFnNumericData.kFloat, 1.0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)

    YL_intersection.inJoint1ratio = mFnAttr.create("joint1_ratio", "j1r", OpenMaya.MFnNumericData.kFloat, 0.1)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)

    YL_intersection.inJoint2ratio = mFnAttr.create("joint2_ratio", "j2r", OpenMaya.MFnNumericData.kFloat, 0.1)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)

    YL_intersection.inVec1_a = mFnAttr.create("vect1_a", 'v1a', OpenMaya.MFnNumericData.k3Float)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)
    YL_intersection.inVec1_b = mFnAttr.create("vect1_b", 'v1b', OpenMaya.MFnNumericData.k3Float)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)
    YL_intersection.inVec2_a = mFnAttr.create("vect2_a", 'v2a', OpenMaya.MFnNumericData.k3Float)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)

    YL_intersection.inVec2_b = mFnAttr.create("vect2_b", "v2b", OpenMaya.MFnNumericData.k3Float)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)

    YL_intersection.inUp_point = mFnAttr.create("up_point", "up", OpenMaya.MFnNumericData.k3Float)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)

    YL_intersection.addAttribute(YL_intersection.inScale)
    YL_intersection.addAttribute(YL_intersection.inJoint1ratio)
    YL_intersection.addAttribute(YL_intersection.inJoint2ratio)
    YL_intersection.addAttribute(YL_intersection.inVec1_a)
    YL_intersection.addAttribute(YL_intersection.inVec1_b)
    YL_intersection.addAttribute(YL_intersection.inVec2_a)
    YL_intersection.addAttribute(YL_intersection.inVec2_b)
    YL_intersection.addAttribute(YL_intersection.inUp_point)

    YL_intersection.addAttribute(YL_intersection.outPushPos)
    YL_intersection.addAttribute(YL_intersection.outPushXAxis)
    YL_intersection.addAttribute(YL_intersection.outPushYAxis)
    YL_intersection.addAttribute(YL_intersection.outPushZAxis)

    YL_intersection.addAttribute(YL_intersection.outPushJoint1Pos)
    YL_intersection.addAttribute(YL_intersection.outPushJoint1XAxis)
    YL_intersection.addAttribute(YL_intersection.outPushJoint1YAxis)
    YL_intersection.addAttribute(YL_intersection.outPushJoint1ZAxis)

    YL_intersection.addAttribute(YL_intersection.outPushJoint2Pos)
    YL_intersection.addAttribute(YL_intersection.outPushJoint2XAxis)
    YL_intersection.addAttribute(YL_intersection.outPushJoint2YAxis)
    YL_intersection.addAttribute(YL_intersection.outPushJoint2ZAxis)

    for attr in (
            YL_intersection.inScale, YL_intersection.inJoint1ratio, YL_intersection.inJoint2ratio,
            YL_intersection.inVec1_b,
            YL_intersection.inVec1_a, YL_intersection.inVec2_a, YL_intersection.inVec2_b, YL_intersection.inUp_point):
        YL_intersection.attributeAffects(attr, YL_intersection.outPushPos)
        YL_intersection.attributeAffects(attr, YL_intersection.outPushXAxis)
        YL_intersection.attributeAffects(attr, YL_intersection.outPushYAxis)
        YL_intersection.attributeAffects(attr, YL_intersection.outPushZAxis)
        YL_intersection.attributeAffects(attr, YL_intersection.outPushJoint1Pos)
        YL_intersection.attributeAffects(attr, YL_intersection.outPushJoint1XAxis)
        YL_intersection.attributeAffects(attr, YL_intersection.outPushJoint1YAxis)
        YL_intersection.attributeAffects(attr, YL_intersection.outPushJoint1ZAxis)
        YL_intersection.attributeAffects(attr, YL_intersection.outPushJoint2Pos)
        YL_intersection.attributeAffects(attr, YL_intersection.outPushJoint2XAxis)
        YL_intersection.attributeAffects(attr, YL_intersection.outPushJoint2YAxis)
        YL_intersection.attributeAffects(attr, YL_intersection.outPushJoint2ZAxis)


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
