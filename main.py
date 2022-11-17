#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

import datetime

import plotly.express as px

import dash

from google.cloud import bigquery

import pandas_gbq

import numpy

import dash_daq as daq

from dash import dcc, html

import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output


client = bigquery.Client()

query_string = "SELECT * FROM `dummy-surveillance-project.ingest_data.production data table` "

well_data  = pandas_gbq.read_gbq(query_string, project_id = 'dummy-surveillance-project')

well_data.set_index('date',inplace=True)

_app = dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])

app = _app.server

_app.layout = html.Div([
    
    dbc.Row([dbc.Col([html.Div([
        
        html.H1('Production Surveillance Dashboard',
                                       
                                       style = {'textAlign':'center', 'font-family':'Open Sans','letter-spacing':'1.5px','color':'white'}
                                      
                                      )
                                
                               ])
                     
                     ])
            
            ]),
    
    html.Br(),
    
    dbc.Row([dbc.Col([html.Div([
        
        html.H6('Last Update:' +' ' +(well_data.index[-1].strftime('%d-%b-%Y')),
                                       
                                       style={'textAlign':'right', 'font-size':'22px','font-family':'Open Sans','letter-spacing':'1.5px','color':'white'}
                                       
                                       )
                                
                               ])
                     
                     ])
            
            ]),
    
    html.Br(),
    
    
    dbc.Row([dbc.Col([html.Div([
        
        dcc.Dropdown(id='wells dropdown', options=[
            
            {'label': i, 'value': i} for i in well_data['wells'].unique()
            
        ], style={'width':'25%','font-family':'Open Sans','letter-spacing':'1.5px','color':'black'}, placeholder='Select a well')])
                     
                     ])
            
            ]),
    
    html.Br(),
    
    dbc.Row([dbc.Col([html.Div([
        
        dcc.Dropdown(id='wells properties dropdown', options=[
            
            {'label':'Rates and Cumulative','value':'rates and cumulatives'},
            
            {'label':'Pressures','value':'pressures'},
            
            {'label':'Water Cut and Gas Oil Ratio','value':'water cut and gas oil ratio'}
            
        ], style={'width':'25%','font-family':'Open Sans','letter-spacing':'1.5px','color':'black'}, placeholder='Select well properties')])
                     
                     ])
            
            ]),
    
    html.Br(),
    
    dbc.Row([dbc.Col([html.Div([
        
        
        dcc.DatePickerRange(
            
            id='my-date-picker-range',
            
            min_date_allowed=well_data.index[0],
            
            max_date_allowed=well_data.index[-1],
            
            initial_visible_month=well_data.index[-1],
            
            display_format='YYYY-MM-DD'
        
        ),
        
        
    ],style={'font-family':'Open Sans','letter-spacing':'1.5px','color':'black','font-size':'16px','width':'25%'})
        
        
    ])
        
        
    ]),
    
    html.Br(),
    
    html.Br(),
    
    html.Div(
        
        id='my-output'
                     
    ),  
    
], style={'margin':'30px'})

def output_1(well_uptime, uptime_label, choke_size_label, choke_size, heading_1, heading_2, heading_3, heading_4,
             
             figure_1, figure_2, figure_3, figure_4):
    
    output_1 = html.Div([
        
        dbc.Row([
            
            dbc.Col([
                
                html.Div([
                    
                    daq.Gauge(
                        
                        showCurrentValue=True,
                        
                        units = "Hours",
                
                        value = well_uptime,
                        
                        label = uptime_label,
                        
                        max=24,
                        
                        min=0),
                    
                ])
                
            ], md = {"size": 3, "offset": 6}),
            
            dbc.Col([
                
                html.Div([
                    
                    daq.GraduatedBar(
                        
                        label = (choke_size_label),
                        
                        value = choke_size,
                        
                        step = 2,
                        
                        max =192),
                ])
                
            ],align= 'center', md = 3)
            
        ], style={'font-family':'Open Sans','letter-spacing':'1.5px','color':'white', 'font-size':'20px'}),
        
        html.Br(),
        
        html.Br(),

        dbc.Row([

            dbc.Col([

                html.Div([

                    html.H6(heading_1,

                            style={'textAlign':'left','color':'white','font-size':'25px','font-family':'Open Sans'}),

                    html.Br(),

                    dcc.Graph(figure=figure_1)

                ])

            ],md=6),

            dbc.Col([

                html.Div([

                    html.H6(heading_2,

                            style={'textAlign':'left','color':'white','font-size':'25px','font-family':'Open Sans'}),

                    html.Br(),

                    dcc.Graph(figure=figure_2)

                ])

            ],md=6)

        ]),
        
        html.Br(),
        
        html.Br(),

        dbc.Row([

            dbc.Col([

                html.Div([

                    html.H6(heading_3,

                            style={'textAlign':'left','color':'white','font-size':'25px','font-family':'Open Sans'}),

                    html.Br(),

                    dcc.Graph(figure=figure_3)

                ])

            ],md=6),

            dbc.Col([

                html.Div([

                    html.H6(heading_4,

                            style={'textAlign':'left','color':'white','font-size':'25px','font-family':'Open Sans'}),

                    html.Br(),

                    dcc.Graph(figure=figure_4)

                ])

            ],md=6)

        ])  

    ])
    
    return output_1

