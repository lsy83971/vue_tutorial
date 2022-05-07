import traceback
from copy import deepcopy
## TODO: OFF delete
## TODO:
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
        assert (self.h0 in ['as', 'copy', 'raw', 'iter', 'null'])
        assert (self.h1 in ['id', ''])
        

    def parseHead(self):
        res = dict()
        self.headers = self.headline.strip().split(" ")
        if len(self.headers) <= 0:
            raise Exception('node header empty')
        self.h = self.headers[0]
        self.parseType()
        
    def parse(self):
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
            
        code = code.replace("$f", "self.fromData")
        code = code.replace("$t", "self.toData")
        code = code.replace("$n", "self")
        code = code.replace("$r", "self.root.fromData")
        code = code.replace("$i", "self.iterfunc")
        code = code.replace("$g", "self.attr")
        self.code = code
        if not hasattr(self, "name"):
            self.name = self.code

        
class calcNode:
    def __init__(self):
        self.stack = list()

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
        self.sur = info['sur']
        self.ci = codeParser(self.rawcode)
        self.ci.parse()
        return self

    def result(self):
        return deepcopy({"data": self.toData,
                "route": self.route,
                "id": self.id,
                "name": self.ci.name, 
                "err": self.err,
                "eroute": self.eroute,
                })
    
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
                exec(code)
                if tp not in ["iter", "null"]:
                    assert hasattr(self, "toData")
                if tp == "null":
                    self.toData = "null iter"
                self.err = ""
                self.eroute = ""
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
        self.exec()
        if tp == "null":
            self.stack.append(deepcopy(self.result()))
            return
        
        if tp != "iter":
            yield self.result()
            self.stack.append(deepcopy(self.result()))
        else:
            try:
                for i in self.iterfunc(self):
                    self.toData = i["toData"]
                    self.route = deepcopy(self.rawroute)
                    self.route[ - 1] = self.route[ - 1] + "##key:" + i["key"]
                    yield self.result()
                    self.stack.append(deepcopy(self.result()))
            except:
                self.toData = "iterError!"
                self.err="Error:\n" + traceback.format_exc()
                self.route = deepcopy(self.rawroute)
                self.eroute = self.route
                yield self.result()
                self.stack.append(deepcopy(self.result()))

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
    def __init__(self):
        super().__init__()
        self.attr = attr()

    def from_treeinfo(self, tree):
        self.info = tree['info']
        self.struct = tree['struct']
        self.codes = {i:j["v"] for i, j in self.info.items()}
        self.sur = {i:j["sur"] for i, j in self.info.items()}
        self.nodes = dict()
        for i, j in self.info.items():
            nodeinfo = {
                "id": i, 
                "code": j["v"], 
                "chd": self.struct[i], 
                "sur": j["sur"]}
            n = calcNode().from_nodeinfo(nodeinfo)
            self.nodes[i] = n

        for i, j in self.nodes.items():
            j.link(self)
        return self

    def getNode(self, i):
        return self.nodes[i]

if __name__ == "__main__":
    data = {'info': {'root': {'v': 'as_id\n$f\n:root', 'show': 1, 'sur': 0, 'w1': 182, 'h1': 55, 'w2': 182, 'h2': 130, 'w2_add': 212, 'h4': 0, 'w4': 0, 'w4_add': 0, 'w3': 394, 'h3': 130, 'x0': 0, 'x1': -91, 'x2': 91, 'x4': 121, 'x3': 212, 'x5': 303, 'x6': -91, 'x7': 303, 'y0': 0, 'y1': -27.5, 'y2': 27.5, 'y3': -65, 'y4': 65, 'y5': -65, 'y6': 65, 'y7': 0, 'y8': 0, 'x9': 333, 'x11': 519, 'x10': 426}, 'c_0': {'v': "as\n$f['a']\n:c1", 'show': 1, 'sur': 0, 'w1': 182, 'h1': 55, 'w2': 0, 'h2': 0, 'w2_add': 0, 'h4': 0, 'w4': 0, 'w4_add': 0, 'w3': 182, 'h3': 55, 'x0': 212, 'x1': 121, 'x2': 303, 'x4': 333, 'x3': 333, 'x5': 333, 'x6': 121, 'x7': 333, 'y0': -37.5, 'y1': -65, 'y2': -10, 'y3': -37.5, 'y4': -37.5, 'y5': -65, 'y6': -10, 'y7': -37.5, 'y8': -37.5, 'x9': 363, 'x11': 549, 'x10': 456}, 'c_1': {'v': "as\n$f['b']\n:c2", 'show': 1, 'sur': 0, 'w1': 182, 'h1': 55, 'w2': 0, 'h2': 0, 'w2_add': 0, 'h4': 75, 'w4': 0, 'w4_add': 0, 'w3': 182, 'h3': 55, 'x0': 212, 'x1': 121, 'x2': 303, 'x4': 333, 'x3': 333, 'x5': 333, 'x6': 121, 'x7': 333, 'y0': 37.5, 'y1': 10, 'y2': 65, 'y3': 37.5, 'y4': 37.5, 'y5': 10, 'y6': 65, 'y7': 0, 'y8': 75, 'x9': 363, 'x11': 549, 'x10': 456}}, 'struct': {'root': ['c_0', 'c_1'], 'c_0': [], 'c_1': []}, 'opts': {'cNO': 14, 'offset_x': 191, 'offset_y': 115, 'width': 1022, 'height': 800, 'isalive': 1, 'active_node': 0}}
    xmldata = {"a": 1, "b": 2}
    ct = calcTree().from_treeinfo(data)
    ct.nodes["root"].receive({"err": "", "eroute": "",
                              "route": [], 
                              "name": "", "data": xmldata})

    ct.nodes["root"]. stack[0]
    ct.nodes["c_0"]. stack[0]
    ct.nodes["c_0"]. ci.name
    dir(ct.nodes["c_0"]. ci    )
    ct.nodes["c_0"]. id



    ##    return {"data": self.toData,
    ##            "route": self.route,
    ##            "id": self.id,
    ##            "name": self.ci.name, 
    ##            "err": self.err,
    ##            "eroute": self.eroute,
    ##            }
    
