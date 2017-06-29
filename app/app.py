import os
import io
import base64 as b64

from flask import Flask, render_template, g, jsonify, request, redirect
import pandas as pd
import settings
from random import choice
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import rcParams

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField

from bokeh.plotting import figure
from bokeh.embed import components

df = pd.read_csv(os.path.join(settings.data_dir, 'pop_by_country_long_form.csv'))
df['Year'] = df['Year'].str[4:].astype(int)
df2 = df.groupby(['Year', 'Nation']).sum().unstack()
df2.columns = df2.columns.droplevel()
nations = df2.columns
choices = list(zip(nations, nations))
images = ['mpl/' + nation for nation in df2.columns]
images = list(zip(images, images))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'


rcParams['lines.linewidth'] = 1
rcParams["font.family"] = "Tunga"
rcParams['font.size'] = 14
rcParams['axes.labelsize'] = 12
rcParams['xtick.labelsize'] = 12
rcParams['ytick.labelsize'] = 12
rcParams['font.size'] = 14
rcParams['figure.titlesize'] = 18
rcParams['axes.titlesize'] = 18
rcParams['legend.fontsize'] = 12
rcParams['figure.figsize'] = (8, 5)


class MyForm(FlaskForm):
    nation = SelectField('nation', choices=choices)

class MplForm(FlaskForm):
    nation = SelectField('nation', choices=images)

def hide_spines(ax, alpha=0.4):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_alpha(alpha)
    ax.spines['bottom'].set_alpha(alpha)

def fig_to_html(fig):
    """
    converts a matplotlib figure into an html image

    :param fig: matplotlibe figure object
    :returns: STR html string
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    img = ('data:image/png;base64,{}'
           .format(b64.b64encode(buf.getvalue()))
           .replace("b'",'')
           .replace("'",''))
    return img

@app.route('/')
def index():
    return redirect('/home')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/matplotlib', methods=['GET', 'POST'])
def matplotlib_plot():
    form = MyForm()
    head_scripts = render_template('chartist_head_scripts.html')
    body = render_template('matplotlib.html', form=form)
    scripts = render_template('matplotlib.js')
    return render_template('home.html',head_scripts=head_scripts, body=body, scripts=scripts)

@app.route('/bokeh', methods=['GET', 'POST'])
def bokeh_plot():
    form = MyForm()
    head_scripts = render_template('bokeh_head_scripts.html')
    body = render_template('bokeh.html', form=form)
    scripts = render_template('bokeh.js')
    return render_template('home.html',head_scripts=head_scripts, body=body, scripts=scripts)

@app.route('/chartist', methods=['GET', 'POST'])
def chartist():
    form = MyForm()
    head_scripts = render_template('chartist_head_scripts.html')
    body = render_template('chartist.html', form=form)
    scripts = render_template('chartist.js')
    return render_template('home.html', head_scripts=head_scripts, body=body, scripts=scripts)

@app.route('/c3', methods=['GET', 'POST'])
def c3_route():
    form = MyForm()
    head_scripts = render_template('c3_head_scripts.html')
    body = render_template('c3.html', form=form)
    scripts = render_template('c3_update.js')
    return render_template('home.html', head_scripts=head_scripts, body=body, scripts=scripts)

@app.route('/chartist1', methods=['GET', 'POST'])
def chartist1():
    form = MyForm()
    return render_template('chart.html', form=form)


@app.route('/data/<string:nation>')
def data(nation):
    data =  '{' + 'labels:{}, series: {}'.format(df2.index.astype(int).tolist(), df2[nation].astype(float).tolist()) + '}'
    return jsonify({'results':df2[nation].astype(float).tolist(), 'labels':df2.index.astype(float).tolist()})

@app.route('/mpl/<string:nation>')
def mpl(nation):
    fig, ax = plt.subplots()
    df2[nation].astype(float).plot(ax=ax, color='#D95D39', title=nation + ' population')
    hide_spines(ax)
    return jsonify({'src': fig_to_html(ax.figure)})

@app.route('/pybokeh/<string:nation>')
def pybokeh(nation):
    p = figure(title=nation, logo=None, tools="box_zoom,pan,wheel_zoom,reset",)
    p.line(x=df2[nation].index, y=df2[nation].values)
    script, div = components(p)
    return jsonify({'script': script,
                   'div': div})

@app.route('/c3data/<string:nation>')
def c3_daata_route(nation):

    data = {'columns':[[nation] + df2[nation].astype(float).tolist(), ['x'] + df2.index.astype(float).tolist()],
    'colors': {nation: '#4286f4'},
    'unload': "",}
    return jsonify(data)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)