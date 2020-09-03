from flask import Flask, render_template, request

import plotly
import plotly.graph_objs as go
import plotly.offline as po
import plotly.express as px

import pandas as pd
import numpy as np
import json

from market import day
from market import chart2

import time

app = Flask(__name__)
@app.route('/stock', methods=['GET', 'POST'])
def change_features():
    start = time.time()
    code = request.args.get('code', " ")
    chart2.print_chart(code)
    print("total time :", time.time() - start)
    return render_template('stock.html')

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/first")
def hello_first():
    return "<h3>Hello First</h3>"



if __name__ == "__main__":              
    app.run(host="0.0.0.0", port="3000", debug=True)