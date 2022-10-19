import sys
import traceback
import pandas as pd
import numpy as np
import uuid
import os
from copy import deepcopy
from flask_cors import CORS, cross_origin
import ast
from flask import Flask, session
from flask import render_template_string, render_template
from flask import request
import json
# 任务是建立单机版的调试器
# simple way
# 一切从简单 但是预留扩展空间
sys.path.append(os.getcwd())
os.chdir("../dist")
from run_server import loaddata, tree, code, clear, revert
from run_server_model_view import select, render



if __name__ == "__main__":
    def home():
        return render_template("index.html")
    
    app = Flask(__name__, template_folder='./',static_folder="./",static_url_path="")    
    app.config['SECRET_KEY'] = os.urandom(24)
    
    
    app.add_url_rule("/flask/loaddata", "loaddata", loaddata, methods=["POST"])
    app.add_url_rule("/flask/tree", "tree", tree, methods=["GET", "POST"])
    app.add_url_rule("/flask/code", "code", code, methods=["GET", "POST"])
    app.add_url_rule("/flask/clear", "clear", clear, methods=["GET", "POST"])
    app.add_url_rule("/flask/revert", "revert", revert, methods=["GET", "POST"])

    app.add_url_rule("/model/select", "select", select, methods=["GET", "POST"])
    app.add_url_rule("/model/render", "render", render, methods=["GET", "POST"])

    app.add_url_rule("/", "home", home, methods=["GET", "POST"])    
    app.run(host="127.0.0.1", port=17888, debug=True)
    #app.run(host="127.0.0.1", port=5005, debug=False)
