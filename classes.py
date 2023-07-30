# -*- coding: utf-8 -*-
import os
from datetime import datetime
from odbc_connect import get_table_data


class ScriptCreation:
    def __init__(self, historization=False, model_code='test', table_name='test_table'):
        self.historization = historization
        self.scripts = {}
        self.model_code = ''
        self.table_name = ''
        self.h_script = True
        self.i_script = True

    def load_data(self, model_code, table_name):
        self.model_code = model_code
        self.table_name = table_name
        self.definition_data = DataDefinition(model_code, table_name)

    def replace_names(self, text, data_dict):
        # add correct names
        for key, val in data_dict.items():
            if type(val) == list:
                pass
            else:
                text = text.replace(f'%{key}%', val)
        return text

    def create_head(self, script_type):
        # find end of head
        head_end = self.definition_data.templates_points[script_type]['head'][1]
        head = self.definition_data.templates[script_type][:head_end]
        # add correct names
        head = self.replace_names(head, self.definition_data.data_dict)

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

        return head

    def create_body(self, script_type):
        # find end of head
        body_start = self.definition_data.templates_points[script_type]['body'][0]
        body_end = self.definition_data.templates_points[script_type]['body'][1]
        body = self.definition_data.templates[script_type][body_start:body_end]

        # add correct names [debug]
        body = self.replace_names(body, self.definition_data.data_dict)

        return body

    def create_rest(self, script_type):
        remnant_start = self.definition_data.templates_points[script_type]['head'][1]
        remnant_end = self.definition_data.templates_points[script_type]['history'][0]
        remnant = self.definition_data.templates[script_type][remnant_start:remnant_end]

        # add correct names [debug]
        remnant = self.replace_names(remnant, self.definition_data.data_dict)

        return remnant

    def create_history(self, script_type):
        history_start = self.definition_data.templates_points[script_type]['history'][0]
        history_end = self.definition_data.templates_points[script_type]['history'][1]
        history = self.definition_data.templates[script_type][history_start:history_end]

        # add correct names [debug]
        history = self.replace_names(history, self.definition_data.data_dict)

        return history

    def create_script(self, script_type):
        script = ''
        script += self.create_head(script_type)
        script += self.create_rest(script_type)

        if self.h_script == True:
            if self.historization:
                script += self.create_history(script_type)

        script += self.create_body(script_type)

        # add correct names
        script = self.replace_names(script, self.definition_data.data_dict)

        return script

    def create_all_scripts(self):

        if self.h_script:
            self.scripts["h_script"] = self.create_script("h_script")
        if self.i_script:
            self.scripts["i_script"] = self.create_script("i_script")

    def save_scripts(self):

        if self.h_script == True:
            with open('test_h_script.txt', 'w', encoding='utf-8') as writer:
                writer.write(self.scripts["h_script"])

        if self.i_script == True:
            with open('test_i_script.txt', 'w', encoding='utf-8') as writer:
                writer.write(self.scripts["i_script"])

        return True


