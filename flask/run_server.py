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

load_file = {
    "name": "None", 
    "text": "",
    "json": dict(), 
}

def loaddata():
    data = json.loads(request.data)
    load_file["json"] = data
    print(data)
    return "load json data success!"

def tree():
    data = json.loads(request.data)
    ct = calcTree().from_treeinfo(data)
    res = {"err": "", "name": "", "data": xmldata}
    ct.nodes["root"].receive(res)
    ##print([i for i in ct.nodes["root"]. iter()])
    res = [i for i in ct.nodes["root"]. iter()]
    node_res = {i:j.stack for i, j in ct.nodes.items()}
    tr = {"res": res, "node_res": node_res}
    return json.dumps(tr)

## app.add_url_rule("/", "init", init, methods=["GET", "POST"])
app.add_url_rule("/flask/loaddata", "loaddata", loaddata, methods=["GET", "POST"])
app.add_url_rule("/flask/tree", "tree", tree, methods=["GET", "POST"])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=True)
    #app.run(host="127.0.0.1", port=5005, debug=False)
