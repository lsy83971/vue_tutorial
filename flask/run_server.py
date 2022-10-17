import sys
import traceback
import pandas as pd
import numpy as np
import uuid
import os
from copy import deepcopy
import ast
from flask import Flask, session, jsonify
from flask import render_template_string, render_template
from flask import request
import json

#sys.path.append("/home/lsy/project/vue_tutorial/flask/")
sys.path.append("/home/lsy/project/vue_tutorial/flask/")


from pyxmind_tools import name_trans
from pyxmind import calcTree, result_parse, raw_macro
from pyxmind_output import clacNodeOutput
from pdform import pd2json, pd2str, beautify, abbrStr

code_macro = {"$fd" :"fromDataDict", 
              "$td" :"toDataDict", 
              "$nd" :"ti.tree.nodes", 
              "$f" :"fromData", 
              "$t" :"toData", 
              "$n" :"node", 
              "$g" :"ti.tree.attr", }


          
class treeUserManager:
    def __init__(self):
        self.treeInfos = dict()
        self.code_macro = dict()
        self.tree_macro = dict()        

    def create_treeInfo(self, force=False):
        ## print("usename:")
        ## print(session.get("username"))
        if force is True:
            session["username"] = uuid.uuid4()
            self.treeInfos[session["username"]] = treeInfo()
        else:
            if session.get("username", None) is None:
                session["username"] = uuid.uuid4()
                self.treeInfos[session["username"]] = treeInfo()
                self.code_macro[session["username"]] = code_macro.copy()
                self.tree_macro[session["username"]] = raw_macro.copy()

    def getTreeInfo(self):
        self.create_treeInfo()
        return self.treeInfos[session["username"]]

    def getCodeMacro(self):
        self.create_treeInfo()
        return self.code_macro[session["username"]]

    def getTreeMacro(self):
        self.create_treeInfo()
        return self.tree_macro[session["username"]]
    
class treeInfo:
    def __init__(self):
        self.cleartree()
    
    def loaddata(self, data):
        self.data = data

    def loadtree(self, tree):
        self.tree = tree

    def loadtreedata(self, data):
        self.treedata = data
        
    def cleartree(self):
        self.tree = None
        
    def gettree(self):
        return self.tree
        
    def getdata(self):
        if hasattr(self, 'data'):
            return self.data
        else:
            return None

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
        print(data)
        ti = tm.getTreeInfo()
        ti.loaddata(data)
        return "load json success!"        
    except Exception as e:
        return "load json failed!"        

def code():
    __d = json.loads(request.data)
    __code = __d["code"]
    __context = __d["context"]
    print(__code)
    print(__d)
    try:
        try:
            ti = tm.getTreeInfo()
            toDataDict = {i:j.toData for i, j in ti.tree.nodes.items() if hasattr(j, 'toData')}
            fromDataDict = {i:j.fromData for i, j in ti.tree.nodes.items() if hasattr(j, 'fromData')}
            if __context["node"] != 0:
                tmp_node = __context["node"]
                toData = toDataDict[tmp_node]
                fromData = fromDataDict[tmp_node]
                node = ti.tree.nodes[tmp_node]
        except Exception as e:
            print(e)
        mc = tm.getCodeMacro()
        for i, j in mc.items():
            __code = __code.replace(i, j)
        print(__code)
        __block = ast.parse(__code, '''tmp''', mode='exec')
        __last = __block.body[-1]
        __isexpr = isinstance(__last,ast.Expr)
        _ = __block.body.pop() if __isexpr else None
        exec(compile(__block, '''tmp''', mode='exec'))
        print(__code)
        output = eval(compile(ast.Expression(__last.value),
                              '''tmp''', mode='eval')) if __isexpr else None
        if not isinstance(output, str):
            output = output.__repr__()
        return jsonify({"output": output})
    except Exception as e:
        output = "Error:\n" + traceback.format_exc()
        return jsonify({"output": output})

def add_cnen(res, ct):
    """
    CARE:
    change the origin meaning of route and name
    """
    if isinstance(res, dict):
        res = [j for i in res.values() for j in i]
    for i in res:
        i["id_concat"] = "$$". join(i["route"])

    nt = name_trans([i["id_concat"] for i in res], ct)
    for i in res:
        i["en"] = nt.map_en[i["id_concat"]]
        i["cn"] = nt.map_cn[i["id_concat"]]
    
def tree():
    try:
        data = json.loads(request.data)
        ti = tm.getTreeInfo()
        tmacro = tm.getTreeMacro()
        ti.cleartree()
        ct = calcTree(_node_cls=clacNodeOutput,
                      _macro=tmacro,
                      ).from_treeinfo(data)
        ti.loadtreedata(data)
        ti.loadtree(ct)
        res = {"err": "",
               "eroute": "",
               "route": [], 
               "name": "",
               "data": ti.getdata()}
        ct.nodes["root"].receive(res)
        ##print([i for i in ct.nodes["root"]. iter()])
        ##res = deepcopy([i for i in ct.nodes["root"]. iter()])
        res = [i for i in ct.nodes["root"]. iter()]
        #node_res = deepcopy({i:j.stack for i, j in ct.nodes.items()})
        node_res = {i:j.stack for i, j in ct.nodes.items()}

        add_cnen(res, ct)
        add_cnen(node_res, ct)    

        for i in res:
            result_parse.verr(i)
            i["data"] = beautify(i["data"])
            i["name_abbr"] = abbrStr(i["name"])

        for j in node_res.values():
            for i in j:
                result_parse.verr(i)            
                i["data"] = beautify(i["data"])
                i["name_abbr"] = abbrStr(i["name"])

        output = {i:j.output for i, j in ct.nodes.items()}
        tr = {"error": 0, "errorinfo": "", "res": res, "node_res": node_res, "output": output}
    except:
        errinfo = "Error:\n" + traceback.format_exc()
        tr = {"error": 1, "errorinfo": errinfo}
    
    return json.dumps(tr)

def revert():
    ti = tm.getTreeInfo()
    data = ti.treedata
    return json.dumps(ti.treedata)


## app.add_url_rule("/", "init", init, methods=["GET", "POST"])

if __name__ == "__main__":
    app = Flask(__name__, template_folder='./',static_folder="",static_url_path="/")
    app.config['SECRET_KEY'] = os.urandom(24)
    app.add_url_rule("/flask/loaddata", "loaddata", loaddata, methods=["GET", "POST"])
    app.add_url_rule("/flask/tree", "tree", tree, methods=["GET", "POST"])
    app.add_url_rule("/flask/code", "code", code, methods=["GET", "POST"])
    app.add_url_rule("/flask/clear", "clear", clear, methods=["GET", "POST"])
    app.add_url_rule("/flask/revert", "revert", revert, methods=["GET", "POST"])
    app.run(host="127.0.0.1", port=5005, debug=True)
