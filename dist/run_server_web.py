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


app = Flask(__name__, template_folder='./',static_folder="./",static_url_path="/")
app.config['SECRET_KEY'] = os.urandom(24)


#################### 1 flask
sys.path.append("./flask")
MODEL_PATH = "./flask/models/"

from pyxmind import calcTree, result_parse
from pdform import pd2json, pd2str, beautify, abbrStr

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

    def loadtreedata(self, data):
        self.treedata = data
        
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
    print("THANKS!!!")
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
    ti.loadtreedata(data)
    ti.loadtree(ct)
    res = {"err": "",
           "eroute": "",
           "route": [], 
           "name": "",
           "data": ti.getdata()}
    
    ct.nodes["root"].receive(res)
    ##print([i for i in ct.nodes["root"]. iter()])
    #res = deepcopy([i for i in ct.nodes["root"]. iter()])
    res = [i for i in ct.nodes["root"]. iter()]

    #node_res = deepcopy({i:j.stack for i, j in ct.nodes.items()})
    node_res = {i:j.stack for i, j in ct.nodes.items()}

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

def revert():
    ti = tm.getTreeInfo()
    data = ti.treedata
    return json.dumps(ti.treedata)


## app.add_url_rule("/", "init", init, methods=["GET", "POST"])
app.add_url_rule("/flask/loaddata", "loaddata", loaddata, methods=["POST"])
app.add_url_rule("/flask/tree", "tree", tree, methods=["GET", "POST"])
app.add_url_rule("/flask/code", "code", code, methods=["GET", "POST"])
app.add_url_rule("/flask/clear", "clear", clear, methods=["GET", "POST"])
app.add_url_rule("/flask/revert", "revert", revert, methods=["GET", "POST"])


# 2 model ###################################################

import re
re_month = re.compile("\d{4}-\d{2}")
tkey = 'month'

def j2df(x):
    return pd.DataFrame.from_dict(json.loads(x))

def j2dfd(x):
    for i in x.keys():
        if isinstance(x[i], str):
            x[i] = j2df(x[i])
            continue
        if isinstance(x[i], dict):
            j2dfd(x[i])
            continue
        raise BaseException('j2df error')

def yx(x):
    return x[tkey]["用信"]

def sx(x):
    return x[tkey]["授信"]

def ak(x):
    return x[tkey]["AUC_KS"]


def get_models():
    models = os.listdir(MODEL_PATH)
    models = [i for i in models if ".pkl" in i]
    return models

from copy import deepcopy

class reformDict:
    @staticmethod
    def setkey(target, keys, value):
        key = keys[0]
        if len(keys) == 1:
            target[key] = value
        else:
            if not key in target:
                target[key] = dict()
            reformDict.setkey(target[key], keys[1:], value)

    def load_config(self, d):
        self.config= d

    def reform(self, d):
        if not isinstance(d, dict):
            return d
        i_list = deepcopy(list(d.keys()))
        for i in i_list:
            if i in self.config["replace"]:
                return self.reform(d[i])

        for i in i_list:
            if i in self.config["delete"]:
                del d[i]
                continue

            value = self.reform(d[i])            
            if i in self.config["reform"]:
                del d[i]
                self.setkey(d, self.config["reform"][i], value)
                continue
            d[i] = value
            
            
        return d

def j2df(x):
    return pd.DataFrame.from_dict(json.loads(x))

def j2dfd(x):
    for i in x.keys():
        if isinstance(x[i], str):
            x[i] = j2df(x[i])
            continue
        if isinstance(x[i], dict):
            j2dfd(x[i])
            continue
        raise BaseException('j2df error')



def TotalData():
    res = dict()
    for i in get_models():
        res[i] = pd.read_pickle(MODEL_PATH + i)
    return res

nk = ["MODEL", "TYPE1", "TYPE2", "CHANNEL", "IDX"]

keyword = [
    "month", 
    "channel", 
    "cnt", 
    "bad_rate", 
    "auc", 
    "ks", 
    "bins",
    "feature",
    "label",
    "index",
    "comment",
    "apply_cnt",
    "pass_rate", 
    "pct",
    "psi",
    "PSI", 
    "lift",
    "pct_",
    "color", 
    
]

keyindex = ['psi', 'pass_rate', "lift", 'cnt', 'pct', "apply_cnt"]

def deactive(o, n):
    for i in range(n, len(o)):
        o[i]["active"] = False
        o[i]["ops"] = ["None"]
        o[i]["select"] = "None"

