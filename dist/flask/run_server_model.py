from copy import deepcopy
import sys
import traceback
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
import re
re_month = re.compile("\d{4}-\d{2}")

app = Flask(__name__, template_folder='./',static_folder="",static_url_path="/")
app.config['SECRET_KEY'] = os.urandom(25)
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
        print(i)
        raise BaseException('j2df error')

def yx(x):
    return x[tkey]["用信"]

def sx(x):
    return x[tkey]["授信"]

def ak(x):
    return x[tkey]["AUC_KS"]

MODEL_PATH = "./models/"
def get_models():
    models = os.listdir(MODEL_PATH)
    models = [i for i in models if ".pkl" in i]
    return models



    # ak['分渠道分月份指标监控_AUC，KS']
    # ak1 # select 渠道 up 指标 left 月份
    # ak['总体渠道分月指标监控_AUC，KS']
    # ak2 # select up 指标 left 月份 off 渠道
    # ak['总体月份分渠道指标监控_AUC，KS']
    # ak3 # select up 指标 left 渠道 off 月份
    # ak['总体渠道、月份指标监控']
    # ak4 # select up 指标 left off 月份 渠道

sxit_d = {
    "月样本-单渠道-单指标": 1,
    "总样本-分渠道-单指标": 2,
    "总样本-全渠道-全指标": 3,
}


sxit1_t = {
    "pass_rate": "总体渠道分月指标监控_通过率(pass_rate)", 
    "apply_cnt": "总体渠道分月指标监控_申请量(apply_cnt)", 
    "psi": "总体渠道分月指标监控_申请量(psi)", 
}

sxit1 = {
    "pass_rate": "分渠道分月份指标监控_通过率(pass_rate)", 
    "apply_cnt": "分渠道分月份指标监控_申请量(apply_cnt)", 
    "psi": "分渠道分月份指标监控_申请量(psi)", 
} # select 渠道 指标 up 月

sxit2 = {
    "pass_rate":"总体月份分渠道指标监控_通过率(pass_rate)", 
    "apply_cnt":"总体月份分渠道指标监控_申请量(apply_cnt)", 
    "psi":"总体月份分渠道指标监控_申请量(psi)", 
} # select 指标 up 渠道 off 月

sxit3 = "总体渠道、月份指标监控"
# select up 指标 off 月 渠道

###########################################################

yxit_d = {
    "月样本-单渠道-单指标": 1,
    "总样本-分渠道-单指标": 2,
    "总样本-单渠道-全指标": 3,
    "总样本-全渠道-全指标": 4,
}

yxit1_t = {
    "psi":           "总体渠道分月指标监控_稳定性(psi)", 
    "pass_rate":     "总体渠道分月指标监控_通过率(pass_rate)", 
    "lift":          "总体渠道分月指标监控_提升度(lift)", 
    "cnt":          "总体渠道分月指标监控_通过人数(cnt)", 
    "pct":          "总体渠道分月指标监控_人数占比(pct)", 
}

yxit1 = {
    "psi":           "分渠道分月份指标监控_稳定性(psi)", 
    "pass_rate":     "分渠道分月份指标监控_通过率(pass_rate)", 
    "lift":          "分渠道分月份指标监控_提升度(lift)", 
    "cnt":          "分渠道分月份指标监控_通过人数(cnt)", 
    "pct":          "分渠道分月份指标监控_人数占比(pct)",
} # select 渠道 指标 up 月

yxit2 = {
    "psi": "总体月份分渠道指标监控_稳定性(psi)", 
    "pass_rate": "总体月份分渠道指标监控_通过率(pass_rate)", 
    "lift": "总体月份分渠道指标监控_提升度(lift)", 
    "cnt": "总体月份分渠道指标监控_通过人数(cnt)", 
    "pct": "总体月份分渠道指标监控_人数占比(pct)", 
} # select 指标 up 渠道 off 月

yxit3 = "总体月份分渠道指标监控"
# select 渠道 up 指标 off 月

yxit4 = "总体渠道、月份指标监控"
# select up 指标 off 月 渠道

akit1 = '分渠道分月份指标监控_AUC，KS'
akit2 = '总体渠道分月指标监控_AUC，KS'
akit3 = '总体月份分渠道指标监控_AUC，KS'
akit4 = '总体渠道、月份指标监控'


# MODEL:
# TYPE1:{YX SX AUC}:
# TYPE2:{}
# CHANNEL:
# IDX:

pmap = {"MODEL":0, 
"TYPE1":1, 
"TYPE2":2, 
"CHANNEL":3, 
"IDX":4}

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
]

keyindex = ['psi', 'pass_rate', "lift", 'cnt', 'pct', "apply_cnt"]

