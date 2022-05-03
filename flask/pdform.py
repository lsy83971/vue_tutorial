import pandas as pd


def cutstr(s):
    if len(s) > 200:
        s = s[:200] + "\n..."
    return s

def pdformjson(s):
    return s.to_json()

def pdformstr(s):
    s = s.__repr__()
    return cutstr(s)

def pdform(tree, f=pdformstr):
    if isinstance(tree, dict):
        return {i:pdform(j, f=f) for i, j in tree.items()}
    if isinstance(tree, list):
        return [pdform(i, f=f) for i in tree]
    if isinstance(tree, pd.Series) or isinstance(tree, pd.DataFrame):
        return f(tree)
    if isinstance(tree, str):
        return cutstr(tree)

def pd2json(tree):
    return pdform(tree, f=pdformjson)

def pd2str(tree):
    return pdform(tree, f=pdformstr)
