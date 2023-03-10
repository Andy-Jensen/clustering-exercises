#import libraries and the 'get_connection' function from env
import pandas as pd
import numpy as np
import env
import os
from env import get_connection
from sklearn.model_selection import train_test_split


def wrangle_zillow():
    '''
    looking for an already existing zillow csv on the local machine
    '''
    if os.path.isfile('zillow.csv'):
        return pd.read_csv('zillow.csv')
    else:
        '''
        if there is no existing csv, then connect to the SQL server and get the information from 
        zillow db
        '''
        url = get_connection('zillow')
        '''
        query for sql
        '''
        query = '''
                SELECT *
                FROM properties_2017
                LEFT JOIN predictions_2017 USING(parcelid)
                LEFT JOIN airconditioningtype USING(airconditioningtypeid)
                LEFT JOIN architecturalstyletype USING(architecturalstyletypeid)
                LEFT JOIN buildingclasstype USING(buildingclasstypeid)
                LEFT JOIN heatingorsystemtype USING(heatingorsystemtypeid)
                LEFT JOIN propertylandusetype USING(propertylandusetypeid)
                LEFT JOIN storytype USING(storytypeid)
                LEFT JOIN typeconstructiontype USING(typeconstructiontypeid)
                LEFT JOIN unique_properties USING(parcelid)
                WHERE longitude IS NOT NULL AND latitude IS NOT NULL 
                AND transactiondate LIKE '2017%%';
                '''
        
        df = pd.read_sql(query, url)
        '''
        saving the newly queried SQL table to a csv so it
        can be used instead of connecting to the SQL server
        every time I want this info
        '''
        df.to_csv('zillow.csv', index=False)
        return df


def tts(df, stratify=None):
    '''
    removing your test data from the data
    '''
    train_validate, test=train_test_split(df, 
                                 train_size=.8, 
                                 random_state=8675309,
                                 stratify=None)
    '''
    splitting the remaining data into the train and validate groups
    '''            
    train, validate =train_test_split(train_validate, 
                                      test_size=.3, 
                                      random_state=8675309,
                                      stratify=None)
    return train, validate, test