def deactivate(o, n):
    for i in range(n, len(o)):
        o[i]["active"] = False
        o[i]["ops"] = ["None"]
        o[i]["select"] = "None"

class MPS():
    def __init__(self):
        self.d = dict()
        ms = get_models()
        for i in ms:
            self.d[i] = MP(MODEL_PATH + i)

    def get_models(self):
        return list(self.d.keys())
    
class MP():
    def __init__(self, path):
        self.d = pd.read_pickle(path)
        j2dfd(self.d)
        df = yx(self.d)[yxit1["cnt"]]
        months = pd.Series(df.columns)
        months = months[~months.apply(lambda x:re.search(re_month, x)).isnull()]
        channels = df["channel"]. drop_duplicates()
        self.yx_channels = channels.tolist()
        self.yx_months = months.tolist()
        self.yx_idx = ['psi', 'pass_rate', "lift", 'cnt', 'pct']


        dfsx = sx(self.d)[sxit1["apply_cnt"]]
        sx_months = pd.Series(dfsx.columns)
        sx_months = sx_months[~sx_months.apply(lambda x:re.search(re_month, x)).isnull()]
        sx_channels = dfsx["channel"]. drop_duplicates()
        self.sx_channels = sx_channels.tolist()
        self.sx_months = sx_months.tolist()
        self.sx_idx = ['pass_rate', "apply_cnt", 'psi']


    ## AUC
    def akRouter(self, word, **kwargs):
        pass
    
    ## sx        

    def sxRouterSelect(self, word):
        print(word)
        assert word in sxit_d
        if sxit_d[word] == 1:
            return {"CHANNEL": self.sx_channels,
                    "IDX": self.sx_idx,
                    }
        if sxit_d[word] == 2:
            return {"IDX": self.sx_idx}
        if sxit_d[word] == 3:
            return dict()

    def sxRouter(self, word, **kwargs):
        assert word in sxit_d
        if sxit_d[word] == 1:
            return self.sx1(**kwargs)
        if sxit_d[word] == 2:
            return self.sx2(**kwargs)
        if sxit_d[word] == 3:
            return self.sx3(**kwargs)

    def sx1(self, channel, idx):
        assert idx in ['psi', 'pass_rate', "apply_cnt"]
        if channel == "all":
            return sx(self.d)[sxit1_t[idx]]
        else:
            sxdf = sx(self.d)[sxit1[idx]]
            return sxdf[sxdf["channel"] == channel]

    def sx2(self, idx, channel=None):
        assert idx in ['psi', 'pass_rate', "lift", 'cnt', 'pct']
        return sx(self.d)[sxit2[idx]]

    def sx3(self, channel=None, idx=None):
        return sx(self.d)[sxit3]
        
    ## yx
    def yxRouterSelect(self, word):
        print(word)
        assert word in yxit_d
        if yxit_d[word] == 1:
            return {"CHANNEL": self.yx_channels,
                    "IDX": self.yx_idx,
                    }
        if yxit_d[word] == 2:
            return {"IDX": self.yx_idx}
        if yxit_d[word] == 3:
            return {"CHANNEL": self.yx_channels}
        if yxit_d[word] == 4:
            return dict()

    def yxRouter(self, word, **kwargs):
        assert word in yxit_d
        if yxit_d[word] == 1:
            return self.yx1(**kwargs)
        if yxit_d[word] == 2:
            return self.yx2(**kwargs)
        if yxit_d[word] == 3:
            return self.yx3(**kwargs)
        if yxit_d[word] == 4:
            return self.yx4(**kwargs)
        
    def yx1(self, channel, idx):
        assert idx in ['psi', 'pass_rate', "lift", 'cnt', 'pct']
        if channel == "all":
            return yx(self.d)[yxit1_t[idx]]
        else:
            yxdf = yx(self.d)[yxit1[idx]]
            return yxdf[yxdf["channel"] == channel]

    def yx2(self, idx, channel=None):
        assert idx in ['psi', 'pass_rate', "lift", 'cnt', 'pct']
        return yx(self.d)[yxit2[idx]]

    def yx3(self, channel, idx=None):
        yxdf = yx(self.d)[yxit3]
        return yxdf[yxdf["channel"] == channel]
        
    def yx4(self, channel=None, idx=None):
        return yx(self.d)[yxit4]

