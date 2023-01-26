import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def missing_nulls(df):
    a=[]
    b=[]
    c=[]
    e= {'num_rows_missing': a, 'pct_rows_missing': b}
    for col in df:
        c.append(col)
        nulls= sum(df[col].isnull())
        a.append(nulls)
        b.append(nulls/len(df[col]))
        d= pd.DataFrame(index=c, data=e)
    return d

def handle_missing_values(df, prop_req_column, prop_req_row):
    drop_col= len(df)* prop_req_column
    df= df.dropna(axis=1, thresh= drop_col)
    drop_row= len(df.columns)* prop_req_row
    df= df.dropna(axis=0, thresh=drop_row)
    return df