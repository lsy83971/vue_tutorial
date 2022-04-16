import os
import json
import pandas as pd
import zipfile
import copy
import re
import pickle

class pyxmind:
    def __init__(self):
        pass

    def from_elixir(self, data):
        self.value = json.loads(data)
    
    def to_elixir(self):
        pass

    def save(self, filename="tmp.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.value, f)

    def load(self):
        pass

    def feed(self, xml):
        self.result = "PPLL_" + xml
    
    
