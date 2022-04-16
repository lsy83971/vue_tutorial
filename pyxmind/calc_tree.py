from collections import defaultdict
import pandas as pd
import traceback
from datetime import datetime, timedelta
import re
import copy

"""
bfc: 宏，在insert时被翻译，必须l[0]='bfc'，而l[1:] 分别作为后续被插入当前cell，
"""

#file_name = "drv_flow.org"


def load_org_tree(file_name):
    with open(file_name, "r") as f:
        p = f.read()

    lines = p.split("\n")
    lines1 = list()
    for i in lines:
        i1 = i.strip()
        if len(i1) == 0:
            continue
        if i1.startswith("#"):
            continue
        lines1.append(i)
        
    p = "\n". join(lines1)
    p = p[:re.search("[ \n]*$", p).span()[0]]
    p1 = re.split("\n(?=\*)", p)
    
    # drop level
    dlv = 0
    dact = False
    tree_list = list()
    
    for p2 in p1:
        rep2 = re.search("\n", p2)
        if rep2 is not None:
            _head = p2[:rep2.span()[0]]. strip()
            _tail = p2[rep2.span()[1]:]
            _head_list = re.split(" +", _head)
            
            if len(_head_list) > 2:
                for i in range(2, len(_head_list)):
                    if _head_list[i].startswith("#"):
                        _head_list = _head_list[:i]
                        break

            #print(_head_list)
            assert(len(_head_list) <= 4)
            _head_list.append(_tail)
        else:
            _head_list = re.split(" +", p2.strip())
            if len(_head_list) > 2:
                for i in range(2, len(_head_list)):
                    if _head_list[i].startswith("#"):
                        _head_list = _head_list[:i]
                        break
            
            #print(_head_list)
            assert(len(_head_list) <= 4)
            
        _head_level = len(_head_list[0])
        _head_info = _head_list[1:]
        assert len(_head_info) >= 1


        if dact is True:
            if _head_level > dlv:
                continue
            else:
                dact = False
                dlv = 0
        
        if _head_info[0]. strip().startswith("#"):
            dact = True
            dlv = _head_level
            continue
        
        tree_list.append([_head_level, _head_info])
    
    part = dict()
    part[0] = list()
    for i, j in tree_list:
        part[i] = j
        part[i - 1]. append(part[i])
    
    return part[1]


calc_dict_info = [
["grup", "-999000", ""],
["flws", "-999999", ""],
    
["raw", "-999008", "{0}"],
["asn", "-999000", "self.t={0}"], 
["rvs", "-999000", "{0}\nself.t=r"],

["locd", "-999000", "self.t=r.loc[{0}];assert isinstance(self.t,pd.DataFrame)"],
["locs", "-999000", "self.t=r.loc[{0}];assert isinstance(self.t,pd.Series)"],
["locv", "-999000", "self.t=r.loc[{0}];assert not isinstance(self.t,(pd.Series,pd.DataFrame))"],
    
["ilcd", "-999000", "self.t=r.iloc[{0}];assert isinstance(self.t,pd.DataFrame)"],
["ilcs", "-999000", "self.t=r.iloc[{0}];assert isinstance(self.t,pd.Series)"],
["ilcv", "-999000", "self.t=r.iloc[{0}];assert not isinstance(self.t,(pd.Series,pd.DataFrame))"],

    
["slcd", "-999000", "self.t=r[{0}];assert isinstance(self.t,pd.DataFrame)"],
["slcs", "-999000", "self.t=r['{0}'];assert isinstance(self.t,pd.Series)"],
["slcv", "-999000", "self.t=r['{0}'];assert not isinstance(self.t,(pd.Series,pd.DataFrame))"],

    
["rasn", "-999000", "self.root.{0}=r;self.t=r"], 
["casn", "-999000", "r['{0}']={1};self.t=r"],
["dctk", "-999000", "self.t=r['{0}']"], 
]

calc_dict = pd.DataFrame(calc_dict_info, columns = ["sym", "err", "code", ]).set_index("sym")
assert calc_dict.index.duplicated().mean() == 0
#assert calc_dict["err"].duplicated().mean() == 0

