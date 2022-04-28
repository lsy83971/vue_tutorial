## 任务是建立单机版的调试器
## simple way
## 一切从简单 但是预留扩展空间

import sys
sys.path.append("/home/lsy/pyxmind")

from flask import Flask
from flask import render_template_string, render_template
from flask import request
import json
from pyxmind import calcTree

app = Flask(__name__, template_folder='./',static_folder="",static_url_path="/")

def run():
    return 'test'

def tree():
    data = json.loads(request.data)
    ct = calcTree().from_treeinfo(data)
    xmldata = {'a': 1, 'b': 2}
    res = {"err": "", "name": "", "data": xmldata}
    ct.nodes["root"].receive(res)
    print([i for i in ct.nodes["root"]. iter()])
    return json.dumps([i for i in ct.nodes["root"]. iter()])

## app.add_url_rule("/", "init", init, methods=["GET", "POST"])
app.add_url_rule("/flask/run", "run", run, methods=["GET", "POST"])
app.add_url_rule("/flask/tree", "tree", tree, methods=["GET", "POST"])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=True)
    #app.run(host="127.0.0.1", port=5005, debug=False)
