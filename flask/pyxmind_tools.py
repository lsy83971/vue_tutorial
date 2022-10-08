import json
import copy
import sys
import pandas as pd
sys.path.append("/home/bozb/lsy/RELEASE/model_server/flask/")
from SFTP.load import xml_manager
from SFTP.xml_struct import xml_struct
from pyxmind import *
from datetime import datetime

def read_mdc(file_name):
    with open(file_name, "r") as f:
        x1 = f.read()
    treedata = json.loads(x1)
    ct = calcTree().from_treeinfo(treedata)
    return ct

def res_target(target, ct, t_res = None, update = False, v = False):
    ct._use_stack = False
    print(ct._use_stack)
    s1 = xml_manager()
    if t_res is None:
        newobj = True
    else:
        newobj = False

    if newobj:
        t_res = dict()

    if update is False:
        target = target[~target["pid"]. isin(t_res.keys())]
    for i in s1.read(target. sort_values("dt1"), rm = True):
        if i["filename"] is None:
            continue
        
        if v:        
            print(datetime.now())
        _filename = "/home/bozb/lsy/DATA/XML_DIR/" + i["filename"]
        _xs = xml_struct(_filename)
        _df = _xs.df_info()
        if v:
            print(datetime.now())
        ct.nodes["root"].receive({"err": "", "eroute": "",
                                  "route": [], 
                                  "name": "", "data": _df})
        res = list(ct.nodes["root"]. iter())
        t_res[i["pid"]] = res
        if v:
            print(datetime.now())
            print(i["pid"])
    if newobj:
        return t_res
    

def res_target_raw(target, t_res = None):
    s1 = xml_manager()
    if t_res is None:
        newobj = True
    else:
        newobj = False

    if newobj:
        t_res = dict()

    for i in s1.read(target. sort_values("dt1"), rm = True):
        if i["filename"] is None:
            continue
        print(datetime.now())
        _filename = "/home/bozb/lsy/DATA/XML_DIR/" + i["filename"]
        _xs = xml_struct(_filename)
        _df = _xs.df_info()
        t_res[i["pid"]] = _df
        print(i["pid"])
    if newobj:
        return t_res


#####################
## 脱敏



#####################
## 脱敏

deinfo_list = \
["PA01BQ01_被查询者姓名", #孙晓宇
"PA01BD01_被查询者证件类型", #身份证
"PA01BI01_被查询者证件号码", #131002199905024829
"PB01AQ01_电子邮箱", #17684383470@139.com/@wo.com/@1
"PB01AQ02_通讯地址", #河北省廊坊市经济技术开发区大长亭村2组55号
"PB01AD05_国籍", #中华人民共和国
"PB01AQ03_户籍地址", #河北省廊坊市经济技术开发区大长亭村2组55号
]

def delete_name(i):
    for j in deinfo_list:
        del i["base"][j]

def to_json(df, filename):
    df = df.copy()
    delete_name(df)
    df1 = dict()
    for i, j in df.items():
        df1[i] = j.to_dict()
    _j = json.dumps(df1)
    with open(filename, "w") as f:
        f.write(_j)


######################################
## name
import re

class resdf:
    def __init__(self, t_res):
        self.t_res = t_res
        print(datetime.now())
        self.data = pd.DataFrame({i:{"$$". join(k['route']): k["data"] for k in j} for i, j in t_res.items()}).T
        print(datetime.now())
        self.err = pd.DataFrame({i:{"$$". join(k['route']): k["err"] for k in j} for i, j in t_res.items()}).T
        print(datetime.now())

    def assure_not_null(self):
        err_cols = self.data.columns[self.data.columns.str.contains("Err")]
        normal_cols = self.data.columns[~self.data.columns.str.contains("Err")]
        self.err_cols = err_cols
        self.normal_cols = normal_cols
        assert self.data[normal_cols].isnull().sum().sum() == 0
        
    def nerr_trans(self):
        err_cols = self.data.columns[self.data.columns.str.contains("Err")]
        normal_cols = self.data.columns[~self.data.columns.str.contains("Err")]
        self.err_cols = err_cols
        self.normal_cols = normal_cols
        self.aerr_cnt = pd.Series()
        for i in normal_cols:
            print(i)
            _tmp_cond = self.data[i]. astype(str).apply(lambda x:"Error" in x).values
            print(_tmp_cond.sum())
            if _tmp_cond.sum() == 0:
                self.aerr_cnt[i] = 0
                continue
            self.aerr_cnt[i] = (~(self.err[i]. loc[_tmp_cond]. str.contains("NErr").fillna(False))).sum()

        assert self.aerr_cnt.sum() == 0

        for i in normal_cols:
            _tmp_cond = self.data[i]. astype(str).apply(lambda x:"Error" in x).values
            if _tmp_cond.sum() == 0:
                continue
            self.data.loc[_tmp_cond, i] = self.err.loc[_tmp_cond, i]
        