def choose(order, name):
    for i in order:
        if i["name"] == name:
            return i
    raise Exception("No Item")

class node:
    def __init__(self, name):
        self.name = name
        self.ops_next = dict()


    def node_next(self, order):
        if isinstance(self.ops, list):
            select = choose(order, self.name)["select"]
            if select in self.ops_next:
                return self.ops_next[select]
            else:
                return None
        return None

    def ops_dict(self):
        if isinstance(self.ops, list):
            return {self.name: self.ops}
        else:
            return self.ops
        
    def fit(self, data, order):
        """
        规定有哪些选项 包括后续
        """
        raise
    def select(self, data, order):
        raise

    def fit_next(self, data, order):
        pass


class node_TypeDict(node):
    def select(self, data, order):
        i = choose(order, self.name)
        return data[i["select"]]

    def fit(self, data, order):
        self.ops = list((data.keys()))
        order = deepcopy(order)
        j = choose(order, self.name)
        for i in self.ops:
            j["select"] = i
            self.fit_next(self.select(data, order), order)

class node_MODEL(node_TypeDict):
    def fit_next(self, data, order):
        select = choose(order, self.name)["select"]
        if select == "MONITOR_ALL.pkl":
            node = node_TYPE2("TYPE2")
        else:
            node = node_TYPE1("TYPE1")
        node.fit(data, order)
        self.ops_next[select] = node

class node_TYPE1(node_TypeDict):
    def fit_next(self, data, order):
        select = choose(order, self.name)["select"]
        node = node_TYPE2("TYPE2")
        node.fit(data, order)
        self.ops_next[select] = node

class node_TYPE2(node_TypeDict):
    def fit_next(self, data, order):
        select2 = choose(order, self.name).get("select")
        select1 = choose(order, "TYPE1").get("select")
        if select1 == "AUC_KS":
            return
        if select2 == "全量":
            return
        if select2 == "分月份":
            node = node_IDX_CHANNEL("IDX_CHANNEL")
            node.fit(data, order)
            self.ops_next[select2] = node

        if select2 == "分渠道":
            node = node_IDX("IDX")
            node.fit(data, order)
            self.ops_next[select2] = node

        if select2 == "分指标":
            node = node_CHANNEL("CHANNEL")
            node.fit(data, order)
            self.ops_next[select2] = node

class node_CHANNEL(node):
    def select(self, data, order):
        i = choose(order, self.name)["select"]
        if i not in ["total"]:
            data = data["sub"]
            return data[data["channel"] == i]
        else:
            return data["total"]

    def fit(self, data, order):
        _l = list()
        if "total" in data:
            _l.append("total")
        if "sub" in data:
            _l += list(set(data["sub"]["channel"]))
        self.ops = _l

class node_IDX(node_TypeDict):
    pass

class node_IDX_CHANNEL(node):
    def select(self, data, order):
        i1 = choose(order, "IDX")["select"]
        i2 = choose(order, "CHANNEL")["select"]
        data = data[i1]
        if i2 not in ["total"]:
            data = data["sub"]
            return data[data["channel"] == i2]
        else:
            return data["total"]

    def fit(self, data, order):
        _l1 = list(data.keys())
        _l2 = list()        
        if not len(_l1) == 0:
            data = list(data.values())[0]
            if "total" in data:
                _l2.append("total")
            if "sub" in data:
                _l2 += list(set(data["sub"]["channel"]))
        self.ops ={"CHANNEL": _l2, "IDX": _l1}

        
