import traceback
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
        if self.h0 in ['null', 'off']:
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
        code = code.replace("$r", "self.root.toData")
        code = code.replace("$i", "self.iterfunc")
        self.code = code
        if not hasattr(self, "name"):
            self.name = self.code

        
class calcNode:
    def hasChild(self):
        return len(self.chd) != 0
    
    def hasSur(self):
        return self.sur != 0

    def needYieldId(self):
        return self.ci.h1 == "id"
    
    def link(self, m):
        self.m = m
        self.root = self.m.getNode("root")
        
    def from_nodeinfo(self, info):
        self.rawcode = info["code"]
        self.chd = info['chd']
        self.sur = info['sur']
        self.ci = codeParser(self.rawcode)
        self.ci.parse()
        return self

    def result(self):
        return {"data": self.toData,
                "name": self.name,
                "err": self.err
                }
    
    def receive(self, res):
        self.fromData = res["data"]
        self.fromErr = res["err"]
        self.fromName = res["name"]        
        self.name = res["name"] + "##" + self.ci.name

    def calc(self):
        code = self.ci.code
        try:
            exec(code)
            self.err = ""
        except:
            self.err=traceback.format_exc()
            self.toData = self.err            

    def iterSur(self, res):
        sur = self.m.getNode(self.sur)
        sur.receive(res)
        yield from sur.iter()

    def iterChd(self):
        tp = self.ci.h0
        tp1 = self.ci.h1        
        for i in self.chd:
            n = self.m.getNode(i)
            n.receive(self.result())
            yield from n.iter()
        
    def iter(self):
        tp = self.ci.h0
        tp1 = self.ci.h1        
        if tp == "off":
            raise Exception("node off")
        
        if self.fromErr != "":
            return
        
        if tp == "null":
            return

        self.calc()
        
        if (not self.hasChild()) and (not self.hasSur()):
            yield self.result()
            return
        
        if self.needYieldId():
            yield self.result()

        for tmp_res in self.iterChd():
            if self.hasSur():
                yield from self.iterSur(tmp_res)
            else:
                yield tmp_res
                

class calcTree:
    def from_treeinfo(self, tree):
        self.info = tree['info']
        self.struct = tree['struct']
        self.codes = {i:j["v"] for i, j in self.info.items()}
        self.sur = {i:j["sur"] for i, j in self.info.items()}
        self.nodes = dict()
        for i, j in self.info.items():
            nodeinfo = {"code": j["v"], 
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
    pass

    


    
