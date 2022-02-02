#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd

import datetime

import plotly.express as px

import dash

import numpy

from dash import dcc

from dash import html

import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output


well_data=pd.read_excel(r'C:\Users\Oladayo\Downloads\well_data.xlsx')

well_data.set_index('date',inplace=True)


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])

app=app.server

app.layout=html.Div([
    
    html.H1(children='Production Surveillance Dashboard',
            
            style={
                
                'textAlign': 'center',
                
                'color': '#FFFFFF',
                
                'font-size': 50
                
                
            }
           ),
    
    html.Br(),
    
    html.H6(children='Last Update:'+ ' '+ (well_data.index[-1].strftime('%d-%b-%Y')),
                
                style={
                    
                    'textAlign': 'right',
                    
                    'color':'#FFFFFF',
                    
                    'font-size':20
                
                }
               
               ),
    
    html.Br(),
    
    html.Label('Select a well'),
    
    dcc.Dropdown(
        
        id='wells_dropdown',
        
        options=[
            
            {'label':'OK4ST','value':'OK4ST'},
            {'label':'OK5ST2','value':'OK5ST2'},
            {'label':'OK7','value':'OK7'},
            {'label':'OK9','value':'OK9'},
            {'label':'OK10','value':'OK10'},
            {'label':'OK12ST1','value':'OK12ST1'},
            {'label':'OK14ST','value':'OK14ST'},
            {'label':'OK16','value':'OK16'},
            {'label':'OK17','value':'OK17'},
            {'label':'OK19','value':'OK19'},
            {'label':'OK20','value':'OK20'},
            {'label':'OK21','value':'OK21'},
        
        ], style={'width':'40%','color':'#000000'}
        
    ),
    
    html.Br(),
    
    html.Label('Select well properties'),
    
    dcc.Dropdown(
        
        id='wells_properties_dropdown',
        
        options=[
            {'label':'Rates','value':'Well_Rates'},
            {'label':'Pressures','value':'Well_Pressures'},
            {'label':'Water Cut/GOR','value':'Water_Cut_Gor'},
            
        ],style={'width':'40%','color':'#000000'}
    
    ),
    
    html.Br(),
    
    dcc.DatePickerRange(
            
            id='my-date-picker-range',
            
            min_date_allowed=well_data.index[0],
            
            max_date_allowed=well_data.index[-1],
            
            initial_visible_month=well_data.index[-1],
            
            display_format='YYYY-MM-DD'
        
        ),
    
    html.Br(),
    
    html.Br(),
    
    html.Div(id='output-container-dropdown'),       
    
])


@app.callback(
    
    Output('output-container-dropdown','children'),
    
    Input('wells_dropdown','value'),
    
    Input('wells_properties_dropdown','value'),

    Input('my-date-picker-range','start_date'),

    Input('my-date-picker-range','end_date'))