rf_config = {
    "replace": {
        "month", 
    },
    "delete": {
        "week", 
    },
    "reform": {
        "总体渠道分月指标监控_通过率(pass_rate)": ["分月份", "pass_rate", "total"], 
        "总体渠道分月指标监控_申请量(apply_cnt)": ["分月份", "apply_cnt", "total"],
        "总体渠道分月指标监控_申请量(psi)": ["分月份", "psi", "total"],
        "总体渠道分月指标监控_稳定性(psi)": ["分月份", "psi", "total"],

        
        "总体渠道分月指标监控_提升度(lift)": ["分月份", "lift", "total"],
        "总体渠道分月指标监控_通过人数(cnt)": ["分月份", "cnt", "total"],
        "总体渠道分月指标监控_人数占比(pct)": ["分月份", "pct", "total"],

        "分渠道分月份指标监控_通过率(pass_rate)": ["分月份", "pass_rate", "sub"], 
        "分渠道分月份指标监控_申请量(apply_cnt)": ["分月份", "apply_cnt", "sub"],
        "分渠道分月份指标监控_申请量(psi)": ["分月份", "psi", "sub"],
        "分渠道分月份指标监控_稳定性(psi)": ["分月份", "psi", "sub"],
        "分渠道分月份指标监控_提升度(lift)": ["分月份", "lift", "sub"],
        "分渠道分月份指标监控_通过人数(cnt)": ["分月份", "cnt", "sub"],
        "分渠道分月份指标监控_人数占比(pct)": ["分月份", "pct", "sub"],

        "总体月份分渠道指标监控_稳定性(psi)": ["分渠道", "psi"],
        "总体月份分渠道指标监控_申请量(psi)": ["分渠道", "psi"],
        "总体月份分渠道指标监控_通过率(pass_rate)": ["分渠道", "pass_rate"],
        "总体月份分渠道指标监控_提升度(lift)": ["分渠道", "lift"],
        "总体月份分渠道指标监控_通过人数(cnt)": ["分渠道", "cnt"],
        "总体月份分渠道指标监控_人数占比(pct)": ["分渠道", "pct"],
        "总体月份分渠道指标监控_申请量(apply_cnt)": ["分渠道", "apply_cnt"],

        "总体月份分渠道指标监控": ["分指标", "sub"],
        '总体渠道、月份指标监控': ["分指标", "total"],

        '分渠道分月份指标监控_AUC，KS': ["分月份/渠道"],
        '总体渠道分月指标监控_AUC，KS': ["分月份"],
        '总体月份分渠道指标监控_AUC，KS': ["分渠道"],
        '总体渠道、月份指标监控': ["全量"], 

        "总体渠道分月指标监控_AUC，KS(cnt)": ["分月份", "cnt", "total"],
        "总体渠道分月指标监控_AUC，KS(bad_rate)": ["分月份", "bad_rate", "total"],
        "总体渠道分月指标监控_AUC，KS(auc)": ["分月份", "AUC", "total"],
        "总体渠道分月指标监控_AUC，KS(ks)": ["分月份", "KS", "total"],
        "整体情况": ["全量"],
    }
}

raw_order = [{"name": "MODEL"},
             {"name": "TYPE1"},
             {"name": "TYPE2"},
             {"name": "MODEL"},
             {"name": "IDX"},
             {"name": "CHANNEL"},          
             ]

class OrderRoute():
    def __init__(self):
        rf = reformDict()
        rf.load_config(rf_config)
        td = TotalData()
        j2dfd(td)
        td = rf.reform(td)
        self.td = td
        nm = node_MODEL("MODEL")
        nm.fit(td, raw_order)
        self.nm = nm

    def select(self, order, point='', render=False):
        if point in ["CHANNEL", "IDX"]:
            return order, None

        new_order = deepcopy(order)
        for i in new_order:
            i["ops"] = ["None"]
            i["select"] = "None"
            i["active"] = False

        node = self.nm
        data = self.td
        name = "MODEL"
        need_finish = False
        if point == "raw":
            need_finish = True
        
        while True:
            ops_dict = node.ops_dict()
            for name, ops in ops_dict.items():
                i1 = choose(new_order, name)
                i1["ops"] = ops
                i1["active"] = True

            if need_finish:
                return new_order, None

            selectactive = True
            for name, ops in ops_dict.items():
                i = choose(order, name)
                if ("select" not in i) or ("active" not in i):
                    selectactive = False                    
                    break
                    
                if (i["active"] is False) or (i["select"] not in ops):
                    selectactive = False                    
                    break
            if selectactive is False:
                return new_order, None

            if selectactive is True:
                for name, ops in ops_dict.items():
                    i = choose(order, name)
                    i1 = choose(new_order, name)
                    i1["select"] = i["select"]

            if point == name:
                need_finish = True

            new_node = node.node_next(order)
            if new_node is None:
                if render is False:
                    return new_order, None
                else:
                    return new_order, node.select(data, order)
            data = node.select(data, order)            
            node = new_node
            name = node.name

            
                        


odr = OrderRoute()

## raw_order = [{"name": "MODEL", "active": True, "select": 'ZYD_XYFR_TYZXMODELSCORE_score.pkl'},
## {"name": "TYPE1", "active": True, "select": '用信'},
## {"name": "TYPE2", "active": True, "select": '分月份'},
## {"name": "IDX", "active": True, "select": 'psi'},
## {"name": "CHANNEL", "active": True, "select": 'total'},          
## ]
## 
## sb = odr.select(raw_order, "TYPE2")
## 
## pd.DataFrame(sb[0])
# sb = odr.select(raw_order, "", True)