def output_2(well_uptime, uptime_label, choke_size_label, choke_size, heading_1, heading_2, figure_1, figure_2):
    
    output_2=html.Div([
        
        dbc.Row([
            
            dbc.Col([
                
                html.Div([
                    
                    daq.Gauge(
                        
                        showCurrentValue=True,
                        
                        units = "Hours",
                
                        value = well_uptime,
                        
                        label=uptime_label,
                        
                        max=24,
                        
                        min=0),
                ])
                
            ], md = {"size": 3, "offset": 6}),
            
            dbc.Col([
                
                html.Div([
                    
                    daq.GraduatedBar(
                        
                        label = choke_size_label,
                        
                        value = choke_size,
                        
                        step = 2,
                        
                        max =192),
                ])
                
            ],align= 'center', md = 3)
            
        ], style={'height': '6%','font-family':'Open Sans','letter-spacing':'1.5px','color':'white', 'font-size':'20px'}),
        
        html.Br(),
        
        html.Br(),


        dbc.Row([

            dbc.Col([

                html.Div([

                    html.H6(heading_1,

                            style={'textAlign':'left','color':'white','font-size':'25px','font-family':'Open Sans'}),

                    html.Br(),

                    dcc.Graph(figure=figure_1)

                ])

            ],md=6),

            dbc.Col([

                html.Div([

                    html.H6(heading_2,

                            style={'textAlign':'left','color':'white','font-size':'25px','font-family':'Open Sans'}),

                    html.Br(),

                    dcc.Graph(figure=figure_2)

                ])

            ],md=6)

        ])
        
    ])
    
    return output_2


@_app.callback(
    
    Output('my-output','children'),
    
    Input('wells dropdown','value'),
    
    Input('wells properties dropdown','value'),
    
    Input('my-date-picker-range','start_date'),
    
    Input('my-date-picker-range','end_date'))

