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
        if isinstance(data, str):
            self.value = json.loads(data)
        elif isinstance(data, dict):
            self.value = data
        else:
            raise
    
    def to_elixir(self):
        return json.dumps(self.value)

    def save(self, filename="tmp.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.value, f)

    def load(self, filename='tmp.pkl'):
        print(filename)
        with open(filename, "rb") as f:
            self.value = pickle.load(f)
        print(filename)

    def feed(self, xml):
        self.result = "PPLL_" + xml


    
