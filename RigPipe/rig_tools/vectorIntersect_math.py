import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
from maya.api.OpenMaya import MVector, MPoint, MMatrix
import math


#####

#####

def quadratic_bezier_curve(points, t):
    # Extract coordinates of the control points
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
    z_coords = [point[2] for point in points]

    # Calculate the parametric equations for x, y, and z
    x = (1 - t) ** 4 * x_coords[0] + 4 * (1 - t) ** 3 * t * x_coords[1] + 6 * (1 - t) ** 2 * t ** 2 * x_coords[
        2] + 4 * (1 - t) * t ** 3 * x_coords[3] + t ** 4 * x_coords[4]
    y = (1 - t) ** 4 * y_coords[0] + 4 * (1 - t) ** 3 * t * y_coords[1] + 6 * (1 - t) ** 2 * t ** 2 * y_coords[
        2] + 4 * (1 - t) * t ** 3 * y_coords[3] + t ** 4 * y_coords[4]
    z = (1 - t) ** 4 * z_coords[0] + 4 * (1 - t) ** 3 * t * z_coords[1] + 6 * (1 - t) ** 2 * t ** 2 * z_coords[
        2] + 4 * (1 - t) * t ** 3 * z_coords[3] + t ** 4 * z_coords[4]

    # Return the point on the curve
    return (x, y, z)