def update_graph(wells_name,wells_properties,start_date,end_date):
    
    well_data_filtered=well_data[well_data['wells']==wells_name]
    
    well_data_filtered_date=well_data_filtered.loc[start_date:end_date] 
    
    well_data_filtered_date['cumulative production bbls']=well_data_filtered_date['oil bopd'].cumsum(axis=0)
    
    if wells_name and wells_properties and start_date and end_date is None:
        
        return None
    
    elif wells_properties=='Well_Rates' and start_date is None and end_date is None:
        
        output1=html.Div([
            
            dbc.Row([
            
                dbc.Col([
                
                    html.H6(children='Oil Production Rate',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered,x=well_data_filtered.index, y='oil bopd', color_discrete_sequence=['green']
                                         
                                            ).update_layout(
                    
                        template='plotly_dark',
                    
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                    
                        title='<b>'+'Oil Production:'+' '+ str(well_data_filtered['oil bopd'].iloc[-1])+' '+ 'bopd'+ '</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
            
                ],md=6),
            
                dbc.Col([
                
                    html.H6(children='Gas Production Rate',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered,x=well_data_filtered.index,y='gas mmscfd', color_discrete_sequence=['red']
                                         
                                            ).update_layout(
                    
                        template='plotly_dark',
        
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                          
                        title='<b>'+'Gas Production:'+' '+ str(well_data_filtered['gas mmscfd'].iloc[-1])+' '+ 'mmscfd'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
                
                ],md=6),
            
            ],align='center'),
            
            html.Br(),
        
            html.Br(),
        
            dbc.Row([
            
                dbc.Col([
                
                    html.H6(children='Water Production Rate',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered,x=well_data_filtered.index,y='water bwpd', color_discrete_sequence=['blue']
                         
                             ).update_layout(
                    
                        template='plotly_dark',
        
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                            
                        title='<b>'+'Water Production:'+' '+ str(well_data_filtered['water bwpd'].iloc[-1])+' '+ 'bwpd'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
            
                ],md=6),
            
                dbc.Col([
                
                    html.H6(children='Cumulative Production',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered,x=well_data_filtered.index,y='cumulative production bbls', color_discrete_sequence=['green']
                         
                             ).update_layout(
                    
                        template='plotly_dark',
        
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
        
                        title='<b>'+'Cumulative Production :'+' '+str(well_data_filtered['cumulative production bbls'].iloc[-1])+' '+ 'bbls'+'</b>',
                      
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
            
                ],md=6),
        
            ],align='center')
    
        ])
        
        return output1
    
    elif wells_properties=='Well_Pressures' and start_date is None and end_date is None:
        
        output2=html.Div([
            
            dbc.Row([
            
                dbc.Col([
                
                    html.H6(children='P*',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered,x=well_data_filtered.index, y='p* psi', color_discrete_sequence=['red']
                                         
                                            ).update_layout(
                    
                        template='plotly_dark',
                    
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                    
                        title='<b>'+'P*:'+' '+ str(round(well_data_filtered['p* psi'].iloc[-1],2))+' '+ 'psi'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
            
                ],md=6),
            
                dbc.Col([
                
                    html.H6(children='BHP',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered,x=well_data_filtered.index,y='bhp psi', color_discrete_sequence=['red']
                                         
                                            ).update_layout(
                    
                        template='plotly_dark',
        
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                          
                        title='<b>'+'BHP:'+' '+ str(round(well_data_filtered['bhp psi'].iloc[-1],2))+' '+ 'psi'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
                
                ],md=6),
            
            ],align='center'),
            
            html.Br(),
        
            html.Br(),
        
            dbc.Row([
            
                dbc.Col([
                
                    html.H6(children='FTHP',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered,x=well_data_filtered.index,y='fthp psi', color_discrete_sequence=['red']
                         
                             ).update_layout(
                    
                        template='plotly_dark',
        
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                            
                        title='<b>'+'FTHP:'+' '+ str(round(well_data_filtered['fthp psi'].iloc[-1],2))+' '+ 'psi'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
            
                ],md=6),
            
                dbc.Col([
                
                    html.H6(children='Drawdown',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered,x=well_data_filtered.index,y='dp psi', color_discrete_sequence=['red']
                         
                             ).update_layout(
                    
                        template='plotly_dark',
        
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
        
                        title='<b>'+'Drawdown :'+' '+str(round(well_data_filtered['dp psi'].iloc[-1]))+' '+ 'psi'+'</b>',
                      
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True).update_xaxes(fixedrange=True))
            
                ],md=6),
        
            ],align='center')
    
        ])
        
        return output2
    
    elif wells_properties=='Water_Cut_Gor' and start_date is None and end_date is None:
        
        output3=html.Div([
            
            dbc.Row([
            
                dbc.Col([
                
                    html.H6(children='BS&W',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered,x=well_data_filtered.index, y='bs&w %', color_discrete_sequence=['blue']
                                         
                                            ).update_layout(
                    
                        template='plotly_dark',
                    
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                    
                        title='<b>'+'BS&W:'+' '+ str(round(well_data_filtered['bs&w %'].iloc[-1],2))+' '+ '%'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(range=[0,100],fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
            
                ],md=6),
            
                dbc.Col([
                
                    html.H6(children='GOR',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered,x=well_data_filtered.index,y='gor scf/bbl', color_discrete_sequence=['red']
                                         
                                            ).update_layout(
                    
                        template='plotly_dark',
        
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                          
                        title='<b>'+'GOR:'+' '+ str(round(well_data_filtered['gor scf/bbl'].iloc[-1]))+' '+ 'scf/bbl'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
                
                ],md=6),
            
            ],align='center')
            
        ])
        
        return output3
    
    elif wells_properties=='Well_Rates' and start_date is not None and end_date is not None:
        
        output4=html.Div([
            
            dbc.Row([
            
                dbc.Col([
                
                    html.H6(children='Oil Production Rate',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered_date,well_data_filtered_date.index, y='oil bopd', color_discrete_sequence=['green']
                                         
                                            ).update_layout(
                    
                        template='plotly_dark',
                    
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                    
                        title='<b>'+'Average Oil Production:'+' '+ str(round(well_data_filtered_date['oil bopd'].mean()))+' '+ 'bopd'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
            
                ],md=6),
            
                dbc.Col([
                
                    html.H6(children='Gas Production Rate',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered_date,x=well_data_filtered_date.index,y='gas mmscfd', color_discrete_sequence=['red']
                                         
                                            ).update_layout(
                    
                        template='plotly_dark',
        
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                          
                        title='<b>'+'Average Gas Production:'+' '+ str(round(well_data_filtered_date['gas mmscfd'].mean(),2))+' '+ 'mmscfd'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
                
                ],md=6),
            
            ],align='center'),
            
            html.Br(),
        
            html.Br(),
        
            dbc.Row([
            
                dbc.Col([
                
                    html.H6(children='Water Production Rate',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered_date,x=well_data_filtered_date.index,y='water bwpd', color_discrete_sequence=['blue']
                         
                             ).update_layout(
                    
                        template='plotly_dark',
        
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                            
                        title='<b>'+'Average Water Production:'+' '+ str(round(well_data_filtered_date['water bwpd'].mean()))+' '+ 'bwpd'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
            
                ],md=6),
            
                dbc.Col([
                
                    html.H6(children='Cumulative Production',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered_date,x=well_data_filtered_date.index,y='cumulative production bbls', color_discrete_sequence=['green']
                         
                             ).update_layout(
                    
                        template='plotly_dark',
        
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
        
                        title='<b>'+'Cumulative Production :'+' '+str(well_data_filtered_date['oil bopd'].sum(axis = 0, skipna = True))+' '+ 'bbls'+'</b>',
                      
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
            
                ],md=6),
        
            ],align='center')
    
        ])
        
        return output4
    
    elif wells_properties=='Well_Pressures' and start_date is not None and end_date is not None:
        
        output5=html.Div([
            
            dbc.Row([
            
                dbc.Col([
                
                    html.H6(children='P*',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered_date, x=well_data_filtered_date.index, y='p* psi', color_discrete_sequence=['red']
                                         
                                            ).update_layout(
                    
                        template='plotly_dark',
                    
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                    
                        title='<b>'+'P*:'+' '+ str(round(well_data_filtered_date['p* psi'].iloc[-1],2))+' '+ 'psi'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
            
                ],md=6),
            
                dbc.Col([
                
                    html.H6(children='BHP',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered_date,x=well_data_filtered_date.index,y='bhp psi', color_discrete_sequence=['red']
                                         
                                            ).update_layout(
                    
                        template='plotly_dark',
        
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                          
                        title='<b>'+'BHP:'+' '+ str(round(well_data_filtered_date['bhp psi'].iloc[-1],2))+' '+ 'psi'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
                
                ],md=6),
            
            ],align='center'),
            
            html.Br(),
        
            html.Br(),
        
            dbc.Row([
            
                dbc.Col([
                
                    html.H6(children='FTHP',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered_date,x=well_data_filtered_date.index,y='fthp psi', color_discrete_sequence=['red']
                         
                             ).update_layout(
                    
                        template='plotly_dark',
        
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                            
                        title='<b>'+'FTHP:'+' '+ str(round(well_data_filtered_date['fthp psi'].iloc[-1],2))+' '+ 'psi'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
            
                ],md=6),
            
                dbc.Col([
                
                    html.H6(children='Drawdown',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered_date,x=well_data_filtered_date.index,y='dp psi', color_discrete_sequence=['red']
                         
                             ).update_layout(
                    
                        template='plotly_dark',
        
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
        
                        title='<b>'+'Drawdown :'+' '+str(round(well_data_filtered_date['dp psi'].iloc[-1]))+' '+ 'psi'+'</b>',
                      
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True).update_xaxes(fixedrange=True))
            
                ],md=6),
        
            ],align='center')
    
        ])
        
        return output5
    
    elif wells_properties=='Water_Cut_Gor' and start_date is not None and end_date is not None:
        
        output6=html.Div([
            
            dbc.Row([
            
                dbc.Col([
                
                    html.H6(children='BS&W',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered_date,x=well_data_filtered_date.index, y='bs&w %', color_discrete_sequence=['blue']
                                         
                                            ).update_layout(
                    
                        template='plotly_dark',
                    
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                    
                        title='<b>'+'BS&W:'+' '+ str(round(well_data_filtered_date['bs&w %'].iloc[-1],2))+' '+ '%'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(range=[0,100],fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
            
                ],md=6),
            
                dbc.Col([
                
                    html.H6(children='GOR',
                        
                            style={
                            
                                'textAlign': 'left',
                            
                                'color':'#FFFFFF',
                            
                                'font-size':25
                        
                            }
                       
                           ),
                
                    html.Br(),
                
                    dcc.Graph(figure=px.line(well_data_filtered_date,x=well_data_filtered_date.index,y='gor scf/bbl', color_discrete_sequence=['red']
                                         
                                            ).update_layout(
                    
                        template='plotly_dark',
        
                        plot_bgcolor='#32383E',
        
                        paper_bgcolor='#32383E',
                          
                        title='<b>'+'GOR:'+' '+ str(round(well_data_filtered_date['gor scf/bbl'].iloc[-1]))+' '+ 'scf/bbl'+'</b>',
                            
                        title_font_color='white',
        
                        title_font_size=23,
                  
                        title_font_family='Cambria').update_yaxes(fixedrange=True,rangemode='nonnegative').update_xaxes(fixedrange=True))
                
                ],md=6),
            
            ],align='center')
            
        ])
        
        return output6
    
    else:
        
        return None
    
if __name__ == '__main__':

    app.run_server(debug=True)
                   


# In[ ]:




