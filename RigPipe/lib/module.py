import maya.cmds as cmds
import ast
import os
import shutil
import datetime
import json

import json


class Module():


    inputs = {}
    outputs = {}
    controls = {}
    guides = {}
    attrs = {}
    def __init__(self,name):
        self.name = name

    @classmethod
    def scene_setup(cls):
        inputs_datas = cmds.getAttr('inputs.notes')
        Module.inputs =  ast.literal_eval(inputs_datas)
        outputs_datas = cmds.getAttr('outputs.notes')
        Module.outputs = ast.literal_eval(outputs_datas)
        controls_datas = cmds.getAttr('controls.notes')
        Module.controls = ast.literal_eval(controls_datas)
        guides_datas = cmds.getAttr('guides.notes')
        Module.guides = ast.literal_eval(guides_datas)
        attrs_datas = cmds.getAttr('attrs.notes')
        Module.attrs = ast.literal_eval(attrs_datas)

    #@classmethod
    #def add_item(cls,):




    def export_datas(self,file_path = 'D:/My Drive/rig/pipe/module/'):
        folder = file_path + self.name
        file = folder + '/'+self.name + '.ma'
        date_datas = datetime.datetime.now()
        date = (date_datas.strftime("%Y%m%d%H%M"))
        data_json =  folder + '/'+self.name + '.json'
        if os.path.isdir(folder):
            backup = folder + '/backup/'
            file_backup = backup + '/'+self.name + '.ma'
            if os.path.isdir(backup):
                os.mkdir(backup + date)
                shutil.move(file, backup + date + '/'+self.name + '.ma')
                shutil.move(data_json, backup + date + '/' + self.name + '.json')
            else:
                os.mkdir(backup)
                os.mkdir(backup + date)
                shutil.move(file, backup + date + '/'+self.name + '.ma')
                shutil.move(data_json, backup + date + '/' + self.name + '.json')
        else:
            os.mkdir(folder)

        datas = {'inputs':self.inputs,'outputs':self.outputs,'controls':self.controls,'guides':self.guides,'attrs':self.attrs}
        cmds.file(rename=file)
        cmds.file(save=True, type='mayaAscii', f = True)
        with open(data_json, 'w') as file_json:
            json.dump(datas, file_json)
        file_json.close()










