import numpy as np
import pandas as pd
from env import get_connection
from acquire import wrangle_zillow
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import sklearn.preprocessing

def wrangle_mall_customers():
    '''
    looking for an already existing mall_customers csv on the local machine
    '''
    if os.path.isfile('mall_customers.csv'):
        return pd.read_csv('mall_customers.csv')
    else:
        '''
        if there is no existing csv, then connect to the SQL server and get the information from 
        mall_customers db
        '''
        url = get_connection('mall_customers')
        '''
        query for sql
        '''
        query = '''
                SELECT *
                FROM customers;
                '''
        
        df = pd.read_sql(query, url)
        '''
        saving the newly queried SQL table to a csv so it
        can be used instead of connecting to the SQL server
        every time I want this info
        '''
        df.to_csv('mall_customers.csv', index=False)
        return df


def remove_outliers(df, k=1.5, number=8):
    a=[]
    b=[]
    fences=[a, b]
    features= []
    col_list = []
    i=0
    for col in df:
        new_df=np.where(df[col].nunique()>number, True, False)
        if new_df==True:
            if df[col].dtype == 'float' or df[col].dtype == 'int':
                '''
                for each feature find the first and third quartile
                '''
                q1, q3 = df[col].quantile([.25, .75])
                '''
                calculate inter quartile range
                '''
                iqr = q3 - q1
                '''
                calculate the upper and lower fence
                '''
                upper_fence = q3 + (k * iqr)
                lower_fence = q1 - (k * iqr)
                '''
                appending the upper and lower fences to lists
                '''
                a.append(upper_fence)
                b.append(lower_fence)
                '''
                appending the feature names to a list
                '''
                features.append(col)
                '''
                assigning the fences and feature names to a dataframe
                '''
                var_fences= pd.DataFrame(fences, columns=features, index=['upper_fence', 'lower_fence'])
                col_list.append(col)
            else:
                print(col)
                print('column is not a float or int')
        else:
            print(f'{col} column ignored')
                                    
    for col in col_list:
        '''
        reassigns the dataframe to only include values withing the upper and lower fences/drop outliers
        '''
        df = df[(df[col]<= a[i]) & (df[col]>= b[i])]
        i+=1
    return df, var_fences


def scale_mall(df):
    ss=sklearn.preprocessing.StandardScaler()
    num_cols=['age', 'annual_income', 'spending_score']
    ss.fit(df[num_cols])
    df[num_cols]=ss.transform(df[num_cols])
    return df