import maya.cmds as cmds
from maya.api.OpenMaya import MVector, MPoint, MMatrix
import math

#####

#####

# datas


def vector_intersect(vector_1_point_a,vector_1_point_b,vector_2_point_a,vector_2_point_b,up_point,scale,joint1_ratio,joint2_ratio):
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

    joint1_matrix = MMatrix((joint_vect1_up[0] * scale, joint_vect1_up[1] * scale, joint_vect1_up[2] * scale, 0,
                             joint_vect1_side[0] * scale, joint_vect1_side[1] * scale, joint_vect1_side[2] * scale, 0,
                             joint_vect1_front[0] * scale, joint_vect1_front[1] * scale, joint_vect1_front[2] * scale, 0,
                             joint_vect1_pos[0], joint_vect1_pos[1], joint_vect1_pos[2], 1
                             ))

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

    joint2_matrix = MMatrix((joint_vect2_up[0] * scale, joint_vect2_up[1] * scale, joint_vect2_up[2] * scale, 0,
                             joint_vect2_side[0] * scale, joint_vect2_side[1] * scale, joint_vect2_side[2] * scale, 0,
                             joint_vect2_front[0] * scale, joint_vect2_front[1] * scale, joint_vect2_front[2] * scale, 0,
                             joint_vect2_pos[0], joint_vect2_pos[1], joint_vect2_pos[2], 1
                             ))

    return {'pushjoint':push_matrix,'joint1':joint1_matrix,'joint2':joint2_matrix}