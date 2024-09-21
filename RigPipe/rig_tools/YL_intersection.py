import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
from maya.api.OpenMaya import MVector, MPoint, MMatrix
import math
nodeName = "YL_intersection"
nodeId = OpenMaya.MTypeId(0x200fff)


class YL_intersection(OpenMayaMPx.MPxNode):
    inScale = OpenMaya.MObject()
    inPinch = OpenMaya.MObject()
    inPushLimit = OpenMaya.MObject()
    inVec1_a = OpenMaya.MObject()
    inVec1_b = OpenMaya.MObject()
    inVec2_a = OpenMaya.MObject()
    inVec2_b = OpenMaya.MObject()
    inUp_point = OpenMaya.MObject()

    outPoint0 = OpenMaya.MObject()
    outPoint1 = OpenMaya.MObject()
    outPoint2 = OpenMaya.MObject()
    outPoint3 = OpenMaya.MObject()
    outPoint4= OpenMaya.MObject()
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, dataBlock):

        def vector_intersect(vector_1_point_a, vector_1_point_b, vector_2_point_a, vector_2_point_b, up_point,
                             scale,
                             pinch, pushLimit):
            # temp maya import datas
            joint1_ratio = pinch
            joint2_ratio = pinch
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

                    if push_length > pushLimit:
                        push_length = pushLimit

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
        dataHandlePinch = dataBlock.inputValue(YL_intersection.inPinch)
        dataHandlePushLimit = dataBlock.inputValue(YL_intersection.inPushLimit)
        dataHandleVect1_a = dataBlock.inputValue(YL_intersection.inVec1_a)
        dataHandleVect1_b = dataBlock.inputValue(YL_intersection.inVec1_b)
        dataHandleVect2_a = dataBlock.inputValue(YL_intersection.inVec2_a)
        dataHandleVect2_b = dataBlock.inputValue(YL_intersection.inVec2_b)
        dataHandleUp_point = dataBlock.inputValue(YL_intersection.inUp_point)


        inScaleVal = dataHandleScale.asFloat()
        inJPinchVal = dataHandlePinch.asFloat()
        inJoint2PushLimitVal = dataHandlePushLimit.asFloat()
        inVect1_aVal = dataHandleVect1_a.asFloat3()
        inVect1_bVal = dataHandleVect1_b.asFloat3()
        inVect2_aVal = dataHandleVect2_a.asFloat3()
        inVect2_bVal = dataHandleVect2_b.asFloat3()
        inUp_pointVal = dataHandleUp_point.asFloat3()

        datas = vector_intersect(inVect1_aVal, inVect1_bVal, inVect2_aVal, inVect2_bVal, inUp_pointVal,
                         inScaleVal,
                         inJPinchVal, inJoint2PushLimitVal)


        point1 = inVect1_bVal
        point2 = datas['joint1'][9:]
        point3 = datas['pushjoint'][9:]
        point4 = datas['joint2'][9:]
        point5 = inVect2_bVal

        dataHandlePoint0 = dataBlock.outputValue(YL_intersection.outPoint0)
        dataHandlePoint0.set3Float(point1[0],point1[1],point1[2])

        dataHandlePoint0 = dataBlock.outputValue(YL_intersection.outPoint1)
        dataHandlePoint0.set3Float(point2[0],point2[1],point2[2])

        dataHandlePoint0 = dataBlock.outputValue(YL_intersection.outPoint2)
        dataHandlePoint0.set3Float(point3[0],point3[1],point3[2])

        dataHandlePoint0 = dataBlock.outputValue(YL_intersection.outPoint3)
        dataHandlePoint0.set3Float(point4[0],point4[1],point4[2])

        dataHandlePoint0 = dataBlock.outputValue(YL_intersection.outPoint4)
        dataHandlePoint0.set3Float(point5[0],point5[1],point5[2])


        dataBlock.setClean(plug)

        dataBlock.setClean(plug)


