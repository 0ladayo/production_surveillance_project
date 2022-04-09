from google.cloud import storage

import pandas as pd

import datetime

import xlrd

import openpyxl

import fsspec

import gcsfs

import itertools

def dummy_function(event, context):
    
  def data():
      
      storage_client = storage.Client()

      prefix = 'Daily Production Report'

      blobs = storage_client.list_blobs('dummy-field-reports', prefix = prefix)

      date_list = []

      wells_list = []
  
      for blob in blobs:
          
          data_bytes = blob.download_as_bytes()
          
          df = pd.read_excel(data_bytes)
      
          date = df.iloc[2,6]
      
          wells = df.iloc[33:47,0:19]
      
          date_list.append(date)
      
          wells_list.append(wells)
      
      K = 12
      
      date_list = list(itertools.chain.from_iterable(itertools.repeat(i, K) for i in date_list))

      return date_list, wells_list
  
  date_list, wells_list = data()

  def date_data():
      
      date_df = pd.DataFrame(date_list)

      date_df.columns = ['next_date']

      date_df['next_date'] = date_df['next_date'].astype('string')

      date_df['next_date'] = date_df['next_date'].str.replace(' at 08:00 AM',' ')

      date_df['next_date'] = pd.to_datetime(date_df['next_date']).dt.date

      date_df['date'] = (date_df['next_date'] - datetime.timedelta(days=1))

      date_df.drop(['next_date'],axis = 1,inplace = True)

      date_df = date_df.reset_index(drop = True)
      
      return date_df
      
  date_df = date_data()

  def wells_data():
      
      wells_df = pd.concat(wells_list, axis = 0)
      
      wells_df.drop([36,39],axis = 0, inplace = True)
      
      wells_df.drop(['Unnamed: 2','Unnamed: 4','Unnamed: 6','Unnamed: 7','Unnamed: 12','Unnamed: 14',
                  
                  'Unnamed: 17'],axis = 1,inplace = True)

      wells_df = wells_df.reset_index(drop = True)
      
      return wells_df

  wells_df = wells_data()

  def wells_data2():
      
      wells_df2 = pd.concat([date_df, wells_df], axis = 1)
      
      wells_df2.columns = ['date','wells','choke size','uptime hrs','thp psi','bhp psi','p* psi','dp psi','oil bopd','gas mmscfd',
                          
                          'water bwpd','bs&w %','gor scf/bbl']
      
      wells_df2['date']=pd.to_datetime(wells_df2['date']).dt.date
      
      wells_df2['choke size']= wells_df2['choke size'].astype(str).str.lower()

      wells_df2['choke size']= wells_df2['choke size'].replace(['shut in'],0)

      wells_df2[['choke size','uptime hrs', 'thp psi', 'bhp psi', 'p* psi', 'dp psi', 'oil bopd', 'gas mmscfd', 'water bwpd', 'bs&w %', 'gor scf/bbl']] = wells_df2[['choke size','uptime hrs','thp psi', 
                                                                                                                              
              'bhp psi', 'p* psi', 'dp psi', 'oil bopd', 'gas mmscfd', 'water bwpd', 'bs&w %', 'gor scf/bbl']].apply(pd.to_numeric)
      
      wells_df2[['oil bopd', 'water bwpd', 'gor scf/bbl']] =  wells_df2[['oil bopd', 'water bwpd', 'gor scf/bbl']].round(0)
      
      wells_df2[['thp psi', 'bhp psi', 'p* psi', 'dp psi']] = wells_df2[['thp psi', 'bhp psi', 'p* psi', 'dp psi']].round(1)
      
      wells_df2[['gas mmscfd', 'bs&w %']] = wells_df2[['gas mmscfd', 'bs&w %']].round(2)
      
      wells_df2 = wells_df2.astype({'choke size': 'int', 'oil bopd':'int', 'water bwpd': 'int', 'gor scf/bbl': 'int'})

      return wells_df2

  wells_df2 = wells_data2()

  def initial_cumulative_production():
      
      cumulative_production_dic = {'well 4' : 4500000, 'well 5' : 4000000, 'well 7' : 3000000, 'well 9' : 3750000,
                                  
                                  'well 10' : 3200000, 'well 12': 2950000, 'well 14' : 2700000, 'well 16' :  2560000,
                                  
                                  'well 17' : 2470000, 'well 19' : 2150000, 'well 20' : 900000, 'well 21' : 720000 }
      
      wells_df2['initial cumulative production bbls'] = wells_df2['wells'].map(cumulative_production_dic)
      
      return wells_df2

  wells_df2 = initial_cumulative_production()

  def structured_well_data():
      
      cumulative_production_list = []
      
      wells_names = wells_df2['wells'].unique()
      
      for well in wells_names:
          
          cumulative_production=wells_df2[wells_df2['wells'] == well]['oil bopd'].cumsum(axis=0)
          
          cumulative_production_list.append(cumulative_production)
          
      cumulative_production_df = pd.concat(cumulative_production_list, axis = 0)
      
      cumulative_production_df.sort_index(inplace = True)
      
      wells_df3 = pd.concat([wells_df2, cumulative_production_df], axis = 1)
      
      wells_df3.columns = ['date','wells','choke size','uptime hrs','thp psi','bhp psi','p* psi','dp psi','oil bopd','gas mmscfd',
                          
                          'water bwpd','bs&w %','gor scf/bbl','initial cumulative production bbls',
                          
                          'periodic_cumulative production bbls']
      
      wells_df3['cumulative production bbls'] = wells_df3['initial cumulative production bbls'] + wells_df3['periodic_cumulative production bbls']
      
      wells_df3.drop(['initial cumulative production bbls', 'periodic_cumulative production bbls'], axis = 1, inplace = True)
      
      return wells_df3

  wells_df3 = structured_well_data()

  wells_df3.to_excel('gs://dummy-well-data/dummy well data.xlsx', index = False)
