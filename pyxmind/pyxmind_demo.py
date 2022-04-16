import os
import json
import pandas as pd
from pbxmind import *

## 读取xmind结构
ct=xt("test2.xmind")

## 读取人行征信结构化数据
_sjf="./sample/sample_od_PID2021010200047166.json"
with open(_sjf,"r") as f:
    sj=f.read()
    _df={i:pd.DataFrame(j) for i,j in json.loads(sj).items()}
    
## 基本模式;喂数据,出结果
result=ct.feed(_df)
print(ct.record)
print(ct.result)
print(ct.errors)
print(result)

## 记录模式;喂数据,出结果 记录每个节点结果
ct.start_record()
result=ct.feed(_df)
print(ct.record)
print(pd.Series(ct.result))
print(pd.Series(ct.errors))