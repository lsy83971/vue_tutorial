from pyxmind import calcNode
class clacNodeOutput(calcNode):
    def result(self):
        res = super().result()
        res["output"] = self.output
        return res
        
    def result_point(self):
        res = super().result_point()
        res["output"] = self.output
        return res

    def exec(self):
        self.output = ""
        super().exec()

        

