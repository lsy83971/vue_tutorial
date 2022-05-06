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

class treeUserManager:
    def __init__(self):
        self.treeInfos = dict()

    def create_treeInfo(self, force=False):
        print("usename:")
        print(session.get("username"))
        if force is True:
            session["username"] = uuid.uuid4()
            self.treeInfos[session["username"]] = treeInfo()
        else:
            if session.get("username", None) is None:
                session["username"] = uuid.uuid4()
                self.treeInfos[session["username"]] = treeInfo()

    def getTreeInfo(self):
        self.create_treeInfo()
        return self.treeInfos[session["username"]]

    
class treeInfo:
    def __init__(self):
        self.cleartree()
    
    def loaddata(self, data):
        self.data = data

    def loadtree(self, tree):
        self.tree = tree
        
    def cleartree(self):
        self.tree = None
        
    def gettree(self):
        return self.tree
        
    def getdata(self):
        return self.data

tm = treeUserManager()

def clear():
    try:
        ti = tm.getTreeInfo()    
        ti.cleartree()
        return "success!"
    except:
        return "failed!"
    
def loaddata():
    try:
        data = json.loads(request.data)
        ti = tm.getTreeInfo()
        ti.loaddata(data)
        return "load json success!"        
    except Exception as e:
        return "load json failed!"        

def code():
    __d = json.loads(request.data)
    __code = __d["code"]
    __context = __d["context"]
    try:
        try:
            ti = tm.getTreeInfo()
            toDataDict = {i:j.toData for i, j in ti.tree.nodes.items()}
            fromDataDict = {i:j.fromData for i, j in ti.tree.nodes.items()}
            if __context["node"] != 0:
                tmp_node = __context["node"]
                toData = toDataDict[tmp_node]
                fromData = fromDataDict[tmp_node]
                node = ti.tree.nodes[tmp_node]
        except Exception as e:
            print(e)
        __code = __code.replace("$fd", "fromDataDict")
        __code = __code.replace("$td", "toDataDict")
        __code = __code.replace("$nd", "ti.tree.nodes")        
        __code = __code.replace("$f", "fromData")
        __code = __code.replace("$t", "toData")
        __code = __code.replace("$n", "node")
        __code = __code.replace("$g", "ti.tree.attr")                      
        __block = ast.parse(__code, '''tmp''', mode='exec')
        __last = __block.body[-1]
        __isexpr = isinstance(__last,ast.Expr)
        _ = __block.body.pop() if __isexpr else None
        exec(compile(__block, '''tmp''', mode='exec'))
        output = eval(compile(ast.Expression(__last.value),
                              '''tmp''', mode='eval')) if __isexpr else None
        if not isinstance(output, str):
            output = output.__repr__()
        return {"output": output}
    except Exception as e:
        output = "Error:\n" + traceback.format_exc()
        return {"output": output}

def tree():
    data = json.loads(request.data)
    ti = tm.getTreeInfo()
    ti.cleartree()
    ct = calcTree().from_treeinfo(data)
    ti.loadtree(ct)
    res = {"err": "",
           "eroute": "",
           "route": [], 
           "name": "",
           "data": ti.getdata()}
    
    ct.nodes["root"].receive(res)
    ##print([i for i in ct.nodes["root"]. iter()])
    res = deepcopy([i for i in ct.nodes["root"]. iter()])
    node_res = deepcopy({i:j.stack for i, j in ct.nodes.items()})

    for i in res:
        result_parse.verr(i)
        i["data"] = beautify(i["data"])
        i["name_abbr"] = abbrStr(i["name"])
        
    for j in node_res.values():
        for i in j:
            result_parse.verr(i)            
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
app.add_url_rule("/flask/clear", "clear", clear, methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=True)
    #app.run(host="127.0.0.1", port=5005, debug=False)