def vector_intersect(vector_1_a_matrix, vector_1_b_matrix, vector_2_a_matrix, vector_2_b_matrix,up_direction,
                     pinch, pushLimit,bind_vector_1_a_matrix, bind_vector_1_b_matrix, bind_vector_2_a_matrix, bind_vector_2_b_matrix,num_points):


    # define scale
    scale = 1
    vector_1_a_mat = MMatrix((vector_1_a_matrix[0:4],
                              vector_1_a_matrix[4:8],
                              vector_1_a_matrix[8:12],
                              vector_1_a_matrix[12:]))

    vector_1_b_mat = MMatrix((vector_1_b_matrix[0:4],
                              vector_1_b_matrix[4:8],
                              vector_1_b_matrix[8:12],
                              vector_1_b_matrix[12:]))

    vector_2_a_mat = MMatrix((vector_2_a_matrix[0:4],
                              vector_2_a_matrix[4:8],
                              vector_2_a_matrix[8:12],
                              vector_2_a_matrix[12:]))

    vector_2_b_mat = MMatrix((vector_2_b_matrix[0:4],
                              vector_2_b_matrix[4:8],
                              vector_2_b_matrix[8:12],
                              vector_2_b_matrix[12:]))

    bind_vector_1_a_mat = MMatrix((bind_vector_1_a_matrix[0:4],
                              bind_vector_1_a_matrix[4:8],
                              bind_vector_1_a_matrix[8:12],
                              bind_vector_1_a_matrix[12:]))

    bind_vector_1_b_mat = MMatrix((bind_vector_1_b_matrix[0:4],
                              bind_vector_1_b_matrix[4:8],
                              bind_vector_1_b_matrix[8:12],
                              bind_vector_1_b_matrix[12:]))

    bind_vector_2_a_mat = MMatrix((bind_vector_2_a_matrix[0:4],
                              bind_vector_2_a_matrix[4:8],
                              bind_vector_2_a_matrix[8:12],
                              bind_vector_2_a_matrix[12:]))

    bind_vector_2_b_mat = MMatrix((bind_vector_2_b_matrix[0:4],
                              bind_vector_2_b_matrix[4:8],
                              bind_vector_2_b_matrix[8:12],
                              bind_vector_2_b_matrix[12:]))

    vector_1_a_mat_diff = vector_1_a_mat * bind_vector_1_a_mat.inverse()
    vector_1_b_mat_diff = vector_1_b_mat * bind_vector_1_b_mat.inverse()
    vector_2_a_mat_diff = vector_2_a_mat * bind_vector_2_a_mat.inverse()
    vector_2_b_mat_diff = vector_2_b_mat * bind_vector_2_b_mat.inverse()

    # temp maya import datas
    joint1_ratio = pinch
    joint2_ratio = pinch

    # vector 1
    vector_1_point_a = (vector_1_a_matrix[12], vector_1_a_matrix[13], vector_1_a_matrix[14])
    vector_1_point_b = (vector_1_b_matrix[12], vector_1_b_matrix[13], vector_1_b_matrix[14])
    vector1 = MVector(vector_1_point_b[0] - vector_1_point_a[0],
                      vector_1_point_b[1] - vector_1_point_a[1],
                      vector_1_point_b[2] - vector_1_point_a[2]
                      )

    # vector 2
    vector_2_point_a = (vector_2_a_matrix[12], vector_2_a_matrix[13], vector_2_a_matrix[14])
    vector_2_point_b = (vector_2_b_matrix[12], vector_2_b_matrix[13], vector_2_b_matrix[14])
    vector2 = MVector(vector_2_point_b[0] - vector_2_point_a[0],
                      vector_2_point_b[1] - vector_2_point_a[1],
                      vector_2_point_b[2] - vector_2_point_a[2]
                      )

    # bind_vector 1
    bind_point_1_a_matrix = (bind_vector_1_a_matrix[12], bind_vector_1_a_matrix[13], bind_vector_1_a_matrix[14])
    bind_point_1_b_matrix = (bind_vector_1_b_matrix[12], bind_vector_1_b_matrix[13], bind_vector_1_b_matrix[14])
    bind_vector1 = MVector(bind_point_1_b_matrix[0] - bind_point_1_a_matrix[0],
                      bind_point_1_b_matrix[1] - bind_point_1_a_matrix[1],
                      bind_point_1_b_matrix[2] - bind_point_1_a_matrix[2]
                      )

    # bind_vector 1
    bind_point_2_a_matrix = (bind_vector_2_a_matrix[12], bind_vector_2_a_matrix[13], bind_vector_2_a_matrix[14])
    bind_point_2_b_matrix = (bind_vector_2_b_matrix[12], bind_vector_2_b_matrix[13], bind_vector_2_b_matrix[14])
    bind_vector2 = MVector(bind_point_2_b_matrix[0] - bind_point_2_a_matrix[0],
                           bind_point_2_b_matrix[1] - bind_point_2_a_matrix[1],
                           bind_point_2_b_matrix[2] - bind_point_2_a_matrix[2]
                           )

    # place up point
    up_vector =(bind_vector1+bind_vector2)/2*up_direction

    # vector mid dir vec1
    vector_mid_dir1 = MVector(vector_1_point_a[0] - vector_2_point_a[0],
                              vector_1_point_a[1] - vector_2_point_a[1],
                              vector_1_point_a[2] - vector_2_point_a[2]
                              )
    mid_point = (MPoint(vector_2_point_a) + (vector_mid_dir1 * 0.5))

    up_point = mid_point + up_vector


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


    vector_2_pushtarget = MVector(vector_2_point_b[0] - push_point[0],
                                  vector_2_point_b[1] - push_point[1],
                                  vector_2_point_b[2] - push_point[2]
                                  )

    # find joint 2 matrix

    joint_vect2_pos = (MPoint(push_point) + (vector_2_pushtarget * joint2_ratio))






    up_vector = bind_vector1 ^ bind_vector2
    up_vector = up_vector.normalize()

    point_list = []
    point_up_list = []
    point_matrix = []
    num_points = num_points
    for i in range(num_points):
        t = float(i) / (num_points - 1)  # Calculate parameter t

        # Calculate point on the curve
        result = quadratic_bezier_curve([vector_1_point_b ,joint_vect1_pos,push_point,joint_vect2_pos,vector_2_point_b], t)

        result_up = quadratic_bezier_curve(
            [MPoint(vector_1_point_b) + (up_vector * vector_1_b_mat_diff ),
             joint_vect1_pos + (up_vector * vector_1_a_mat_diff),
             MPoint(push_point) + (up_vector * vector_1_a_mat_diff),
             joint_vect2_pos + (up_vector * vector_2_a_mat_diff),
             MPoint(vector_2_point_b) + (up_vector * vector_2_b_mat_diff )],
            t)

        point_list.append(result)
        point_up_list.append(result_up)

    for i in range(num_points):
        if i != num_points-1:
            k = 1
        else:
            k = -1

        target_point = point_list[i + k]
        point = point_list[i]
        point_up = point_up_list[i]

        targetVector = MVector(target_point[0] - point[0],
                           target_point[1] - point[1],
                           target_point[2] - point[2])
        targetVector*= k
        temp_upVector = MVector(point_up[0] - point[0],
                           point_up[1] - point[1],
                           point_up[2] - point[2])

        targetVector = targetVector.normalize()
        temp_upVector = temp_upVector.normalize()

        side_vector = targetVector ^ temp_upVector
        upVector = side_vector ^ targetVector
        upVector = upVector.normalize()

        matrix = (targetVector[0],targetVector[1],targetVector[2],0,
                  upVector[0],upVector[1],upVector[2],0,
                  side_vector[0],side_vector[1],side_vector[2],0,
                  point[0],point[1],point[2],1)

        point_matrix.append(matrix)

    return {"points":point_matrix}
