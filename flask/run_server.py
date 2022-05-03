# 任务是建立单机版的调试器
# simple way
# 一切从简单 但是预留扩展空间
import sys
sys.path.append("/home/lsy/pyxmind")
from flask import Flask
from flask import render_template_string, render_template
from flask import request
import json
app = Flask(__name__, template_folder='./',static_folder="",static_url_path="/")


from pyxmind import calcTree
from pdform import pd2json, pd2str
import pandas as pd
import numpy as np

def beautify(x):
    print(type(x))
    res = dict()
    res["raw_data"] = pd2str(x)
    if isinstance(x, dict):
        res["b_data"] = f"<dict>:\n{list(x.keys())}"
    elif isinstance(x, list):
        res["b_data"] = f"<list>:\nlength{len(x)}"
    elif isinstance(x, pd.DataFrame):
        res["b_data"] = f"<pd.DataFrame>:\n{x.__repr__()}"
    elif isinstance(x, pd.Series):
        res["b_data"] = f"<pd.Series>:\n{x.reset_index().__repr__()}"
    else:
        res["b_data"] = x
    return res

def abbrStr(x):
    if len(x) > 20:
        return x[:17] + "..."
    else:
        return x
        

class treeInfo:
    def loaddata(self, data):
        self.data = data
    def getdata(self):
        return self.data
ti = treeInfo()

    
def loaddata():
    data = json.loads(request.data)
    ti.loaddata(data)
    print(data.keys())
    return "load json data success!"

def tree():
    data = json.loads(request.data)
    ct = calcTree().from_treeinfo(data)
    res = {"err": "",
           "eroute": "",
           "route": [], 
           "name": "",
           "data": ti.getdata()}
    ct.nodes["root"].receive(res)
    ##print([i for i in ct.nodes["root"]. iter()])
    res = [i for i in ct.nodes["root"]. iter()]
    node_res = {i:j.stack for i, j in ct.nodes.items()}
    for i in res:
        i["data"] = beautify(i["data"])
        i["name_abbr"] = abbrStr(i["name"])        
    for j in node_res.values():
        for i in j:
            i["data"] = beautify(i["data"])
            i["name_abbr"] = abbrStr(i["name"])                    
    tr = {"res": res, "node_res": node_res}
    ##tr_str = pd2str(tr)
    return json.dumps(tr)

## app.add_url_rule("/", "init", init, methods=["GET", "POST"])
app.add_url_rule("/flask/loaddata", "loaddata", loaddata, methods=["GET", "POST"])
app.add_url_rule("/flask/tree", "tree", tree, methods=["GET", "POST"])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=True)
    #app.run(host="127.0.0.1", port=5005, debug=False)
