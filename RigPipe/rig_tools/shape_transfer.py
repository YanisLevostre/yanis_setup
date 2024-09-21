import maya.cmds as cmds
import maya.api.OpenMaya as om
import json

folder = 'C:/Users/Yanis/PycharmProjects/yanis_setup/datas/'
base_name = 'cartoon_hiRes'
eyeLids_joint_order = {'anchor': 4, 'L_upper': 0, 'L_lower': 1, 'R_upper': 2, 'R_lower': 3}


def init_shape_transfer(name=base_name,
                        folder=folder):
    """
    :param name: name of the preset for shapes
    :param folder: preset folder localisation
    :return:
    """
    # import data for topo model from Json
    with open(folder + name + '.json') as json_data:
        data = json.load(json_data)
        json_data.close()

    # set data from json
    vertex_exception = data['exception']
    lower_mouth = data['lowerMouth']
    l_upperlid = data['L_upperLid']
    l_lowerlid = data['L_lowerLid']
    r_upperlid = data['R_upperLid']
    r_lowerlid = data['R_lowerLid']
    shapes_list = data['shapeList']
    vertex_count_topology = data['vertexCount']

    # eyeLids index joint order need to create a cleaner option

    return {'vertex_exception': vertex_exception,
            'lower_mouth': lower_mouth,
            'l_upperlid': l_upperlid,
            'l_lowerlid': l_lowerlid,
            'r_upperlid': r_upperlid,
            'r_lowerlid': r_lowerlid,
            'shapes_list': shapes_list,
            'vertex_count_topology': vertex_count_topology,
            'data': data
            }


