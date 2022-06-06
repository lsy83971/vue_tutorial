import pandas as pd

sb = pd.DataFrame([[1, 2], [3, 4]])
data:sb.to_json(orient="records")
columns:sb.columns.tolist()
opts:[]


pd.Series([1, 2, 3]).max()

# 1 opts (type:process, process:{max color} width:. )
# 2 type
import numpy as np
np.format_float_positional(3, trim="-")
np.format_float_positional(3.00, trim="-")
np.format_float_positional(3.00, trim="-")
np.nan
pd.isnull(np.nan)

pd.api.types.is_float(3)
round(4, 4)
        orient : str
            Indication of expected JSON string format.

            * Series:

                - default is 'index'
                - allowed values are: {{'split', 'records', 'index', 'table'}}.

            * DataFrame:

                - default is 'columns'
                - allowed values are: {{'split', 'records', 'index', 'columns',
                  'values', 'table'}}.

            * The format of the JSON string:

                - 'split' : dict like {{'index' -> [index], 'columns' -> [columns],
                  'data' -> [values]}}
                - 'records' : list like [{{column -> value}}, ... , {{column -> value}}]
                - 'index' : dict like {{index -> {{column -> value}}}}
                - 'columns' : dict like {{column -> {{index -> value}}}}
                - 'values' : just the values array
                - 'table' : dict like {{'schema': {{schema}}, 'data': {{data}}}}

                Describing the data, where data component is like ``orient='records'``.




from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
#求向量积(outer()方法又称外积)
x = np.outer(np.linspace(-2, 2, 30), np.ones(30))
#矩阵转置
y = x.copy().T 
#数据z
z = np.cos(x ** 2 + y ** 2)
#绘制曲面图
fig = plt.figure()
ax = plt.axes(projection='3d')
调用plot_surface()函数
ax.plot_surface(x, y, z,cmap='viridis', edgecolor='none')
ax.set_title('Surface plot')
plt.show()

import numpy as np
from scipy.stats import multivariate_normal
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
X = np.linspace(-5,5,50)
Y = np.linspace(-5,5,50)
X, Y = np.meshgrid(X,Y)

X_mean = 0; Y_mean = 0
X_var = 5; Y_var = 5
pos = np.empty(X.shape+(2,))
pos[:,:,0]=X
pos[:,:,1]=Y
rv = multivariate_normal([X_mean, Y_mean],[[X_var, 0], [0, Y_var]])
Z = rv.pdf(pos)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, rv.pdf(pos), cmap="plasma", alpha=0.8)
plt.show()

s = 0.0025

X1 = X[::5, ::5]
Y1 = Y[::5, ::5]
Z1 = Z[::5, ::5]


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
Z1 = list()
for i in range(X1.shape[0] - 1):
    Z1_sub = list()
    for j in range(Y1.shape[0] - 1):    
        s1 = int(min(Z1[i, j], Z1[i + 1, j], Z1[i, j + 1], Z1[i + 1, j + 1]) / s)*s
        x = X1[i:(i + 2), j:(j + 2)]
        y = Y1[i:(i + 2), j:(j + 2)]        
        z = np.array([[s1, s1], [s1, s1]])
        Z1_sub.append(s1)

        
        ax.plot_surface(x, y, z, cmap="plasma", alpha=0.8)        
plt.show()
X1

Z1
Z



import pandas as pd

gg = pd.read_pickle("./models/MONITOR_ALL.pkl")
gg.keys()



import json
pd.DataFrame(json.loads(gg['总体渠道分月指标监控_AUC，KS(auc)']))

for i in gg.keys():
    print(i)
    print(pd.DataFrame(json.loads(gg[i])))


pd.DataFrame(json.loads(gg["总体渠道分月指标监控_AUC，KS(cnt)"])).columns
pd.DataFrame(json.loads(gg["总体渠道分月指标监控_AUC，KS(cnt)"])).columns