def plot_update(wells_name, wells_properties, start_date, end_date):
    
    well_data_filter=well_data[well_data['wells']==wells_name]
    
    well_data_filter_date=well_data_filter.loc[start_date:end_date]
    
    well_data_filter_date['cumulative production bbls']=well_data_filter_date['oil bopd'].cumsum(axis=0)
    
    if wells_name and wells_properties and start_date and end_date is None:
        
        return None
    
    elif wells_properties=='rates and cumulatives' and start_date is None and end_date is None:
        
        output1=output_1(
            
            well_uptime = well_data_filter['uptime hrs'].iloc[-1],
            
            uptime_label = 'Uptime',
            
            choke_size_label = 'Choke Size:' + ' ' + str(well_data_filter['choke size'].iloc[-1])+'/192' + ' ' + 'inches',
            
            choke_size = well_data_filter['choke size'].iloc[-1],
            
            heading_1='Oil Production Rate', 
    
            heading_2='Gas Production Rate', 

            heading_3='Water Production Rate', 

            heading_4='Cumulative Production',

            figure_1=px.line(well_data_filter, y='oil bopd', color_discrete_sequence=['green']

                                                    ).update_layout(

                title='<b>'+'Oil Production:'+' '+ str(well_data_filter['oil bopd'].iloc[-1])+' '+ 'bopd'+ '</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True),

            figure_2=px.line(well_data_filter,y='gas mmscfd', color_discrete_sequence=['red']

                                                    ).update_layout(

                title='<b>'+'Gas Production:'+' '+ str(well_data_filter['gas mmscfd'].iloc[-1])+' '+ 'mmscfd'+'</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True),

            figure_3=px.line(well_data_filter,y='water bwpd', color_discrete_sequence=['blue']

                                     ).update_layout(

              title='<b>'+'Water Production:'+' '+ str(well_data_filter['water bwpd'].iloc[-1])+' '+  'bwpd'+'</b>',

              template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True),

            figure_4=px.line(well_data_filter,y='cumulative production bbls', color_discrete_sequence=['green']

                                     ).update_layout(

                title='<b>'+'Cumulative Production:'+' '+str(well_data_filter['cumulative production bbls'].iloc[-1])+' '+ 'bbls'+'</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True))
        
        return output1
    
    elif wells_properties=='pressures' and start_date is None and end_date is None:
        
        output2=output_1(
            
            well_uptime = well_data_filter['uptime hrs'].iloc[-1],
            
            uptime_label = 'Uptime',
            
            choke_size_label = 'Choke Size:' + ' ' + str(well_data_filter['choke size'].iloc[-1])+'/192' + ' ' + 'inches',
            
            choke_size = well_data_filter['choke size'].iloc[-1],
            
            heading_1='P*', 
    
            heading_2='BHP', 

            heading_3='THP', 

            heading_4='Drawdown',

            figure_1=px.line(well_data_filter, y='p* psi', color_discrete_sequence=['red']

                                                    ).update_layout(

                title='<b>'+'P*:'+' '+ str(well_data_filter['p* psi'].iloc[-1])+' '+ 'psi'+ '</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True),

            figure_2=px.line(well_data_filter,y='bhp psi', color_discrete_sequence=['red']

                                                    ).update_layout(

                title='<b>'+'BHP:'+' '+ str(well_data_filter['bhp psi'].iloc[-1])+' '+ 'psi'+'</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True),

            figure_3=px.line(well_data_filter,y='thp psi', color_discrete_sequence=['red']

                                     ).update_layout(

              title='<b>'+'THP:'+' '+ str(well_data_filter['thp psi'].iloc[-1])+' '+  'psi'+'</b>',

              template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True),

            figure_4=px.line(well_data_filter,y='dp psi', color_discrete_sequence=['red']

                                     ).update_layout(

                title='<b>'+'Drawdown :'+' '+ str(well_data_filter['dp psi'].iloc[-1])+' '+ 'psi'+'</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True))
        
        return output2
    
    elif wells_properties=='water cut and gas oil ratio' and start_date is None and end_date is None:
        
        output3=output_2(
            
            well_uptime = well_data_filter['uptime hrs'].iloc[-1],
            
            uptime_label = 'Uptime',
            
            choke_size_label = 'Choke Size:' + ' ' + str(well_data_filter['choke size'].iloc[-1])+'/192' + ' ' + 'inches',
            
            choke_size = well_data_filter['choke size'].iloc[-1],
            
            heading_1='BS&W', 
    
            heading_2='GOR', 

            figure_1=px.line(well_data_filter, y='bs&w %', color_discrete_sequence=['blue']

                                                    ).update_layout(

                title='<b>'+'BS&W:'+' '+ str(well_data_filter['bs&w %'].iloc[-1])+' '+ '%'+ '</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(range=[0,100],fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True),

            figure_2=px.line(well_data_filter,y='gor scf/bbl', color_discrete_sequence=['red']

                                                    ).update_layout(

                title='<b>'+'GOR:'+' '+ str(well_data_filter['gor scf/bbl'].iloc[-1])+' '+ 'scf/bbl'+'</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True))
        
        return output3
    
    elif wells_properties=='rates and cumulatives' and start_date is not None and end_date is not None:
        
        output4=output_1(
            
            well_uptime = round(well_data_filter_date['uptime hrs'].mean(),2),
            
            uptime_label = 'Average Uptime',
            
            choke_size_label = 'Choke Size:' + ' ' + str(well_data_filter_date['choke size'].iloc[-1])+'/192' + ' ' + 'inches',
            
            choke_size = well_data_filter_date['choke size'].iloc[-1],
            
            heading_1='Oil Production Rate', 
    
            heading_2='Gas Production Rate', 

            heading_3='Water Production Rate', 

            heading_4='Cumulative Production',

            figure_1=px.line(well_data_filter_date, y='oil bopd', color_discrete_sequence=['green']

                                                    ).update_layout(

                title='<b>'+'Average Oil Production:'+' '+ str(round(well_data_filter_date['oil bopd'].mean()))+' '+ 'bopd'+ '</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True),

            figure_2=px.line(well_data_filter_date,y='gas mmscfd', color_discrete_sequence=['red']

                                                    ).update_layout(

                title='<b>'+'Average Gas Production:'+' '+ str(round(well_data_filter_date['gas mmscfd'].mean()))+' '+ 'mmscfd'+'</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True),

            figure_3=px.line(well_data_filter_date,y='water bwpd', color_discrete_sequence=['blue']

                                     ).update_layout(

              title='<b>'+'Average Water Production:'+' '+ str(round(well_data_filter_date['water bwpd'].mean()))+' '+  'bwpd'+'</b>',

              template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True),

            figure_4=px.line(well_data_filter_date,y='cumulative production bbls', color_discrete_sequence=['green']

                                     ).update_layout(

                title='<b>'+'Cumulative Production:'+' '+str(well_data_filter_date['oil bopd'].sum(axis = 0, skipna = True))+' '+ 'bbls'+'</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True))
        
        return output4
    
    elif wells_properties=='pressures' and start_date is not None and end_date is not None:
        
        output5=output_1(
            
            well_uptime = round(well_data_filter_date['uptime hrs'].mean(),2),
            
            uptime_label = 'Average Uptime',
            
            choke_size_label = 'Choke Size:' + ' ' + str(well_data_filter_date['choke size'].iloc[-1])+'/192' + ' ' + 'inches',
            
            choke_size = well_data_filter_date['choke size'].iloc[-1],
            
            heading_1='P*', 
    
            heading_2='BHP', 

            heading_3='THP', 

            heading_4='Drawdown',

            figure_1=px.line(well_data_filter_date, y='p* psi', color_discrete_sequence=['red']

                                                    ).update_layout(

                title='<b>'+'P*:'+' '+ str(well_data_filter_date['p* psi'].iloc[-1])+' '+ 'psi'+ '</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True),

            figure_2=px.line(well_data_filter_date,y='bhp psi', color_discrete_sequence=['red']

                                                    ).update_layout(

                title='<b>'+'BHP:'+' '+ str(well_data_filter_date['bhp psi'].iloc[-1])+' '+ 'psi'+'</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True),

            figure_3=px.line(well_data_filter,y='thp psi', color_discrete_sequence=['red']

                                     ).update_layout(

              title='<b>'+'THP:'+' '+ str(well_data_filter_date['thp psi'].iloc[-1])+' '+  'psi'+'</b>',

              template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True),

            figure_4=px.line(well_data_filter_date,y='dp psi', color_discrete_sequence=['red']

                                     ).update_layout(

                title='<b>'+'Drawdown:'+' '+ str(well_data_filter_date['dp psi'].iloc[-1])+' '+ 'psi'+'</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True))
        
        return output5
    
    elif wells_properties=='water cut and gas oil ratio' and start_date is None and end_date is not None:
        
        output6=output_2(
            
            well_uptime = round(well_data_filter_date['uptime hrs'].mean(),2),
            
            uptime_label = 'Average Uptime',
            
            choke_size_label = 'Choke Size:' + ' ' + str(well_data_filter_date['choke size'].iloc[-1])+'/192' + ' ' + 'inches',
            
            choke_size = well_data_filter_date['choke size'].iloc[-1],
            
            heading_1='BS&W', 
    
            heading_2='GOR', 

            figure_1=px.line(well_data_filter_date, y='bs&w %', color_discrete_sequence=['blue']

                                                    ).update_layout(

                title='<b>'+'BS&W:'+' '+ str(well_data_filter_date['bs&w %'].iloc[-1])+' '+ '%'+ '</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(range=[0,100], fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True),

            figure_2=px.line(well_data_filter_date,y='gor scf/bbl', color_discrete_sequence=['red']

                                                    ).update_layout(

                title='<b>'+'GOR:'+' '+ str(well_data_filter_date['gor scf/bbl'].iloc[-1])+' '+ 'scf/bbl'+'</b>',

                template='plotly_dark',plot_bgcolor='#32383E',paper_bgcolor='#32383E', title_font_color='white',title_font_size=23,title_font_family='Open Sans').
            
            update_yaxes(rangemode='tozero',fixedrange=True).update_xaxes(fixedrange=True))
        
        return output6
    
    else:
        
        return None
    
    
if __name__ == '__main__':

    _app.run_server(debug=True)



# In[ ]:




