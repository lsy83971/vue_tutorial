import traceback
from copy import deepcopy
## TODO: OFF delete
## TODO:

raw_macro = {
    "$f":  "self.fromData", 
    "$t": "self.toData", 
    "$n": "self", 
    "$r": "self.root.fromData", 
    "$i": "self.iterfunc", 
    "$g": "self.attr", 
}

        
class codeParser:
    def __init__(self, rawcode):
        self.rawcode = rawcode

    def parseType(self):
        res = dict()
        h = self.h
        if (h == ""):
            raise Exception('node header empty')
        if h.startswith("#"):
            self.h0 = 'off'
            self.h1 = ''
            return
        
        h = h.lower()
        hs = h.split("_")
        assert ((len(hs) <= 2) and (len(hs) >= 1))
        self.h0 = hs[0]        
        if (len(hs) == 1):
            self.h1 = ''
        else:
            self.h1 = hs[1]
        assert (self.h0 in ['as', 'copy', 'raw', 'iter', 'null', "once"])
        assert (self.h1 in ['id', '',  'nomacro'])
        

    def parseHead(self):
        res = dict()
        self.headers = self.headline.strip().split(" ")
        if len(self.headers) <= 0:
            raise Exception('node header empty')
        self.h = self.headers[0]
        self.parseType()
        
    def parse(self, macro):
        rawcode = self.rawcode
        lines = rawcode.split('\n')
        foot = lines[ - 1]. strip()
        if foot.startswith(":"):
            self.name = foot[1:]
            lines = lines[: -1]
            
        self.lines = lines
        if (len(self.lines) <= 0):
            raise Exception('node info empty')
        self.headline = self.lines[0]
        self.parseHead()

        if self.h0 in ['off']:
            self.code = ""
            
        self.restline = '\n'. join([" ". join(self.headers[1:])] + self.lines[1:])
        code = self.restline

        if self.h0 == "as":
            code = f'$t={code.strip()}'
        if self.h0 == "copy":
            code = f'{code}\n$t=$f'
        if self.h0 in ["raw", "iter"]:
            code = code

        if self.h1 != "nomacro":
            for i, j in macro.items():
                code = code.replace(i, j)

        self.code = code
        if not hasattr(self, "name"):
            self.name = self.code

        
