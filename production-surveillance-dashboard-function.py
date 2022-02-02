from google.cloud import storage

import pandas as pd

import datetime

import xlrd

import openpyxl

import fsspec

import gcsfs

import itertools

def production_surveillance(event, context):
  
  storage_client = storage.Client()

  prefix='Daily Production Report'

  blobs = storage_client.list_blobs('field-production-reports',prefix=prefix)

  date_list=[]

  wells_list=[]

  for blob in blobs:
    
    data_bytes = blob.download_as_bytes()

    df = pd.read_excel(data_bytes)

    date=df.iloc[2:3,6:7]

    wells_df=df.iloc[33:47,0:19]

    date_list.append(date)

    wells_list.append(wells_df)

  K=12

  date_list = list(itertools.chain.from_iterable(itertools.repeat(i, K) for i in date_list))

  date_df=pd.concat(date_list,axis=0)

  date_df.columns=['next_date']

  date_df['next_date']=date_df['next_date'].astype('string')

  date_df['next_date']=date_df['next_date'].str.replace(' at 08:00 AM',' ')

  date_df['next_date']=pd.to_datetime(date_df['next_date']).dt.date

  date_df['date']=(date_df['next_date']-datetime.timedelta(days=1))

  date_df.drop(['next_date'],axis=1,inplace=True)

  date_df=date_df.reset_index(drop=True)


  wells_df2=pd.concat(wells_list, axis=0)

  wells_df2.drop([36,39],axis=0,inplace=True)

  wells_df2=wells_df2.reset_index(drop=True)


  well_data=pd.concat([date_df,wells_df2],axis=1)

  well_data.drop(['Unnamed: 2','Unnamed: 3','Unnamed: 4','Unnamed: 6','Unnamed: 7','Unnamed: 12','Unnamed: 14','Unnamed: 17'],axis=1,inplace=True)

  well_data.columns=['date','wells','choke size','fthp psi','bhp psi','p* psi','dp psi','oil bopd','gas mmscfd','water bwpd','bs&w %','gor scf/bbl']

  well_data['wells']=well_data['wells'].astype(str).replace(['OK20 '] ,'OK20')

  well_data['choke size']= well_data['choke size'].astype(str).str.lower()

  well_data['choke size']= well_data['choke size'].replace(['shut in'],0)

  wells_unique_list=(well_data['wells'].unique())


  cumulative_production_list=[]

  for wells in wells_unique_list:
    
    cumulative_production=well_data[well_data['wells']==wells]['oil bopd'].cumsum(axis=0)
      
    cumulative_production=2000000+cumulative_production
    
    cumulative_production_list.append(cumulative_production)

  cumulative_production_df=pd.concat(cumulative_production_list,axis=0)

  cumulative_production_df.sort_index(inplace=True)


  well_data=pd.concat([well_data,cumulative_production_df],axis=1)

  well_data.columns=['date','wells','choke size','fthp psi','bhp psi','p* psi','dp psi','oil bopd','gas mmscfd','water bwpd','bs&w %','gor scf/bbl','cumulative production bbls']

  well_data['date']=pd.to_datetime(well_data['date']).dt.date

  well_data['oil bopd']=well_data['oil bopd'].apply(pd.to_numeric)

  well_data['oil bopd']=well_data['oil bopd'].round(0)

  well_data['gas mmscfd']=well_data['gas mmscfd'].apply(pd.to_numeric)

  well_data['gas mmscfd']=well_data['gas mmscfd'].round(2)

  well_data['water bwpd']=well_data['water bwpd'].apply(pd.to_numeric)

  well_data['water bwpd']=well_data['water bwpd'].round(0)

  well_data['bs&w %']=well_data['bs&w %'].apply(pd.to_numeric)

  well_data['bs&w %']=well_data['bs&w %'].round(2)

  well_data['gor scf/bbl']=well_data['gor scf/bbl'].apply(pd.to_numeric)

  well_data['gor scf/bbl']=well_data['gor scf/bbl'].round(0)

  well_data['cumulative production bbls']=well_data['cumulative production bbls'].apply(pd.to_numeric)

  well_data['cumulative production bbls']=well_data['cumulative production bbls'].round(0)

  well_data.sort_values(by='date', inplace=True)

  well_data.to_excel('gs://well_data_bucket/well_data.xlsx',index=False)


