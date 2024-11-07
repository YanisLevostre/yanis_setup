import maya.cmds as cmds
import sys

sys.path.insert(0, 'C:/Users/Yanis/PycharmProjects/yanis_setup/')

from RigPipe.lib.constraint import multMatrix, parentMatrix, parentOffsetMatrix
from RigPipe.lib.spaceswitch import do_spaceswitch


class Module(object):
    inputs = {}

    def __init__(self, name):
        self.name = name
        self.attr = name + '_attribute_input'
        self.primaryAxis = name + '_primaryAxis_input'
        self.secondaryAxis = name + '_secondaryAxis_input'
        self.tertiaryAxis = name + '_tertiaryAxis_input'
        self.guide_grp = name + '_guide_grp'
        self.plug_grp = name + '_plugs_grp'
        self.data_grp = name + '_datas_grp'
        self.output_grp = name + '_output_grp'
        self.controlMatrix_orient = name + '_controlMatrix_input'
        self.control_group = name + '_control_grp'
        self.guideSetup_group = name + '_guideSetup_grp'
        self.primaryAxis_reverse = name + '_primaryAxis_reverse_input'
        self.secondaryAxis_reverse = name + '_secondaryAxis_reverse_input'
        self.tertiaryAxis_reverse = name + '_tertiaryAxis_reverse_input'
        self.setup_grp = name + '_setup_grp'
        self.control_grp = name + '_control_grp'
        self.bind_grp = name + '_bind_grp'


    def create_groups(self):
        master_group = cmds.group(em=True, n=self.name + '_rig_grp')
        for grp_name in ['guide', 'input', 'guideSetup', 'control', 'setup', 'bind', 'output']:
            grp = cmds.group(em=True, n='{}_{}_grp'.format(self.name, grp_name))
            cmds.parent(grp, master_group)
        for input_grp in ['datas', 'plugs']:
            grp = cmds.group(em=True, n='{}_{}_grp'.format(self.name, input_grp))
            cmds.parent(grp, '{}_input_grp'.format(self.name))
        for grps in ['primaryAxis', 'secondaryAxis', 'tertiaryAxis', 'controlMatrix','attribute']:
            grp = cmds.group(em=True, n='{}_{}_input'.format(self.name, grps))
            grp_reverse = cmds.group(em=True, n='{}_{}_reverse_input'.format(self.name, grps))
            cmds.parent(grp_reverse,grp, self.guide_grp)
            reverse = cmds.createNode('multiplyDivide',n = '{}_{}_reverse'.format(self.name, grps))
            cmds.connectAttr(grp+'.translate',reverse+'.input1')
            cmds.setAttr(reverse+'.input2',-1,-1,-1)
            cmds.connectAttr(reverse+'.output',grp_reverse+'.translate')


    def create_input(self,
                     name='Name',
                     plugs=False,
                     existingGuide=False,
                     space_switch_list=None,
                     pos=None,
                     rot=None,
                     matrix = None):
        if rot is None:
            rot = [0, 0, 0]
        if pos is None:
            pos = [0, 0, 0]
        if space_switch_list is None:
            space_switch_list = []
        if existingGuide:
            guide = existingGuide
        else:
            guide = cmds.spaceLocator(n=name + '_guide')[0]
            if matrix:
                cmds.xform(guide,ws = True, m = matrix)
            else:
                cmds.setAttr(guide + '.translate', pos[0], pos[1], pos[2])
                cmds.setAttr(guide + '.rotate', rot[0], rot[1], rot[2])
            cmds.parent(guide, self.guide_grp)

        transform = cmds.group(em=True, n=name + '_transform_input')
        cmds.parent(transform, self.data_grp)
        if space_switch_list:
            do_spaceswitch(module_name=self.name, guideList={guide: transform}, parent_list=space_switch_list,
                           node_name=name)
            plugInput = None
            plugOffset = None
        else:
            if plugs:
                plugInput = plugs['input']
                plugOffset = plugs['offset']
            else:
                plugInput = cmds.group(em=True, n=name + '_plugInput')
                plugOffset = cmds.group(em=True, n=name + '_plugOffset')
                cmds.parent(plugInput, self.plug_grp)
                cmds.parent(plugOffset, self.plug_grp)

            plug_loc = cmds.spaceLocator(n=name + '_plug_loc')[0]
            plug_matrix =cmds.xform(plugInput, ws = True, q = True, matrix = True)
            cmds.xform(plug_loc, ws = True,matrix = plug_matrix)
            cmds.parent(plug_loc, plugInput)
            multMatrix(target=plug_loc, source=guide, offset=plugOffset)
            parentMatrix(source=plug_loc, target=transform)

        self.inputs[name] = {'data': transform, 'plug': plugInput, 'offset': plugOffset, 'guide': guide}

    def create_output(self, name="name", node=None, offset_node=None):
        output = cmds.group(em=True, n=name + '_output')
        offset = cmds.group(em=True, n=name + '_offsetOutput')
        parentMatrix(source=node, target=output)
        parentMatrix(source=offset_node, target=offset)
        cmds.parent(output, offset, self.output_grp)

    def attach_chain_inputs(self, node_list=None, input_transform_list=None):
        parentOffsetMatrix(source=input_transform_list[0], target=node_list[0])
        for index in range(len(node_list) - 1):
            index += 1
            multMatrix(source=input_transform_list[index], offset=input_transform_list[index - 1],
                       target=node_list[index])

    def set_axis(self,primary = None,secondary = None,tertiary = None ,controlMatrix = None):
        if primary == None:
            primary = [0,0,0]
        if secondary == None:
            secondary = [0,0,0]
        if tertiary == None:
            tertiary = [0,0,0]
        if controlMatrix == None:
            controlMatrix = [1,1,1]
        cmds.setAttr(self.primaryAxis+'.translate',primary[0],primary[1],primary[2])
        cmds.setAttr(self.secondaryAxis + '.translate', secondary[0],secondary[1],secondary[2])
        cmds.setAttr(self.tertiaryAxis + '.translate', tertiary[0],tertiary[1],tertiary[2])
        cmds.setAttr(self.controlMatrix_orient + '.scale', controlMatrix[0],controlMatrix[1],controlMatrix[2])


