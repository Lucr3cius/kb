# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 16:34:18 2023

@author: nnif
"""

import regex
from datetime import datetime
       


def replace_names(text, data_dict):
    # add correct names
    for key, val in data_dict.items():
        if type(val) == list:
            pass
        else:
            text = text.replace(f'%{key}%', val)
    return text


def create_head(definition_data, script_type='history'):

    # find end of head
    head_end = definition_data.templates_point[script_type]['head'][1]
    head = definition_data.templates[script_type][:head_end]
    # add correct names
    head = replace_names(head, definition_data.data_dict)

    # unified len
    tmp = head.splitlines()
    head = ''
    for line in tmp:
        lenght = len(line)
        if lenght > 100:
            head = ''.join([head, line[:98], '*/\n'])
        elif lenght < 100:
            head = ''.join([head, line[:lenght-2].ljust(98, ' '), '*/\n'])
        else:
            head = ''.join([head, line, '\n'])
            # ''.join(line[:lenght-1]

    return head


def create_history(text, data_dict):
    test = text


def create_body(text, data_dict):
    body_start = definition_data.templates_point[script_type]['body'][0]
    body_end = definition_data.templates_point[script_type]['body'][1]
    body = definition_data.templates[script_type][body_start:body_end]
    # add correct names
    body = replace_names(body, definition_data.data_dict)

    return body


def convert_to_list(dict_names):
    text = ',\n'.join(dict_names)


#dict_names = definition_data.data_dict["pk_names"]
# save result
with open('script.txt', 'w') as f:
    f.writelines(head)

# %%


class ScriptCreation:
    def __init__(self, script_type='history', historization=False):
        self.script_type = script_type
        self.historization = historization
        self.definition_data = DataDefinition(script_type)
        self.script = ''

    def replace_names(self, text, data_dict):
        # add correct names
        for key, val in data_dict.items():
            if type(val) == list:
                pass
            else:
                text = text.replace(f'%{key}%', val)
        return text

    def create_head(self):
        # find end of head
        head_end = self.definition_data.templates_point[self.script_type]['head'][1]
        head = self.definition_data.templates[self.script_type][:head_end]
        # add correct names
        head = replace_names(head, self.definition_data.data_dict)

        # unified len
        tmp = head.splitlines()
        head = ''
        for line in tmp:
            lenght = len(line)
            if lenght > 100:
                head = ''.join([head, line[:98], '*/\n'])
            elif lenght < 100:
                head = ''.join([head, line[:lenght-2].ljust(98, ' '), '*/\n'])
            else:
                head = ''.join([head, line, '\n'])
                # ''.join(line[:lenght-1]

        return head

    def create_history(self):
        pass

    def create_body(self):
        # find end of head
        body_start = self.definition_data.templates_point[self.script_type]['body'][0]
        body_end = self.definition_data.templates_point[self.script_type]['body'][1]
        body = self.definition_data.templates[self.script_type][body_start:body_end]
        # add correct names
        body = replace_names(body, self.definition_data.data_dict)

        return body

    def create_rest(self):
        pass

    def create_script(self):
        script = ''
        script += self.create_head()
        script += self.create_rest()

        if self.historization:
            script += self.create_history()

        script += self.create_body()


# %%
class DataDefinition:
    def __init__(self, script_type="history", usname='dburiane'):
        self.script_type = script_type
        # data dictionary
        self.data_dict = {}
        self.data_dict['usname'] = usname
        self.data_dict['scriptname'] = 'HD_TEST_SCRIPT'
        self.data_dict['database'] = 'mp'
        self.data_dict['table_name'] = 'test_table'
        self.data_dict['denne'] = 'daily'
        self.data_dict['repeat'] = 'N'
        self.data_dict['change_date'] = f"'{datetime.now().strftime('%Y-%m-%d')}'"
        self.data_dict['pk_names'] = ['pk1', 'pk2']
        self.data_dict['atr_names'] = ['atr1', 'atr2', 'atr3']
        self.data_dict['aux_database'] = 'aux_database'

        # create lists
        self.data_dict['pk_names_list'] = self.convert_to_list(
            self.data_dict['pk_names'])
        self.data_dict['atr_names_list'] = self.convert_to_list(
            self.data_dict['atr_names'])

        # load script type
        self.templates = {}
        if 'history' in script_type:
            self.templates['history'] = self.load_template("h_template")
        if 'I' in script_type:
            self.templates['increment'] = self.load_template("i_template")

        # template points
        self.templates_point = self.find_template_points()

    def load_template(self, name):
        with open(f'{name}.txt') as f:
            # raw_template = f.readlines()
            template = f.read()
        return template

    def convert_to_list(self, dict_names):
        text = ',\n'.join(dict_names)

        return text

    def find_template_points(self):
        templates = {}
        try:
            self.templates['history']
        # except AttributeError:
        except KeyError:
            print("error")
        else:
            txt = self.templates['history']
            tmp = {}
            tmp['head'] = [0, txt.find('.SET SESSION')]
            tmp['history'] = [txt.find(
                '/*************** HISTOR'), txt.find('TABLE - END ****')+29]
            tmp['body'] = [tmp['history'][1], len(txt)]
            templates['history'] = tmp
        try:
            self.templates['increment']
        except KeyError:
            pass
        else:
            txt = self.templates['increment']
            tmp = {}
            tmp['head'] = [0, txt.find('.SET SESSION')]
            tmp['history'] = [txt.find(
                '/*************** HISTOR'), txt.find('TABLE - END ****')+29]
            tmp['body'] = [tmp['history'][1]+1, len(txt)]
            templates['increment'] = tmp

        return templates

# %%


definition_data = DataDefinition()
y = definition_data.templates_point


x += create_head(definition_data)
# %%
data_dict = {'scriptname': 'HD_TEST_SCRIPT', 'database': 'mp', 'table_name': 'test_table',
             'repeat': 'N', 'usname': 'dburiane', 'change_date': '2023-02-20'}
# %%
"""
    %historization_field_list%
    or %mandatory_field_check_list

"""
# read template file
with open('h_template.txt') as f:
    # raw_template = f.readlines()
    test = f.read()