class RT():
    def receive(self, o, point):
        if point == "RAW":
            return self.receive1(o)
        if point == "MODEL":
            return self.receive2(o)
        if point == "TYPE1":
            return self.receive3(o)
        if point == "TYPE2":
            return self.receive4(o)

    def receive1(self, o):
        ms = mps.get_models()
        if len(ms) > 0:
            print(o)
            o[0]["ops"] = ms
            o[0]["active"] = True
            o[0]["select"] = "None"           
            deactivate(o, 1)
        else:
            deactivate(o, 0)
        return o

    def receive2(self, o):
        mp = mps.d[o[0]["select"]]
        o[1]["ops"] = list(mp.d[tkey].keys())
        o[1]["active"] = True
        o[1]["select"] = "None"
        print(list(mp.d.keys()))
        deactivate(o, 2)
        return o

    def receive3(self, o):
        mp = mps.d[o[0]["select"]]
        mp1 = mp.d[tkey][o[1]["select"]]
        k = o[1]["select"]
        if k == "用信":
            o[2]["ops"] = list(yxit_d.keys())
            o[2]["active"] = True
            o[2]["select"] = 'None'

        if k == "AUC_KS":
            o[2]["ops"] = list(mp1.keys())
            o[2]["active"] = True
            o[2]["select"] = 'None'            


        if k == "授信":
            o[2]["ops"] = list(sxit_d.keys())
            o[2]["active"] = True
            o[2]["select"] = 'None'            
            
        deactivate(o, 3)            
        return o

    def receive4(self, o):
        mp = mps.d[o[0]["select"]]
        mp1 = mp.d[tkey][o[1]["select"]]
        k = o[1]["select"]
        j = o[2]["select"]
        if k == "用信":
            deactivate(o, 3) 
            res = mp.yxRouterSelect(j)
            for i1, i2 in res.items():
                o[pmap[i1]]["ops"] = i2
                o[pmap[i1]]["active"] = True
                o[pmap[i1]]["select"] = 'None'            

        if k == "授信":
            deactivate(o, 3) 
            res = mp.sxRouterSelect(j)
            for i1, i2 in res.items():
                o[pmap[i1]]["ops"] = i2
                o[pmap[i1]]["active"] = True
                o[pmap[i1]]["select"] = 'None'                           

        if k == "AUC_KS":
            deactivate(o, 3)
        return o

    def render(self, o):
        m = o[0]["select"]
        t1 = o[1]["select"]
        t2 = o[2]["select"]
        channel = o[3]["select"]
        idx = o[4]["select"]
        
        mp = mps.d[m]
        mp1 = mp.d[tkey][t1]
        if t1 == "用信":
            return mp.yxRouter(t2, channel=channel, idx=idx)

        if t1 == "授信":
            return mp.sxRouter(t2, channel=channel, idx=idx)

        if t1 == "AUC_KS":
            return mp1[t2]
    
mps = MPS()
rt = RT()

def select():
    data = json.loads(request.data)
    o = rt.receive(data["o"], data["p"])
    print(pd.DataFrame(o))
    return json.dumps(o)

def render():
    data = json.loads(request.data)
    df = rt.render(data["o"])
    idx = data['o'][4]["select"]
    return parsedf(minimize(df), idx)

def minimize(df):
    if "feature" in df:
        df = df[df["feature"] == "score"]
        del df["feature"]
    if "label" in df:
        df = df[df["label"] == "odhis30_first"]
        del df["label"]
    if "index" in df:
        del df["index"]
    return df

def parsedf(df, idx=None):
    if idx not in keyindex:
        idx = None
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
            _d1["process_max"] = 0.1
            _d1["process_color"] = "blue"
        elif j == "pass_rate":
            _d1 = {"data": i, "type": "process"}
            _d1["process_max"] = 0.5
            _d1["process_color"] = "green"
        elif j == "lift":
            _d1 = {"data": i, "type": "process"}
            _d1["process_max"] = 2
            _d1["process_color"] = "red"
        elif j in ["cnt", "apply_cnt"]:
            _d1 = {"data": i, "type": "process"}
            _d1["process_max"] = df[i]. max(skipna = True)
            _d1["process_color"] = "green"
        elif j == "pct":
            _d1 = {"data": i, "type": "process"}
            _d1["process_max"] = df[i]. max(skipna = True)
            _d1["process_color"] = "green"
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
        
    print(_typedict)
    print(_typedict1)   
    
    df = df.applymap(lambda x: \
                     "null" if pd.isnull(x) else \
                     np.format_float_positional(round(x, 4), trim="-") \
                     if pd.api.types.is_float(x) \
                     else str(x))
    _d = df.astype(str).to_json(orient='records')
    ## lift:
    return json.dumps({"col": _c, "data": _d, "type": _typedict1})

app.add_url_rule("/model/select", "select", select, methods=["GET", "POST"])
app.add_url_rule("/model/render", "render", render, methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5006, debug=True)
    #app.run(host="127.0.0.1", port=5005, debug=False)