class calcNode:
    def __init__(self, macro=raw_macro):
        self.stack = list()
        self.macro = macro

    def clear(self):
        self.stack = []

    def find_route(self, r):
        for i in self.stack:
            print("ir:", i['route'])
            print("r:", r)
            if i["route"] == r:
                return i
    
    def hasChild(self):
        return len(self.chd) != 0
    
    def hasSur(self):
        return self.sur != 0

    def needYieldId(self):
        return self.ci.h1 == "id"

    def isLeaf(self):
        return (not self.hasChild()) and (not self.hasSur())        
    
    def link(self, m):
        self.m = m
        self.root = self.m.getNode("root")
        self.attr = m.attr
        
    def from_nodeinfo(self, info):
        self.rawcode = info["code"]
        self.id = info["id"]        
        self.chd = info['chd']
        self.name = info['name']        
        self.sur = info['sur']
        self.ci = codeParser(self.rawcode)
        self.ci.parse(self.macro)
        if self.ci.h0 == "once":
            self.done_once = False
        return self

    def result(self):
        try:
            return deepcopy({"data": self.toData,
                    "route": self.route,
                    "id": self.id,
                    "name": self.name, 
                    "err": self.err,
                    "eroute": self.eroute,
                    })
        except:
            return {"data": self.toData,
                    "route": self.route,
                    "id": self.id,
                    "name": self.name, 
                    "err": self.err,
                    "eroute": self.eroute,
                    }
        
    def result_point(self):
        return {"data": self.toData,
                "route": self.route,
                "id": self.id,
                "name": self.name, 
                "err": self.err,
                "eroute": self.eroute,
                }
        
    def receive(self, res):
        """
        step1
        fromData
        fromErr
        fromEroute
        route
        """
        self.fromData = res["data"]
        self.fromErr = res["err"]
        self.fromEroute = res["eroute"]        
        self.rawroute = res["route"] + [self.id]


    def receiveErr(self):
        return not(self.fromErr == "")

    ## def calc(self):
    ##     code = self.ci.code
    ##     try:
    ##         exec(code)
    ##         self.err = ""
    ##         self.eroute = ""
    ##     except:
    ##         self.err="Error:\n" + traceback.format_exc()
    ##         self.eroute = self.route
    ##         self.toData = "Error!"

    def iterSur(self, res):
        sur = self.m.getNode(self.sur)
        sur.receive(res)
        yield from sur.iter()

    def exec(self):
        """
        step3
        in EXEC PROCESSION
        WE MUST DEFINE:
        1. toData
        2. err
        3. eroute
        4. route
        """
        tp = self.ci.h0
        code = self.ci.code
         
        if self.receiveErr():
            self.toData = "Receive Error!"
            self.err = self.fromErr
            self.eroute = self.fromEroute
            self.route = self.rawroute
        else:
            try:
                self.err = ""
                self.eroute = ""
                exec(code)
                if (self.err != ""):
                    self.eroute = self.rawroute
                    self.toData = "Error!"
                else:
                    self.eroute = ""
                    if tp not in ["iter", "null", "once"]:
                        assert hasattr(self, "toData")
                    if tp in ["null", "once"]:
                        self.toData = "null iter"
                    assert isinstance(self.err, str)
                    
                self.route = self.rawroute
            except:
                self.err="Error:\n" + traceback.format_exc()
                self.eroute = self.rawroute
                self.route = self.rawroute
                self.toData = "Error!"
                return
            

    def iterSelf(self):
        """
        step4
        """
        tp = self.ci.h0
        code = self.ci.code
        if tp == "once":
            if self.done_once:
                print("HAS DONE")
                return 
        
        self.exec()
        if tp == "null":
            if self.m._use_stack:
                self.stack.append(self.result())
            return

        if tp == "once":
            if self.m._use_stack:
                self.stack.append(self.result())
                self.done_once = True
                return
        
        if tp != "iter":
            yield self.result_point()
            if self.m._use_stack:            
                self.stack.append(self.result())
        else:
            try:
                if self.receiveErr():
                    self.route = deepcopy(self.rawroute)
                    self.route[ - 1] = self.route[ - 1] + "##key:" + "Err"
                    yield self.result_point()
                    if self.m._use_stack:                
                        self.stack.append(self.result())
                    
                else:
                    tmp_iter = list(self.iterfunc(self))
                    for i in tmp_iter:
                        self.toData = i["toData"]
                        self.route = deepcopy(self.rawroute)
                        self.route[ - 1] = self.route[ - 1] + "##key:" + i["key"]
                        yield self.result_point()
                        if self.m._use_stack:
                            self.stack.append(self.result())
            except:
                self.toData = "iterError!"
                self.err="Error:\n" + traceback.format_exc()
                self.route = deepcopy(self.rawroute)
                self.eroute = self.route
                yield self.result_point()
                
                if self.m._use_stack:                
                    self.stack.append(self.result())

    def iterChd(self):
        tp = self.ci.h0
        tp1 = self.ci.h1
        for j in self.iterSelf():
            for i in self.chd:
                n = self.m.getNode(i)
                n.receive(j)
                yield from n.iter()
        
    def iter(self):
        """
        step2
        """
        tp = self.ci.h0
        tp1 = self.ci.h1
        if tp == "off":
            return
            ##raise Exception("node off")
        if self.isLeaf():
            yield from self.iterSelf()
            return
        
        if self.needYieldId():
            yield from self.iterSelf()

        for tmp_res in self.iterChd():
            if self.hasSur():
                yield from self.iterSur(tmp_res)
            else:
                yield tmp_res

class result_parse:
    @staticmethod
    def verr(x):
        if x["err"] != "":
            x["data"] = x["err"]
        return x

                
class attr(dict):
    def __getattribute__(self, name):
        return super().__getattribute__(name)
    def __setattr__(self, name, value):
        self[name] = value
        super().__setattr__(name, value)
            
class calcTree:
    def __init__(self, _use_stack = True, _node_cls=calcNode, _macro=raw_macro):
        super().__init__()
        self.attr = attr()
        self._node_cls = _node_cls
        self._use_stack = _use_stack
        self._macro = _macro

    def from_treeinfo(self, tree):
        self.info = tree['info']
        self.struct = tree['struct']
        self.codes = {i:j["v"] for i, j in self.info.items()}
        self.sur = {i:j["sur"] for i, j in self.info.items()}
        self.nodes = dict()
        for i, j in self.info.items():
            nodeinfo = {
                "name": j["name"], 
                "id": i, 
                "code": j["v"], 
                "chd": self.struct[i], 
                "sur": j["sur"]}
            n = self._node_cls(macro=self._macro).from_nodeinfo(nodeinfo)
            self.nodes[i] = n

        for i, j in self.nodes.items():
            j.link(self)
        return self

    def getNode(self, i):
        return self.nodes[i]

if __name__ == "__main__":
    import json
    with open("/home/lsy/Downloads/pd01 (13).mdc", "r") as f:
        x1 = f.read()
    with open("/home/lsy/vue_tutorial/flask/sample/sample_od_PID2021010200033947.json", "r") as f:
        x2 = f.read()
    treedata = json.loads(x1)
    xmldata = json.loads(x2)
    ct = calcTree().from_treeinfo(treedata)
    ct.nodes["root"].receive({"err": "", "eroute": "",
                              "route": [], 
                              "name": "", "data": xmldata})
    import datetime
    print(datetime.datetime.now())
    res = ct.nodes["root"]. iter()
    res1 = list(res)
    res1[0]
    print(datetime.datetime.now())



