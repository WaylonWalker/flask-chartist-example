import os
from flask import Flask, render_template, g, jsonify, request
import pandas as pd
import settings
from random import choice

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField


df = pd.read_csv(os.path.join(settings.data_dir, 'pop_by_country_long_form.csv'))
df['Year'] = df['Year'].str[4:].astype(int)
df2 = df.groupby(['Year', 'Nation']).sum().unstack()
df2.columns = df2.columns.droplevel()
nations = df2.columns
choices = zip(nations, nations)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

class MyForm(FlaskForm):
    nation = SelectField('nation', choices=choices)




@app.route('/', methods=['GET', 'POST'])
def index():
    global nations
    form = MyForm()
    return render_template('chart.html', form=form)


@app.route('/data/<string:nation>')
def data(nation):
    data =  '{' + 'labels:{}, series: {}'.format(df2.index.astype(int).tolist(), df2[nation].astype(float).tolist()) + '}'
    return jsonify({'results':df2[nation].astype(float).tolist(), 'labels':df2.index.astype(float).tolist()})

if __name__ == '__main__':
    app.run(debug=True)