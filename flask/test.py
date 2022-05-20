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

