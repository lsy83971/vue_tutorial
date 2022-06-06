import sys
import traceback
sys.path.append("/home/lsy/pyxmind")
from pyxmind import calcTree, result_parse
from pdform import pd2json, pd2str, beautify, abbrStr
import pandas as pd
import numpy as np
import uuid
import os
from copy import deepcopy
import ast
from flask import Flask, session
from flask import render_template_string, render_template
from flask import request
import json
app = Flask(__name__, template_folder='./',static_folder="",static_url_path="/")
app.config['SECRET_KEY'] = os.urandom(24)

# 任务是建立单机版的调试器
# simple way
# 一切从简单 但是预留扩展空间

def index():
    return render_template()


## app.add_url_rule("/", "init", init, methods=["GET", "POST"])
app.add_url_rule("/flask/loaddata", "loaddata", loaddata, methods=["GET", "POST"])
app.add_url_rule("/flask/tree", "tree", tree, methods=["GET", "POST"])
app.add_url_rule("/flask/code", "code", code, methods=["GET", "POST"])
app.add_url_rule("/flask/clear", "clear", clear, methods=["GET", "POST"])

app.add_url_rule("/flask/revert", "revert", revert, methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=True)
    #app.run(host="127.0.0.1", port=5005, debug=False)