def select():
    print("TANKS!!")
    data = json.loads(request.data)
    o, df = odr.select(data["o"], data["p"])
    return json.dumps(o)

def render():
    data = json.loads(request.data)
    o, df = odr.select(data["o"], "", True)
    idx = choose(data['o'], "IDX")["select"]
    return parsedf(minimize(df), idx)

def minimize(df):
    # if "feature" in df:
    #     df = df[df["feature"] == "score"]
    #     del df["feature"]
    if "label" in df:
        df = df[df["label"] == "odhis30_first"]
        del df["label"]
    if "index" in df:
        del df["index"]

    for i in ["pct_base", "bad_rate_base", "cnt_all", "bad_cnt_all", "days_far_from_now", "PSI"]:
        if i in df:
            del df[i]
        
    return df

def parsedf(df, idx=None):
    if idx not in keyindex:
        idx = None
    if "feature" in df.columns:
        df["color"] = (df["feature"]. shift(1)!= df["feature"]).cumsum().apply(lambda x:"white" if x % 2 == 1 else "black")
    _c = df.columns.astype(str).tolist()
    _typedict = dict()
    _typedict1 = dict()    
    for i in _c:
        if i not in keyword:
            _typedict[i] = idx
        else:
            _typedict[i] = i

    for i, j in _typedict.items():
        if j is None:
            _d1 = {"data": i, "type": "normal"}
        elif j == "psi":
            _d1 = {"data": i, "type": "process"}
            _d1["process_max"] = 0.05
            _d1["process_color"] = "blue"
        elif j == "pass_rate":
            _d1 = {"data": i, "type": "process"}
            _d1["process_max"] = 0.5
            _d1["process_color"] = "blue"
        elif j == "lift":
            _d1 = {"data": i, "type": "process"}
            _d1["process_max"] = 2
            _d1["process_color"] = "red"
        elif j in ["cnt", "apply_cnt"]:
            _d1 = {"data": i, "type": "process"}
            _d1["process_max"] = df[i]. max(skipna = True)
            _d1["process_color"] = "blue"
        elif j == "pct":
            _d1 = {"data": i, "type": "process"}
            _d1["process_max"] = df[i]. max(skipna = True)
            _d1["process_color"] = "blue"
        elif j == "bad_rate":
            _d1 = {"data": i, "type": "process"}
            _d1["process_max"] = df[i]. max(skipna = True)
            _d1["process_color"] = "red"
        elif j in keyword:
            _d1 = {"data": i, "type": "normal"}
        else:
            raise Exception("testGG")
        if "process_max" in _d1:
            if pd.isnull(_d1['process_max']):
                _d1 = {"data": i, "type": "normal"}
        _typedict1[i] = _d1
    df = df.applymap(lambda x: \
                     "null" if pd.isnull(x) else \
                     np.format_float_positional(round(x, 4), trim="-") \
                     if pd.api.types.is_float(x) \
                     else str(x))
    _d = df.astype(str).to_json(orient='records')
    return json.dumps({"col": _c, "data": _d, "type": _typedict1})

app.add_url_rule("/model/select", "select", select, methods=["GET", "POST"])
app.add_url_rule("/model/render", "render", render, methods=["GET", "POST"])

############### 3 web

# 任务是建立单机版的调试器
# simple way
# 一切从简单 但是预留扩展空间
def home():
    return render_template("index.html")

# import requests
# @app.route('/model/<path>',methods=['POST', "GET"])
# def proxymodel(path):
#     SITE_NAME = "http://127.0.0.1:5006/model/"
#     if request.method=='GET':
#         resp = requests.get(f'{SITE_NAME}{path}')
#         return resp.content
#     elif request.method=='POST':
#         resp = requests.post(f'{SITE_NAME}{path}',json=request.get_json())
#         return resp.content        
# 
# import requests
# @app.route('/flask/<path>',methods=['POST', "GET"])
# def proxyflask(path):
#     SITE_NAME = "http://127.0.0.1:5005/flask/"
#     if request.method=='GET':
#         resp = requests.get(f'{SITE_NAME}{path}')
#         return resp.content
#     elif request.method=='POST':
#         resp = requests.post(f'{SITE_NAME}{path}',json=request.get_json())
#         return resp.content        

app.add_url_rule("/", "home", home, methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=True)
    #app.run(host="127.0.0.1", port=5005, debug=False)