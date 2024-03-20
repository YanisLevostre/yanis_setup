import maya.cmds as cmds
from maya.api.OpenMaya import MVector
import math
#####

#####

# datas
# temp maya import datas
vector_1_point_a = cmds.getAttr('locator1.translate')[0]
vector_1_point_b = cmds.getAttr('locator2.translate')[0]
vector_2_point_a = cmds.getAttr('locator3.translate')[0]
vector_2_point_b = cmds.getAttr('locator4.translate')[0]
# vector 1
#vector_1_point_a = (0, 0, -2)
#vector_1_point_b = (-6, 0, -2)
vector1 = MVector(vector_1_point_b[0] - vector_1_point_a[0],
                  vector_1_point_b[1] - vector_1_point_a[1],
                  vector_1_point_b[2] - vector_1_point_a[2]
                  )
# vector 2
#vector_2_point_a = (1.904, 0, -0.613)
#vector_2_point_b = (3.436, 0, 4.146)
vector2 = MVector(vector_2_point_b[0] - vector_2_point_a[0],
                  vector_2_point_b[1] - vector_2_point_a[1],
                  vector_2_point_b[2] - vector_2_point_a[2]
                  )

# vector mid dir vec1
vector_mid_dir1 = MVector(vector_1_point_a[0] - vector_2_point_a[0],
                          vector_1_point_a[1] - vector_2_point_a[1],
                          vector_1_point_a[2] - vector_2_point_a[2]
                          )
# vector mid dir vec1
vector_mid_dir2 = MVector(vector_2_point_a[0] - vector_1_point_a[0],
                          vector_2_point_a[1] - vector_1_point_a[1],
                          vector_2_point_a[2] - vector_1_point_a[2]
                          )
mid_legth = vector_mid_dir1.length()

if vector_mid_dir1.length() != 0:
    # vec1_vec2 angle
    vec1_vec2_cos = vector1.normalize() * vector2.normalize()
    vec1_vec2_angle = math.acos(abs(vec1_vec2_cos))
    print('vec1_vec2 angle: {}'.format(math.degrees(vec1_vec2_angle)))

    # vec1_vecMid angle
    vec1_vecMid_cos = vector1.normalize() * vector_mid_dir1.normalize()
    vec1_vecMid_angle =math.acos(abs(vec1_vecMid_cos))
    print('vec1_vecMid angle: {}'.format(math.degrees(vec1_vecMid_angle)))

    # vec2_vecMid angle
    vec2_vecMid_cos = vector2.normalize() * vector_mid_dir2.normalize()
    vec2_vecMid_angle = math.acos(abs(vec2_vecMid_cos))
    print('vec2_vecMid angle: {}'.format(math.degrees(vec2_vecMid_angle)))


    if math.sin(vec1_vec2_angle) != 0:
        rapport_sinus = (mid_legth / 2.00)/math.sin((math.pi+vec1_vec2_angle)/2.00)
        push_legth = rapport_sinus * math.sin(vec1_vecMid_angle)
        print(push_legth)

    else:
        print('flat angle')
        push_legth = 0



else:
    print('bindPose')
    push_legth = 0

cmds.setAttr('locator6.tz',push_legth)