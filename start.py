from flask import Flask, render_template, request, redirect, url_for, flash
import time
#%%

class TestDefinition:
    def __init__(self) -> None:
        self.attributes = ['pk1', 'pk2', 'atr1', 'atr2', 'atr3']
        self.database_name = "mp"
        self.table_name = "test_table"
        self.sel_attr=[]
        self.historization=True
        self.h_script = True
        self.i_script = True

def fake_connection():
    time.sleep(2)
    return True

def save_file():
    time.sleep(2)
    print("saving file")
    return True
#%%
# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'TopSecret'
# create a route decorator
data = TestDefinition()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data.database_name = request.form.get("database_name")
        data.table_name = request.form.get("table_name")
        if fake_connection() == True:
            return redirect(url_for("script_config"))
    return render_template("index.html")

@app.route('/user/<name>', methods=['GET', 'POST'])
def user():
    attributes = ['pk1', 'pk2', 'atr1', 'atr2', 'atr3']
    if request.method == 'POST':
        selected_list = request.form.getlist("test")
    return render_template("user.html", attributes=attributes)

@app.route('/database_connection', methods=['GET', 'POST'])
def connecting_dabase():
    if request.method == 'POST':
        data.database_name = request.form.get("database_name")
        data.table_name = request.form.get("table_name")
        if fake_connection() == True:
            return redirect(url_for("script_config"))
    return render_template("database_connection.html", database_name=data.database_name, table_name=data.table_name)


@app.route('/script/config', methods=['GET', 'POST'])
def script_config():
    if request.method == 'POST':
        data.database_name = request.form.get("database_name")
        data.table_name = request.form.get("table_name")
        data.sel_attr = request.form.getlist("attributes")
        data.historization = True if request.form.get("historization") is not None else False
        data.h_script = True if request.form.get("h_script") is not None else False
        data.i_script = True if request.form.get("i_script") is not None else False

        return redirect(url_for("script_result"))
    return render_template("script_config.html", attributes=data.attributes, historization=data.historization, h_script=data.h_script, i_script=data.i_script)

@app.route('/script/result', methods=['GET', 'POST'])
def script_result():
    if request.method == 'POST':
        save_file()
        flash("Scripts saved")
    return render_template('result.html', attributes=data.sel_attr, historization=data.historization, h_script=data.h_script, i_script=data.i_script)

