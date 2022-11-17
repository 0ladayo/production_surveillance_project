from google.cloud import storage

import pandas as pd

import datetime

import xlrd

import openpyxl

import fsspec

import gcsfs

import itertools

import os

import pandas_gbq

from google.cloud import bigquery

from pandas.api.types import CategoricalDtype 

import time

def dummy_function(event, context):
    
    def latest_file():
        
        storage_client = storage.Client()

        prefix = 'Daily Production Report'

        blobs = storage_client.list_blobs('demo-bucket-report', prefix = prefix)

        blob_created_time = []

        for blob in blobs:

            blob_created_time.append(blob.updated)

        if blob.updated == max(blob_created_time):

            latest_file_name = blob.name

        return latest_file_name
    
    def read_latest_file():
    
        df = pd.read_excel('gs://field-reports/{}'.format(latest_file()))

        return df
    
    def extract_date_and_well_data():
    
        date_list = []

        wells_list = []

        date_list.append(read_latest_file().iloc[2,6])

        wells_list.append(read_latest_file().iloc[33:47, 0:19])

        K = 12

        date_list = list(itertools.chain.from_iterable(itertools.repeat(i, K) for i in date_list))

        return date_list, wells_list
    
    def date_data_cleaning():
    
        date_df = pd.DataFrame(extract_date_and_well_data()[0])

        date_df.columns = ['next_date']

        date_df['next_date'] = date_df['next_date'].astype('string')

        date_df['next_date'] = date_df['next_date'].str.replace(' at 08:00 AM',' ')

        date_df['next_date'] = pd.to_datetime(date_df['next_date']).dt.date

        date_df['date'] = (date_df['next_date'] - datetime.timedelta(days=1))

        date_df.drop(['next_date'],axis = 1,inplace = True)

        date_df = date_df.reset_index(drop = True)

        return date_df
    
    def wells_data_cleaning():
    
        wells_df = pd.concat(extract_date_and_well_data()[1], axis = 0)

        wells_df.drop([36,39],axis = 0, inplace = True)

        wells_df.drop(['Unnamed: 2','Unnamed: 4','Unnamed: 6','Unnamed: 7','Unnamed: 12','Unnamed: 14',

                  'Unnamed: 17'],axis = 1,inplace = True)

        wells_df = wells_df.reset_index(drop = True)

        return wells_df
    
    def updated_wells_data():
      
        wells_df2 = pd.concat([date_data_cleaning(), wells_data_cleaning()], axis = 1)

        wells_df2.columns = ['date','wells','choke_size','uptime','thp','bhp','pstar','dp','oil',

                             'gas', 'water','bsw','gor']

        wells_df2['date']=pd.to_datetime(wells_df2['date']).dt.date

        wells_df2['choke_size']= wells_df2['choke_size'].astype(str).str.lower()

        wells_df2['choke_size']= wells_df2['choke_size'].replace(['shut in'],0)

        wells_df2[['choke_size','uptime', 'thp', 'bhp', 'pstar', 'dp', 'oil', 'gas', 'water', 'bsw', 'gor']] = wells_df2[['choke_size','uptime','thp', 

              'bhp', 'pstar', 'dp', 'oil', 'gas', 'water', 'bsw', 'gor']].apply(pd.to_numeric)

        wells_df2[['oil', 'water', 'gor']] =  wells_df2[['oil', 'water', 'gor']].round(0)

        wells_df2[['thp', 'bhp', 'pstar', 'dp']] = wells_df2[['thp', 'bhp', 'pstar', 'dp']].round(1)

        wells_df2[['gas', 'bsw']] = wells_df2[['gas', 'bsw']].round(2)

        wells_df2['uptime'] =wells_df2['uptime'].astype(float)

        wells_df2 = wells_df2.astype({'choke_size': 'int', 'oil':'int', 'water': 'int', 'gor': 'int'})

        return wells_df2
    
    def read_big_query_table():
    
        client = bigquery.Client()

        query_string = "SELECT * FROM `dummy-surveillance-project.ingest_data.production data table` "

        bq_table_df = pandas_gbq.read_gbq(query_string, project_id = 'dummy-surveillance-project')

        return bq_table_df
    
    def initial_cumulative_production():
      
        cumulative_production = {'well 4' : 4500000, 'well 5' : 4000000, 'well 7' : 3000000, 'well 9' : 3750000,

                                  'well 10' : 3200000, 'well 12': 2950000, 'well 14' : 2700000, 'well 16' :  2560000,

                                  'well 17' : 2470000, 'well 19' : 2150000, 'well 20' : 900000, 'well 21' : 720000}

        return cumulative_production
    
    def final_well_data():
    
        bq_table_df = read_big_query_table()

        final_wells_df = updated_wells_data()

        wells_unique_name = list(final_wells_df ['wells'].unique())

        well_order = CategoricalDtype(wells_unique_name, ordered = True)

        if list(bq_table_df['wells'].unique()) == []:

            final_wells_df['initial_cumulative_production'] = final_wells_df['wells'].map(initial_cumulative_production())

            final_wells_df['cumulative_production'] = final_wells_df['initial_cumulative_production'] + final_wells_df['oil']

            final_wells_df['cumulative_production'] = final_wells_df['cumulative_production'].astype(int)

            final_wells_df.drop(['initial_cumulative_production'], axis = 1, inplace = True)

            final_wells_df['wells'] = final_wells_df['wells'].astype(well_order)

            final_wells_df.sort_values(['wells', 'date'], inplace = True)

            return final_wells_df

        else:

            if final_wells_df['date'].unique() not in bq_table_df['date'].unique():

                bq_table_df['wells'] = bq_table_df['wells'].astype(well_order)

                bq_table_df.sort_values(['wells', 'date'], inplace = True)

                bq_table_df.reset_index(drop = True, inplace = True)

                last_cumulative_production = bq_table_df[bq_table_df['date'] ==

                                                                   bq_table_df['date'].unique().max()]['cumulative_production']

                last_cumulative_production.reset_index(drop = True, inplace = True)

                final_wells_df['cumulative_production'] = final_wells_df['oil'] + last_cumulative_production

                return final_wells_df

            else:

                bq_table_df['wells'] = bq_table_df['wells'].astype(well_order)

                bq_table_df.sort_values(['wells', 'date'], inplace = True)

                bq_table_df.reset_index(drop = True, inplace = True)

                previous_date = bq_table_df['date'].unique()[list(bq_table_df['date'].unique()).index(final_wells_df['date'].unique())-1]

                previous_cumulative_production = bq_table_df[bq_table_df['date'] ==

                                                                   previous_date]['cumulative_production']

                previous_cumulative_production.reset_index(drop = True, inplace = True)

                final_wells_df['cumulative_production'] = final_wells_df['oil'] + previous_cumulative_production

                final_wells_df['wells'] = final_wells_df['wells'].astype(well_order)

                final_wells_df.sort_values(['wells', 'date'], inplace = True)

                index = bq_table_df[bq_table_df['date'] == final_wells_df.iloc[0]['date']].index

                bq_table_df.drop(index, inplace = True)

                bq_table_df = pd.concat([bq_table_df, final_wells_df], axis = 0)

                bq_table_df.reset_index(drop = True, inplace = True)

                return bq_table_df
            
            
    def bq_table_schema():
    
        table_schema = [{'name':'date', 'type':'DATE'}, {'name':'wells', 'type':'STRING'},

                  {'name':'choke_size', 'type':'INTEGER'}, {'name':'uptime', 'type':'FLOAT'},

                  {'name':'thp', 'type':'FLOAT'}, {'name':'bhp', 'type':'FLOAT'},

                  {'name':'pstar', 'type':'FLOAT'}, {'name':'dp', 'type':'FLOAT'},

                  {'name':'oil', 'type':'INTEGER'}, {'name':'gas', 'type':'FLOAT'},

                  {'name':'water', 'type':'INTEGER'}, {'name':'bsw', 'type':'FLOAT'},

                  {'name':'gor', 'type':'FLOAT'}, {'name':'cumulative_production', 'type':'INTEGER'},

                     ]

        return table_schema
    
    def save_to_bq_table():
    
        bq_table_df = read_big_query_table()

        final_wells_df = updated_wells_data()

        if list(bq_table_df['wells'].unique()) == []:

            return final_well_data().to_gbq('ingest_data.production data table', if_exists = 'append', 

                                      table_schema = bq_table_schema(), project_id = 'dummy-surveillance-project')

        else:

            if final_wells_df['date'].unique() not in bq_table_df['date'].unique():

                return final_well_data().to_gbq('production_dataset.production data table', if_exists = 'append', 

                                         table_schema = bq_table_schema(), project_id = 'dummy-surveillance-project')

            else:

                return final_well_data().to_gbq('production_dataset.production data table', if_exists = 'replace', 

                                         table_schema = bq_table_schema(), project_id = 'dummy-surveillance-project')
      
    save_to_bq_table()