# %%
class DataDefinition:
    def __init__(self, model_code, table_name):
        self.model_code = model_code
        self.table_name = table_name

        # data dictionary
        self.data_dict = self.load_data_dict()

        # load script type
        self.templates = {}
        self.templates["h_script"] = self.load_template("h_template")
        self.templates["i_script"] = self.load_template("i_template")

        # template points
        self.templates_points = self.find_templates_points()

    def convert_to_text_list(self, dict_names):
        return ',\n'.join(dict_names)

    def load_data_dict(self):
        data_dict = {}
        data_dict['usname'] = os.getlogin().lower()
        # debug stuffs
        data_dict['scriptname'] = f'HD_{self.model_code}_{self.table_name}'
        data_dict['i_scriptname'] = f'ID_mpax_{self.table_name}'  # dodelat
        data_dict['database'] = self.model_code
        data_dict['aux_database'] = 'mp_aux'  # self.model_code + '_aux'
        data_dict['table_name'] = self.table_name
        data_dict['h_table_name'] = 'h_' + self.table_name
        data_dict['denne'] = 'daily'
        data_dict['repeat'] = 'N'
        data_dict['change_date'] = f"'{datetime.now().strftime('%Y-%m-%d')}'"
        data_dict['logon'] = 'logon_user_dodělat'
        data_dict['aux_logon'] = 'aux_logon_user_dodělat'

        # get pk & atr & src
        df = get_table_data(self.model_code, self.table_name)
        data_dict['pk_names'] = df.loc[df['Column_Primary_Key_Flag']
                                       == 'Y', 'Column_Code'].values.tolist()
        data_dict['atr_names'] = df.loc[df['Column_Primary_Key_Flag']
                                        == 'N', 'Column_Code'].values.tolist()
        data_dict['src_table_name'] = df['Source_Table'].unique()[0]
        data_dict['src_database'] = df['Source_Model'].unique()[0]

        # create aliases
        data_dict['table_alias'] = self.create_alias(data_dict['table_name'])
        data_dict['h_table_alias'] = self.create_alias(
            data_dict['h_table_name'])

        # create lists
        data_dict['pk_names_list'] = self.convert_to_text_list(
            data_dict['pk_names'])
        data_dict['atr_names_list'] = self.convert_to_text_list(
            data_dict['atr_names'])

        data_dict['at1_pk_names_list'] = self.convert_to_text_list(
            [f"  {data_dict['table_alias']}." + item for item in data_dict['pk_names']])
        data_dict['at1_atr_names_list'] = self.convert_to_text_list(
            [f"  {data_dict['table_alias']}." + item for item in data_dict['atr_names']])

        # historization stuffs
        data_dict['pk_names_list_where'] = self.create_pk_where_condition(
            data_dict['table_alias'], data_dict['h_table_alias'], data_dict['pk_names'])
        data_dict['historization_where'] = self.create_atr_where_condition(
            data_dict['table_alias'], data_dict['h_table_alias'], data_dict['atr_names'])

        return data_dict

    def create_custom_hist(self, atr):
        self.data_dict['historization_where'] = self.create_atr_where_condition(
            self.data_dict['table_alias'], self.data_dict['h_table_alias'], atr)

    def create_alias(self, table_name):
        return ''.join([item[0].lower() for item in table_name.split('_')]) + '1'

    def create_pk_where_condition(self, alias, h_alias, pk_names):
        condition = f" and {h_alias}.%pk_names% = {alias}.%pk_names%"

        result = ''

        if type(pk_names) == list:
            for val in pk_names:
                result += condition.replace('%pk_names%', val) + '\n'
            result = result[:-1]
        else:
            result += condition.replace('%pk_names%', pk_names) + '\n'

        return result

    def create_atr_where_condition(self, alias, h_alias, atr_names):
        condition = f"""(
        ({h_alias}.%atr_names% <> {alias}.%atr_names%)
         or
         (
          {alias}.%atr_names% is null
           and {h_alias}.%atr_names% is not null
         )
         or
         (
          {alias}.%atr_names% is not null
           and {h_alias}.%atr_names% is null
         )
        )"""

        result = ' and\n'
        if type(atr_names) == list:
            for val in atr_names:
                result += condition.replace('%atr_names%', val) + '\nor\n'
            result = result[:-3]
        else:
            result += condition.replace('%atr_names%', atr_names) + '\n'

        return result

    def load_template(self, name):
        with open(f'sql_templates/{name}.txt', 'r', encoding='utf-8') as f:
            # raw_template = f.readlines()
            template = f.read()
        return template

    def find_templates_points(self):
        templates = {}
        try:
            self.templates['h_script']
        # except AttributeError:
        except KeyError:
            pass
        else:
            txt = self.templates['h_script']
            tmp = {}
            tmp['head'] = [0, txt.find('.SET SESSION')]
            tmp['history'] = [txt.find(
                'exec o_dwh_DWH_Script_Instance_Ins'), txt.find('tabulky - END ****')+35]
            tmp['body'] = [tmp['history'][1], len(txt)]
            templates['h_script'] = tmp
        try:
            self.templates['i_script']
        except KeyError:
            pass
        else:
            txt = self.templates['i_script']
            tmp = {}
            tmp['head'] = [0, txt.find('.SET SESSION')]
            tmp['history'] = [txt.find(
                '/*************** Histor'), txt.find("Ins('%i_scriptname%');")+22]
            tmp['body'] = [tmp['history'][1]+1, len(txt)]
            templates['i_script'] = tmp

        return templates