class name_form:
    def __init__(self, name):
        self.id_concat = name
        self.id_list = name.split("$$")
        self.is_err = ("Err" in name)
        self.err_map = []

    def trans(self, cn_dict, en_dict):
        self.cn_list = [cn_dict.get(i.split("##")[0]) for i in self.id_list]
        self.en_list = [en_dict.get(i.split("##")[0]) for i in self.id_list]
        self.key_list = ["" if '##' not in i else i.split("##")[ - 1] for i in self.id_list]
        for i in range(len(self.key_list)):
            _key = self.key_list[i]
            if _key != "":
                assert(len(_key.split(":")) == 2)
                _key = _key.split(":")[ - 1]
                if _key == "none":
                    self.cn_list[i] = ""
                    self.en_list[i] = ""
                else:
                    self.cn_list[i] = self.cn_list[i]. replace("%key%", _key)
                    self.en_list[i] = self.en_list[i]. replace("%key%", _key)
        
        self.cn_concat = "_". join([i for i in self.cn_list if i != ""])
        self.en_concat = "_". join([i for i in self.en_list if (i != "none" and i != "")])

    def re(self, l):
        self.re_c = re.compile(self.id_concat.replace("Err", "[^:#$]+").replace("$", "\\$") + "$")
        res = list()
        for i in l:
            if i == self.id_concat:
                continue
            if re.match(self.re_c, i):
                res.append(i)
        self.err_map = res


class name_trans:
    def __init__(self, l, ct):
        self.name_dict = {i.id: i.name.split("\n")[0] for i in ct.nodes.values()}
        assert (pd.Series({i: len(j.split(":")) for i, j in self.name_dict.items()}) == 2).mean() == 1
        self.cn_dict = {i: j.split(":")[0] for i, j in self.name_dict.items()}
        self.en_dict = {i: j.split(":")[1] for i, j in self.name_dict.items()}
        self.l = dict()
        for i in l:
            _tmp = name_form(i)
            _tmp.trans(self.cn_dict, self.en_dict)
            self.l[i] = _tmp

        t_cn_concat = [i.cn_concat for i in self.l.values()]
        t_en_concat = [i.en_concat for i in self.l.values()]
        self.cmt = {i.en_concat:i.cn_concat for i in self.l.values()}
        self.map_cn = {i.id_concat:i.cn_concat for i in self.l.values()}
        self.map_en = {i.id_concat:i.en_concat for i in self.l.values()}

        try:
            assert len(t_cn_concat) == len(set(t_cn_concat))
        except:
            print("duplicated cn")

        try:
            assert len(t_en_concat) == len(set(t_en_concat))
        except:
            print("duplicated en")
        
        self.re()
        
    def info(self):
        return {i: j.info() for i, j in self.l.items()}

    def re(self):
        l = list(self.l.keys())
        for i in self.l.values():
            if i.is_err:
                i.re(l)

    def err_keys(self):
        res = list()
        for i, j in self.l.items():
            if j.is_err:
                res.append(i)
        return res

    def err_trans(self, rf):
        for i in self.err_keys():
            cond = (~rf.err[i]. isnull())
            print(i)
            print(cond.sum())
            if cond.sum() == 0:
                continue
            for j in self.l[i]. err_map:
                rf.data.loc[cond, j] = rf.err.loc[cond, i]

def check_ab(rf, pid_info, ct, t_res):
    g = rf.err[rf.aerr_cnt[rf.aerr_cnt > 0]. index]. fillna("").applymap(lambda x:False if x == "" or ("NErr" in x) else True)
    g1 = g.sum(axis = 1)
    new_pid = g1[g1 > 0]. index.tolist()
    print("Err pid cnt:")
    print(len(new_pid))
    res_target(pid_info[pid_info["pid"]. isin(new_pid)], ct = ct, t_res = t_res, v = False, update = True)