class calc_tree:
    """
    基本算符
    """
    def __init__(self, info, root = None):
        if root is None:
            root = self
            self.record=False
            self.reset_records()

        self.root = root
        if isinstance(info[0], str):
            
            if info[0] == "bfc":
                self.type = "bfc"
                
            elif info[0] == "init":
                self.type = "init"                
                
            elif info[0] == "grup":
                self.type = "grup"
                
            elif info[0] == "flow":
                self.type = "flow"
                
            elif info[0] == "flws":
                self.type = "flws"
                
            elif info[0] == "null":
                self.type = "null"
                
            else:
                self.type = "calc"
        else:
            raise

        if self.type == "calc":
            self.calc = calc_basic(info, root = root)

        if self.type == "bfc":
            self.bfc = [calc_tree(i, root = root) for i in info[1:]]
            
        if self.type == "init":
            self.has_init=False
            self.init = [calc_tree(i, root = root) for i in info[1:]]            

        if self.type == "flow":
            self.flow = [calc_tree(i, root = root) for i in info[1:]]         

        if self.type == "flws":
            self.flow = [calc_tree(i, root = root) for i in info[1:]]

        if self.type == "grup":
            self.grup = calc_group(info, root = root)
           
    def start_record(self):
        self.record=True
        
    def stop_record(self):
        self.record=False        
            
    def reset_records(self):
        self.errors=dict()
        self.result=dict()

            
    def iter_flow(self, d, n = None):
        assert self.type in  ("flow", "flws")
        if n is None:
            n = len(self.flow)
            
        if n == 0:
            yield d

        else:
            for _d in self.iter_flow(d, n = n - 1):
                yield from self.flow[n - 1]. iter(d = _d)

    def iter_flws(self, d):
        
        self.iserr = d["e"]
        _cid = d["c"] + "##flws"
        if self.iserr:
            _err = d["r"]
        else:
            try:
                self.t = [i["r"] for i in self.iter_flow(d)]
            except:
                self.iserr = True
                _err = "ERR:" + _cid

        ## TODO cid repeat
        if self.iserr is True:
            yield {"r": _err, "e": self.iserr, "c": _cid}
        else:
            yield {"r": self.t, "e": self.iserr, "c": _cid}
    

    def iter(self, d):
        if self.type == "calc":
            yield from self.calc.iter(d)

        if self.type == "null":
            pass

        if self.type == "bfc":
            for i in self.bfc:
                yield from i.iter(d)
                
        if self.type == "init":
            if self.has_init:
                pass
            else:
                for i in self.init:
                    yield from i.iter(d)
                
                self.has_init=True

        if self.type == "flow":
            yield from self.iter_flow(d)
            
        if self.type == "flws":
            yield from self.iter_flws(d)
            
        if self.type == "grup":
            yield from self.grup.iter(d)

    def feed(self, r, col_map = None):
        pb_info = dict()
        NOT_MAP = col_map is None
        if NOT_MAP:
            for info in self.iter({"r":r,"e":False,"c":""}):
                pb_info[info["c"]] = info["r"]
        else:
            for info in self.iter({"r":r,"e":False,"c":""}):
                if info["c"] in col_map:
                    pb_info[col_map[info["c"]]] = info["r"]
                    
        return pb_info                
                
class calc_basic:
    """
    基本算符

    """
    def __init__(self, info, root = None):
        if root is None:
            root = self
        self.root = root
        
        self.sym = info[0]
        
        self.params = [i.replace("<<", "r['").\
                       replace(">>", "']")\
                       if isinstance(i, str)
                       else i
                       for i in info[1:]]
        self.code = calc_dict.loc[self.sym]["code"]. format(*self.params)
        print(self.code)
        self.err = calc_dict.loc[self.sym]["err"]
        self.cid = "#". join([str(i) for i in info])
        self.iserr = False

    def iter(self, d):
        root=self.root
        self.iserr = d["e"]
        r = d["r"]
        _cid = d["c"] + "##" + self.cid
        
        if self.iserr:
            _err = d["r"]
            _err_info=""
           
        else:
            try:
                exec(self.code)
                if root.record:
                    root.result[_cid]=copy.deepcopy(self.t)
                    
            except:
                
                self.iserr = True
                _err = "ERR:" + _cid
                _err_info=traceback.format_exc()
                root.errors[_cid]=_err_info
                
        if self.iserr is True:
            yield {"r": _err, "e": self.iserr, "c": _cid, "ei":_err_info}
        else:
            yield {"r": self.t, "e": self.iserr, "c": _cid}
            

class calc_group:
    def __init__(self, info, root = None):
        if root is None:
            root = self
        self.root = root
        
        self.sym = info[0]
        self.params = info[1:]
        self.err = calc_dict.loc[self.sym]["err"]
        self.cid = "#". join([str(i) for i in info])
        self.iserr = False

    def gp(self, r):
        for i, j in r.groupby(self.params):
            if not isinstance(i, tuple):
                i = (i, )
            yield i, j

    def iter(self, d):
        root=self.root
        try:
            r = d["r"]
            c = d["c"]
            for i, j in self.gp(r):
                _cid = "##". join(["#". join(["equl", self.params[k], str(i[k])]) for k in range(len(self.params))])
                yield {"c": c + "##" + _cid,
                       "r": (i, j),
                       "e": False}
        except:
            _cid = d["c"] + "##" + self.cid
            self.iserr = True
            r = self.err
            _err_info=traceback.format_exc()
            root.errors[_cid]=_err_info


## -999999 原始空
## -999998 连接空1
## -999997 连接空2



