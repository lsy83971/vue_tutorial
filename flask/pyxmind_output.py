from pyxmind import calcNode, raw_macro
class clacNodeOutput(calcNode):
    def __init__(self, macro=raw_macro):
        super().__init__(macro = macro)
        self.output = ""
    
    def result(self):
        res = super().result()
        #res["output"] = self.output
        return res
        
    def result_point(self):
        res = super().result_point()
        #res["output"] = self.output
        return res

    def exec(self):
        self.output = ""
        super().exec()

        