def nodeCreator():
    return OpenMayaMPx.asMPxPtr(YL_intersection())


def nodeInitializer():
    mFnAttr = OpenMaya.MFnNumericAttribute()


    YL_intersection.outPoint0 = mFnAttr.create('outPoint0', 'outPoint0', OpenMaya.MFnNumericData.k3Float)
    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    YL_intersection.outPoint1 = mFnAttr.create('outPoint1', 'outPoint1', OpenMaya.MFnNumericData.k3Float)
    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)
    YL_intersection.outPoint2 = mFnAttr.create('outPoint2', 'outPoint2', OpenMaya.MFnNumericData.k3Float)
    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)
    YL_intersection.outPoint3 = mFnAttr.create('outPoint3', 'outPoint3', OpenMaya.MFnNumericData.k3Float)
    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)
    YL_intersection.outPoint4= mFnAttr.create('outPoint4', 'outPoint4', OpenMaya.MFnNumericData.k3Float)
    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    # push joint
    # output attributes
    # input attributes
    YL_intersection.inScale = mFnAttr.create("scale", "s", OpenMaya.MFnNumericData.kFloat, 1.0)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)

    YL_intersection.inPinch = mFnAttr.create("pinch", "pinch", OpenMaya.MFnNumericData.kFloat, 0.1)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)

    YL_intersection.inPushLimit = mFnAttr.create("pushLimit", "pushLimit", OpenMaya.MFnNumericData.kFloat, 0.1)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)

    YL_intersection.inVec1_a = mFnAttr.create("vect1_a", 'v1a', OpenMaya.MFnNumericData.k3Float)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(0)
    YL_intersection.inVec1_b = mFnAttr.create("vect1_b", 'v1b', OpenMaya.MFnNumericData.k3Float)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(0)
    YL_intersection.inVec2_a = mFnAttr.create("vect2_a", 'v2a', OpenMaya.MFnNumericData.k3Float)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(0)

    YL_intersection.inVec2_b = mFnAttr.create("vect2_b", "v2b", OpenMaya.MFnNumericData.k3Float)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(0)

    YL_intersection.inUp_point = mFnAttr.create("up_point", "up", OpenMaya.MFnNumericData.k3Float)

    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(0)

    YL_intersection.addAttribute(YL_intersection.inScale)
    YL_intersection.addAttribute(YL_intersection.inPinch)
    YL_intersection.addAttribute(YL_intersection.inPushLimit)
    YL_intersection.addAttribute(YL_intersection.inVec1_a)
    YL_intersection.addAttribute(YL_intersection.inVec1_b)
    YL_intersection.addAttribute(YL_intersection.inVec2_a)
    YL_intersection.addAttribute(YL_intersection.inVec2_b)
    YL_intersection.addAttribute(YL_intersection.inUp_point)
    YL_intersection.addAttribute(YL_intersection.outPoint0)
    YL_intersection.addAttribute(YL_intersection.outPoint1)
    YL_intersection.addAttribute(YL_intersection.outPoint2)
    YL_intersection.addAttribute(YL_intersection.outPoint3)
    YL_intersection.addAttribute(YL_intersection.outPoint4)

    for output in [YL_intersection.outPoint0,YL_intersection.outPoint1,YL_intersection.outPoint2,YL_intersection.outPoint3,YL_intersection.outPoint4]:

        YL_intersection.attributeAffects(YL_intersection.inScale, output)
        YL_intersection.attributeAffects(YL_intersection.inPinch,output)
        YL_intersection.attributeAffects(YL_intersection.inPushLimit, output)
        YL_intersection.attributeAffects(YL_intersection.inVec1_a, output)
        YL_intersection.attributeAffects(YL_intersection.inVec1_b, output)
        YL_intersection.attributeAffects(YL_intersection.inVec2_a, output)
        YL_intersection.attributeAffects(YL_intersection.inVec2_b, output)
        YL_intersection.attributeAffects(YL_intersection.inUp_point, output)


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