def shape_transfer(target_topo_mesh=None,
                   target_mesh=None,
                   target_side_mesh=None,
                   target_mouth_mesh=None,
                   target_eyelids_mesh=None,
                   eyelids_joint_order=None,
                   base_topology_datas=init_shape_transfer(),
                   smooth=5,
                   normalize=False,
                   ):
    """
    :param target_topo_mesh: mesh target shape with matching topology
    :type target_topo_mesh: basestring
    :param target_mesh: mesh target
    :type target_mesh: basestring
    :param target_side_mesh: mesh target with skinCluster painted L/R sides
    :type target_side_mesh: basestring
    :param target_mouth_mesh: mesh target with skinCluster painted Upper Lower mouth
    :type target_mouth_mesh: basestring
    :param target_eyelids_mesh: mesh target with skinCluster painted L/R and Up/Down eyeLids
    :type target_eyelids_mesh: basestring
    :param eyelids_joint_order: a dictionary with joint eyeLids skinCluster  {influence:index}
    :type eyelids_joint_order: dict
    :param smooth: a parameter how many vertices around it takes to match topoMesh to wrap target Mesh
    :type smooth: int
    :param base_topology_datas: all datas from topology mesh imported for transfer
    :type base_topology_datas: dict
    :return: None
    """
    print(base_topology_datas)
    # get datas from base_topology_datas
    vertex_exception = base_topology_datas['vertex_exception']
    lower_mouth = base_topology_datas['lower_mouth']
    l_upperlid = base_topology_datas['l_upperlid']
    l_lowerlid = base_topology_datas['l_lowerlid']
    r_upperlid = base_topology_datas['r_upperlid']
    r_lowerlid = base_topology_datas['r_lowerlid']
    shapes_list = base_topology_datas['shapes_list']
    vertex_count_topology = base_topology_datas['vertex_count_topology']
    data = base_topology_datas['data']

    # get target mesh vertex count
    target_vertex_count = cmds.polyEvaluate(target_mesh, v=True)

    # define all skinClusters
    side_skinCluster = mel.eval('findRelatedSkinCluster ' + target_side_mesh)
    mouth_skinCluster = mel.eval('findRelatedSkinCluster ' + target_mouth_mesh)
    eyeLid_skinCluster = mel.eval('findRelatedSkinCluster ' + target_eyelids_mesh)

    target_vertex_bind = {}

    # this loop go through each vertex from target mesh
    for target_mesh_vtx in range(target_vertex_count):
        # get position for x vertex
        target_mesh_vtx_pos = cmds.xform('{}.vtx[{}]'.format(target_mesh, target_mesh_vtx), ws=True, t=True, q=True)
        # this dict will contain every topoMesh to target mesh distance
        distance_list = {}
        # this go through all vertex topo mesh compare the distance for the specific target mesh and put it in distance
        # dict
        for target_topo_mesh_vtx in range(vertex_count_topology):
            target_topo_mesh_vtx_pos = cmds.xform('{}.vtx[{}]'.format(target_topo_mesh, target_topo_mesh_vtx), ws=True,
                                                  t=True, q=True)
            vector = om.MVector(target_topo_mesh_vtx_pos[0] - target_mesh_vtx_pos[0],
                                target_topo_mesh_vtx_pos[1] - target_mesh_vtx_pos[1],
                                target_topo_mesh_vtx_pos[2] - target_mesh_vtx_pos[2])
            distance_list[vector.length()] = target_topo_mesh_vtx

        # sorted distance dict to only have closest first
        sorted_distance = sorted(distance_list)
        inf_short_list = sorted_distance[:smooth]
        target_vertex_bind[target_mesh_vtx] = {}

        for influence in inf_short_list:
            target_vertex_bind[target_mesh_vtx][distance_list[influence]] = inf_short_list[-1] - influence

    for shape in shapes_list:
        # get ref vertex

        vertex_pos = {}
        ref_vertex_dict = {}
        vertex_scale_list = []
        source_matrix_list = {}
        target_matrix_list = {}
        deformed_shape = {}

        # get target_mesh binding
        for shape_vtx_id in range(vertex_count_topology):
            distance_dict = {}
            shape_vtx_pos = data[shape][str(shape_vtx_id)]
            temp_source_vtx_pos = data['baseMesh'][str(shape_vtx_id)]
            if shape_vtx_pos != temp_source_vtx_pos:
                for source_vtx_id in range(vertex_count_topology):
                    if source_vtx_id not in vertex_exception:
                        source_vtx_pos = data['baseMesh'][str(source_vtx_id)]
                        vector = om.MVector(source_vtx_pos[0] - shape_vtx_pos[0],
                                            source_vtx_pos[1] - shape_vtx_pos[1],
                                            source_vtx_pos[2] - shape_vtx_pos[2])

                        distance = vector.length()
                        distance_dict[distance] = source_vtx_id

                if shape_vtx_id in vertex_exception:
                    for id in vertex_exception:
                        if id in distance_dict:
                            del distance_dict[id]

                sorted_distance = sorted(distance_dict)
                if shape_vtx_id != distance_dict[sorted_distance[0]]:
                    ref_vertex_dict[shape_vtx_id] = distance_dict[sorted_distance[0]]
                else:
                    ref_vertex_dict[shape_vtx_id] = distance_dict[sorted_distance[1]]
                # get source matrix direction

                source_vtx_pos = data['baseMesh'][str(shape_vtx_id)]
                source_ref_vtx_pos = data['baseMesh'][str(ref_vertex_dict[shape_vtx_id])]

                vector_primary = om.MVector(source_ref_vtx_pos[0] - source_vtx_pos[0],
                                            source_ref_vtx_pos[1] - source_vtx_pos[1],
                                            source_ref_vtx_pos[2] - source_vtx_pos[2])
                source_size = vector_primary.length()

                vector_up = om.MVector(0, 1, 1)
                vector_secondary = vector_primary ^ vector_up
                vector_tertiary = vector_primary ^ vector_secondary
                if normalize:
                    vector_primary = vector_primary.normalize()
                    vector_secondary = vector_secondary.normalize()
                    vector_tertiary = vector_tertiary.normalize()

                source_matrix = om.MMatrix(((vector_primary.x, vector_primary.y, vector_primary.z, 0),
                                            (vector_secondary.x, vector_secondary.y, vector_secondary.z, 0),
                                            (vector_tertiary.x, vector_tertiary.y, vector_tertiary.z, 0),
                                            (source_vtx_pos[0], source_vtx_pos[1], source_vtx_pos[2], 1)
                                            ))
                # get target matrix direction

                target_vtx_pos = cmds.xform('{}.vtx[{}]'.format(target_topo_mesh, shape_vtx_id), q=True, ws=True,
                                            t=True)
                target_ref_vtx_pos = cmds.xform('{}.vtx[{}]'.format(target_topo_mesh, ref_vertex_dict[shape_vtx_id]),
                                                q=True,
                                                ws=True, t=True)

                vector_primary = om.MVector(target_ref_vtx_pos[0] - target_vtx_pos[0],
                                            target_ref_vtx_pos[1] - target_vtx_pos[1],
                                            target_ref_vtx_pos[2] - target_vtx_pos[2])
                target_size = vector_primary.length()

                vector_up = om.MVector(0, 1, 1)
                vector_secondary = vector_primary ^ vector_up
                vector_tertiary = vector_primary ^ vector_secondary

                if normalize:
                    vector_primary = vector_primary.normalize()
                    vector_secondary = vector_secondary.normalize()
                    vector_tertiary = vector_tertiary.normalize()

                target_matrix = om.MMatrix(((vector_primary.x, vector_primary.y, vector_primary.z, 0),
                                            (vector_secondary.x, vector_secondary.y, vector_secondary.z, 0),
                                            (vector_tertiary.x, vector_tertiary.y, vector_tertiary.z, 0),
                                            (target_vtx_pos[0], target_vtx_pos[1], target_vtx_pos[2], 1)
                                            ))
                source_matrix_list[shape_vtx_id] = source_matrix
                target_matrix_list[shape_vtx_id] = target_matrix

                # get new shape point
                scale = target_size / source_size
                vertex_scale_list.append(scale)

        for shape_vtx_id in range(vertex_count_topology):
            if shape_vtx_id in source_matrix_list:
                shape_vtx_pos = data[shape][str(shape_vtx_id)]
                source_matrix = source_matrix_list[shape_vtx_id]
                target_matrix = target_matrix_list[shape_vtx_id]
                scale = sum(vertex_scale_list) / len(vertex_scale_list)
                # scale = 1
                shape_point_matrix = om.MMatrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0),
                                                 (shape_vtx_pos[0], shape_vtx_pos[1], shape_vtx_pos[2], 1)))
                scale_matrix = om.MMatrix(((scale, 0, 0, 0), (0, scale, 0, 0), (0, 0, scale, 0), (0, 0, 0, 1)))
                inverted_source_matrix = source_matrix.inverse()
                shape_deplacement = shape_point_matrix * inverted_source_matrix
                scaled_shape = shape_deplacement * scale_matrix
                new_point = scaled_shape * target_matrix
                vertex_pos[shape_vtx_id] = (
                    new_point.getElement(3, 0), new_point.getElement(3, 1), new_point.getElement(3, 2))

        L_shape = None
        R_shape = None
        C_shape = None
        shapes_to_build = []
        if shape.split('_')[0] == 'side':
            name = shape.replace('side_', 'L_')
            L_shape = cmds.duplicate(target_mesh, n=name + '_transfered')[0]
            shapes_to_build.append(L_shape)
            name = shape.replace('side_', 'R_')
            R_shape = cmds.duplicate(target_mesh, n=name + '_transfered')[0]
            shapes_to_build.append(R_shape)
        else:
            C_shape = cmds.duplicate(target_mesh, n=shape + '_transfered')[0]
            shapes_to_build.append(C_shape)

        for vtx in range(target_vertex_count):
            target_mesh_vtx_pos = cmds.xform('{}.vtx[{}]'.format(target_mesh, vtx), ws=True, t=True, q=True)

            for new_shape in shapes_to_build:
                inf_dict = {}
                inf_list = []
                inf_mouth_dict = {}
                inf_eyeLid_dict = {}
                x = target_mesh_vtx_pos[0]
                y = target_mesh_vtx_pos[1]
                z = target_mesh_vtx_pos[2]
                if new_shape.split('_')[0] == 'L':
                    inf_side = \
                        cmds.skinPercent(side_skinCluster, '{}.vtx[{}]'.format(target_side_mesh, vtx), query=True,
                                         value=True)[1]
                elif new_shape.split('_')[0] == 'R':
                    inf_side = \
                        cmds.skinPercent(side_skinCluster, '{}.vtx[{}]'.format(target_side_mesh, vtx), query=True,
                                         value=True)[0]

                else:
                    inf_side = 1

                for topo_vtx in target_vertex_bind[vtx]:
                    if topo_vtx in vertex_pos:
                        if topo_vtx in lower_mouth:
                            inf_mouth = \
                                cmds.skinPercent(mouth_skinCluster, '{}.vtx[{}]'.format(target_mouth_mesh, vtx),
                                                 query=True,
                                                 value=True)[1]
                        else:
                            inf_mouth = \
                                cmds.skinPercent(mouth_skinCluster, '{}.vtx[{}]'.format(target_mouth_mesh, vtx),
                                                 query=True,
                                                 value=True)[0]
                        inf_eyeLid = 0
                        if topo_vtx in l_upperlid:
                            inf_eyeLid += \
                                cmds.skinPercent(eyeLid_skinCluster, '{}.vtx[{}]'.format(target_eyelids_mesh, vtx),
                                                 query=True, value=True)[eyelids_joint_order['L_upper']]
                        if topo_vtx in l_lowerlid:
                            inf_eyeLid += \
                                cmds.skinPercent(eyeLid_skinCluster, '{}.vtx[{}]'.format(target_eyelids_mesh, vtx),
                                                 query=True, value=True)[eyelids_joint_order['L_lower']]
                        if topo_vtx in r_upperlid:
                            inf_eyeLid += \
                                cmds.skinPercent(eyeLid_skinCluster, '{}.vtx[{}]'.format(target_eyelids_mesh, vtx),
                                                 query=True, value=True)[eyelids_joint_order['R_upper']]
                        if topo_vtx in r_lowerlid:
                            inf_eyeLid += \
                                cmds.skinPercent(eyeLid_skinCluster, '{}.vtx[{}]'.format(target_eyelids_mesh, vtx),
                                                 query=True, value=True)[eyelids_joint_order['R_lower']]
                        if topo_vtx not in l_upperlid + l_lowerlid + r_upperlid + r_lowerlid:
                            inf_eyeLid = 1

                        if inf_side * inf_mouth * inf_eyeLid != 0:
                            inf_mouth_dict[topo_vtx] = inf_mouth
                            inf_eyeLid_dict[topo_vtx] = inf_eyeLid
                            inf_dict[topo_vtx] = target_vertex_bind[vtx][topo_vtx]
                            inf_list.append(target_vertex_bind[vtx][topo_vtx])

                if inf_dict != {}:
                    if len(inf_list) != 1:
                        sum_inf = sum(inf_list)
                        for topo_vtx in inf_dict:
                            inf_transfer = inf_dict[topo_vtx] / sum_inf
                            inf_mouth = inf_mouth_dict[topo_vtx]
                            inf_eyeLid = inf_eyeLid_dict[topo_vtx]
                            base = cmds.xform('{}.vtx[{}]'.format(target_topo_mesh, topo_vtx), ws=True, t=True, q=True)
                            target = vertex_pos[topo_vtx]
                            x += (target[0] - base[0]) * inf_transfer * inf_side * inf_mouth * inf_eyeLid
                            y += (target[1] - base[1]) * inf_transfer * inf_side * inf_mouth * inf_eyeLid
                            z += (target[2] - base[2]) * inf_transfer * inf_side * inf_mouth * inf_eyeLid
                    else:
                        for topo_vtx in inf_dict:
                            inf_transfer = 1
                            inf_mouth = inf_mouth_dict[topo_vtx]
                            inf_eyeLid = inf_eyeLid_dict[topo_vtx]
                            base = cmds.xform('{}.vtx[{}]'.format(target_topo_mesh, topo_vtx), ws=True, t=True, q=True)
                            target = vertex_pos[topo_vtx]
                            x += (target[0] - base[0]) * inf_transfer * inf_side * inf_mouth * inf_eyeLid
                            y += (target[1] - base[1]) * inf_transfer * inf_side * inf_mouth * inf_eyeLid
                            z += (target[2] - base[2]) * inf_transfer * inf_side * inf_mouth * inf_eyeLid

                # deformed_shape[vtx] = vertex_pos[vtx]
                cmds.xform('{}.vtx[{}]'.format(new_shape, vtx), ws=True, t=(x, y, z))


shape_transfer(target_topo_mesh='head_ref_topo3',
               target_mesh='_kevin',
               target_side_mesh='kevin_sides',
               target_mouth_mesh='kevin_mouth',
               target_eyelids_mesh='kevin_eyeLid',
               eyelids_joint_order=eyeLids_joint_order,
               base_topology_datas=init_shape_transfer(),
               smooth=12,
               normalize=True
               )
