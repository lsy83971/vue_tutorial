# 任务是建立单机版的调试器
# simple way
# 一切从简单 但是预留扩展空间
import sys
sys.path.append("/home/lsy/pyxmind")
from pyxmind import calcTree
from pdform import pd2json, pd2str, beautify, abbrStr
import pandas as pd
import numpy as np
import uuid
import os
import ast
from flask import Flask, session
from flask import render_template_string, render_template
from flask import request
import json
app = Flask(__name__, template_folder='./',static_folder="",static_url_path="/")
app.config['SECRET_KEY'] = os.urandom(24)

class treeUserManager:
    def __init__(self):
        self.treeInfos = dict()

    def create_treeInfo(self):
        print("usename:")
        print(session.get("username"))
        if session.get("username", None) is None:
            session["username"] = uuid.uuid4()
            self.treeInfos[session["username"]] = treeInfo()

    def getTreeInfo(self):
        self.create_treeInfo()
        return self.treeInfos[session["username"]]

class treeInfo:
    def loaddata(self, data):
        self.data = data

    def loadtree(self, tree):
        self.tree = tree
        
    def gettree(self):
        return self.tree
        
    def getdata(self):
        return self.data

tm = treeUserManager()
    
def loaddata():
    data = json.loads(request.data)
    ti = tm.getTreeInfo()
    ti.loaddata(data)
    print(data.keys())
    return "load json data success!"

def code():
    ti = tm.getTreeInfo()        
    __code = json.loads(request.data)["code"]
    __block = ast.parse(__code, '''tmp''', mode='exec')
    __last = __block.body[-1]
    __isexpr = isinstance(__last,ast.Expr)
    _ = __block.body.pop() if __isexpr else None
    exec(compile(__block, '''tmp''', mode='exec'))
    output = eval(compile(ast.Expression(__last.value), '''tmp''', mode='eval')) if __isexpr else None
    return {"output": output.__repr__()}
    

def tree():
    data = json.loads(request.data)
    ti = tm.getTreeInfo()    
    ct = calcTree().from_treeinfo(data)
    ti.loadtree(ct)
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

    #print("tree info:")
    #exec("""print(ti.tree.nodes)""")
    #print(ti.tree.nodes['root']. stack)
    
    return json.dumps(tr)

## app.add_url_rule("/", "init", init, methods=["GET", "POST"])
app.add_url_rule("/flask/loaddata", "loaddata", loaddata, methods=["GET", "POST"])
app.add_url_rule("/flask/tree", "tree", tree, methods=["GET", "POST"])
app.add_url_rule("/flask/code", "code", code, methods=["GET", "POST"])



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=True)
    #app.run(host="127.0.0.1", port=5005, debug=False)
