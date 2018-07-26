
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import psycopg2
import os 
import dash_html_components as html

'''
#reading in data
applicants = pd.read_csv('~/dev/play-dash/applicants.csv')

#by bootcamp, online, or school                                                                                                                                    
general = applicants.groupby(['is_bootcamp', 'round']).size().to_frame('counts').reset_index()

#by individual school
school_ppl = applicants.loc[applicants.is_bootcamp == 'School']
school_ppl = school_ppl.groupby(['source', 'round']).size().to_frame('counts').reset_index()

#by individual bootcamp
bootcamp_ppl = applicants.loc[applicants.is_bootcamp == 'Bootcamp']
bootcamp_ppl = bootcamp_ppl.groupby(['source', 'round']).size().to_frame('counts').reset_index()'''

#given a dataframe will pivot according to source, and sum to see each of the rounds
def get_counts(df, col):
    p = df.pivot(index=col, columns='round', values='counts').fillna(0)
    by_school = p[['Onboarding', 
                   'Offer', 
                   'Second Interview',
                   'Take-Home Challenge',
                   'First Interview',
                   'Submitted Application']]
    summed = by_school.cumsum(axis=1).drop('Onboarding', axis=1)
    return summed


def get_percents(df):
    df['summy'] = df.sum(axis=1)
    percents = df.apply(lambda x: x/df['summy'], axis=0)
    p_sorted = percents[['Submitted Application', 'First Interview', 'Take-Home Challenge', 'Second Interview', 'Offer']]
    return p_sorted

def create_traces(p_df, v_df):
    trace_list = []
    colorlist = ['#1a3c40', '#144d53', '#307672','#b7e1b5', '#e4eddb']
    c = 0
    for col in p_df.columns:
        trace=go.Bar(y = p_df.index,
                     x = p_df[col], 
                     name=str(col),
                     text = list('count :' + v_df[col].astype(str)),
                     marker = dict(color = colorlist[c]),
                     orientation = 'h',
                     opacity = .75
                    )
        trace_list.append(trace)
        c = c+1
    return trace_list
    
"""plots.py"""
def make_figure(df, col):
#given a df grouped by source and round, returns a plotly that shows both percents and values                                                                      
    v_df = get_counts(df, col)
    p_df = get_percents(v_df)
    traces = create_traces(p_df, v_df)
    layout = go.Layout(
            title = 'Source Success by Round',
            barmode= 'stack',
            yaxis = {'title' :'Source'},
            xaxis = {'title' : 'Percentage by Round', 'tickformat': '%'})
    fig = go.Figure(data = traces, layout = layout)
    return fig 



"""plots.py stacked area chart """
def pipeline_volume(df, frequency):
    df = df.groupby(['is_bootcamp', pd.Grouper(key='last_updated', freq=frequency)]).size().to_frame('counts').reset_index()
    df = df.pivot(index='last_updated', columns = 'is_bootcamp', values='counts').fillna(value = 0)
    colorlist = ['#e6a4b4', '#7a5d7e', '#4e709d']
    layout = go.Layout(paper_bgcolor = '#ffffff', 
                       plot_bgcolor = '#ffffff',
                       title = 'Pipeline Volume by Source Over Time',
                       xaxis = {'title': 'Month'},
                       yaxis = {'title': 'Amount of Applications Updated'})
    df.iplot(kind = 'area', fill=True, colors=colorlist, layout=layout)
    

def time_traces(df, frequency):   
    df = df.groupby(['is_bootcamp', pd.Grouper(key='last_updated', freq=frequency)]).size().to_frame('counts').reset_index()
    df = df.pivot(index='last_updated', columns = 'is_bootcamp', values='counts').fillna(value = 0)
    trace_list = []
    colorlist = ['#7a5d7e', '#4e709d', '#e6a4b4']
    c=0
    for col in df.columns:
        trace = go.Scatter(
            x = df.index,
            y = df[col],
            name = str(col),
            mode = 'lines+markers', 
            marker = dict(color = colorlist[c]))
        trace_list.append(trace)
        c = c + 1
    layout = go.Layout(barmode='stack',
                       title = 'Application Volume by Source Over Time',
                       xaxis = {'title': 'Month'},
                       yaxis = {'title': 'Amount of Applications Updated'})
    fig = go.Figure(data = trace_list, layout=layout)
    return fig 
