# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 16:34:18 2023

@author: nnif
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from classes import ScriptCreation


# %%
# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'TopSecret'

# create main data scripts
scripts = ScriptCreation()

# Global HTML template variables.


@app.context_processor
def set_global_html_variable_values():
    template_config = {'model_code': scripts.model_code,
                       'table_name': scripts.table_name}
    return template_config

# create a route decorator


@app.route('/', methods=['GET', 'POST'])
def index():
    scripts.table_name = ''
    scripts.model_code = ''
    if request.method == 'POST':
        model_code = request.form.get("database_name")
        table_name = request.form.get("table_name")
        scripts.load_data(model_code=model_code, table_name=table_name)
        return redirect(url_for("script_config"))
    return render_template("index.html")


@app.route('/script/config', methods=['GET', 'POST'])
def script_config():
    if request.method == 'POST':
        scripts.definition_data.data_dict["sel_atr"] = request.form.getlist(
            "attributes")
        if scripts.definition_data.data_dict["sel_atr"] != scripts.definition_data.data_dict["atr_names"]:
            scripts.definition_data.create_custom_hist(
                scripts.definition_data.data_dict["sel_atr"])
            # print('not equal')
        scripts.historization = True if request.form.get(
            "historization") is not None else False
        scripts.h_script = True if request.form.get(
            "h_script") is not None else False
        scripts.i_script = True if request.form.get(
            "i_script") is not None else False
        scripts.create_all_scripts()
        return redirect(url_for("script_result"))

    return render_template("script_config.html", attributes=scripts.definition_data.data_dict["atr_names"])


@app.route('/script/result', methods=['GET', 'POST'])
def script_result():
    if request.method == 'POST':
        if scripts.save_scripts():
            flash("Script saved")
        else:
            flash("Error during saving...")
    return render_template('result.html', attributes=scripts.definition_data.data_dict["sel_atr"],  historization=scripts.historization, h_script=scripts.h_script, i_script=scripts.i_script)
