# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 16:34:18 2023

@author: nnif
"""

import regex
from datetime import datetime

# read template file
with open('h_template.txt') as f:
    # raw_template = f.readlines()
    test = f.read()


def create_head(definition_data, script_type='history'):

    # find end of head
    head_end = definition_data.templates_point[script_type]['head'][1]
    head = definition_data.templates[script_type][:head_end]
    # add correct names

    for key, val in definition_data.data_dict.items():
        if type(val) == list:
            pass
        else:
            head = head.replace(f'%{key}%', val)

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


    # save result
with open('script.txt', 'w') as f:
    f.writelines(head)


class DataDefinition:
    def __init__(self, script_type="H", usname='dburiane'):
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

        # load script type
        self.templates = {}
        if 'H' in script_type:
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


definition_data = DataDefinition()


x = create_head(definition_data)
# %%
data_dict = {'scriptname': 'HD_TEST_SCRIPT', 'database': 'mp', 'table_name': 'test_table',
             'repeat': 'N', 'usname': 'dburiane', 'change_date': '2023-02-20'}
# %%
"""
    %historization_field_list%
    or %mandatory_field_check_list

"""
