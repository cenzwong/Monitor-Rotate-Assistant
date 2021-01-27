["""
Ref: https://deepnote.com/project/d780ad21-48be-4756-8c0d-30311a37d59d#%2Fnotebook.ipynb
Date: 20210125
Contact: cenz@hpe.com
"""
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

from io import StringIO
import requests

import datetime
# ==========================Getting the data========================
df_covid = pd.DataFrame()
df_cluster = pd.DataFrame()
df_cluster2 = pd.DataFrame()
def update_the_data(df_covid, df_cluster, df_cluster2):
    url_enhanced_sur_covid_19_eng = 'https://www.chp.gov.hk/files/misc/enhanced_sur_covid_19_eng.csv'
    url_large_clusters_eng = 'https://www.chp.gov.hk/files/misc/large_clusters_eng.csv'

    r = requests.get(url_enhanced_sur_covid_19_eng)
    df_covid = pd.read_csv(StringIO(r.text))

    r = requests.get(url_large_clusters_eng)
    df_cluster = pd.read_csv(StringIO(r.text))

    #Cleaning data

    # Remove all the capital, non capital confusion
    df_covid["HK/Non-HK resident"] = df_covid["HK/Non-HK resident"].str.upper()

    # Convert Date to datetime format
    df_covid["Report date"] = pd.to_datetime(df_covid["Report date"], infer_datetime_format=True)

    # Cannot convert due to Asymptomatic entity
    # df["Date of onset"] = pd.to_datetime(df["Date of onset"], infer_datetime_format=True)

    ## Second file
    df_cluster["Case no."] = df_cluster[["Involved case number"]].applymap(lambda x: int(x.split(",")[0]))
    # df_cluster[["Involved case number count"]] = df_cluster[["Involved case number"]].applymap(lambda x: len(x.split(","))) Done

    df_cluster2 = pd.merge(df_covid, df_cluster, left_on="Case no.", right_on="Case no.")[["Cluster", "Report date", "Number of cases","Case no."]]
    return (df_covid, df_cluster, df_cluster2)
# ======================= Function Declaration ===================================
def df_column_draw_pie_chart(df, columnName, figTitle):
    labels = [arr for arr in df[columnName].unique()]
    values = [df[columnName].value_counts()[label] for _,label in enumerate(labels)]
    fig = go.Figure(data=[go.Pie(labels=labels, 
                                    values=values, 
                                    title=figTitle,
                                )
                        ]
                    )
    return fig

def df_column_count_line_chart(df, columnName, figTitle, mode="count"):
    df_countByDate = df_covid[columnName].value_counts().sort_index()
    if mode == "count":
        fig = px.line(df_countByDate, title=figTitle)
    elif mode == "cumsum":
        fig = px.line(df_countByDate.cumsum(), title=figTitle)
    return fig

def df_column_histogram(df, columnName, figTitle):
    fig = px.histogram(df, x=columnName, title=figTitle)
    return fig

def df_bubble_chart(df, dfx, dfy, dfsize, hoverName, titleName):
    fig = px.scatter(df, x=dfx,y=dfy,
	                    size=dfsize,  
                        hover_name=hoverName, size_max=60, title=titleName)
    return fig

def go_df_plot(df,dfx,dfy,lineName):
    go_obj = go.Scatter(x=df[dfx].to_list(), y=df[dfy].to_list(),
                    mode='lines',
                    name=lineName)
    return go_obj

def go_df_count_plot(df,dfx,lineName,mode="count"):
    df_countByDate = df[dfx].value_counts().sort_index()
    if mode == 'cumsum':
        df_countByDate = df_countByDate.cumsum()
    go_obj = go.Scatter(x=df_countByDate.index.to_list(),y=df_countByDate.to_list(),
                    mode='lines',
                    name=lineName)
    return go_obj

def go_df_bubble_chart(df,dfx,dfy,dfsize,dfhover, lineName):
    go_obj = go.Scatter(
        x=df[dfx].to_list(), y=df[dfy].to_list(),
        mode='markers',
        marker=dict(
            size=df[dfsize].to_list(),
            sizemode='area',
            sizeref=0.2,
            sizemin=1,
        ),
        hovertext=df[dfhover].to_list(),
        name=lineName,
    )
    return go_obj
# ====================== All-in-one chart =======================

from plotly.subplots import make_subplots
def AllinOneChart(df_covid, df_cluster, df_cluster2):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go_df_bubble_chart(df_cluster2,"Report date","Case no.","Number of cases","Cluster", lineName="Big Cluster"))
    fig.add_trace(go_df_count_plot(df_covid,"Report date", lineName="Total Infected Case",mode="cumsum"))
    fig.add_trace(go_df_count_plot(df_covid,"Report date", lineName="Daily Infected Case",mode="count"), secondary_y=True)

    # Add figure title
    fig.update_layout(
        title_text="Summary of Hong Kong COVID19 Cases"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Total</b> Cases", secondary_y=False)
    fig.update_yaxes(title_text="<b>Daily</b> Cases", secondary_y=True)
    return fig

# ======================= Dash App ==============================
import dash
import dash_core_components as dcc
import dash_html_components as html

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://raw.githubusercontent.com/helloezmeral/what-is-this/main/html/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# GUnicorn===========
server = app.server

colors = {
    'background': '#00b388',
    'text': '#425563'
}

# This combination will make it refresh everytime it open
def serve_layout():
    global df_covid, df_cluster, df_cluster2
    df_covid, df_cluster, df_cluster2 = update_the_data(df_covid, df_cluster, df_cluster2)
    _serve_layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
        html.H1(
            children='HPE COVID HK Data Demo :-)',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }),

        html.Div(children='''
            Data Reference: https://data.gov.hk/en/
            || Last Update: 
            ''' + str(datetime.datetime.now()),
            style={
                'textAlign': 'center',
                'color': colors['text']
            }),
        dcc.Graph(
            id='all-in-one',
            figure=AllinOneChart(df_covid, df_cluster, df_cluster2)
        ),
        dcc.Graph(
            id='gender-graph',
            figure=df_column_draw_pie_chart(df_covid,'Gender', 'Gender of the infected')
        ),

        dcc.Graph(
            id='origin-graph',
            figure=df_column_draw_pie_chart(df_covid, 'HK/Non-HK resident', 'Origin of the infected')
        ),

        dcc.Graph(
            id='case-class-graph',
            figure=df_column_draw_pie_chart(df_covid, 'Case classification*', 'Classification of the cases')
        ),

        dcc.Graph(
            id='age-graph',
            figure=df_column_histogram(df_covid, "Age", "Histogram of the infected age")
        ),
        dcc.Graph(
            id='sum-graph',
            figure=df_column_count_line_chart(df_covid, 'Report date', 'Infected People Daily')
        ),
        dcc.Graph(
            id='cumsum-graph',
            figure=df_column_count_line_chart(df_covid, 'Report date', 'Infected People Daily', 'cumsum')
        ),
        dcc.Graph(
            id='cluster-graph',
            figure=df_bubble_chart(df_cluster2, "Report date", "Case no.", "Number of cases", "Cluster", "Cluster of the infected cases")
        ),

        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),
    ])
    return _serve_layout

app.layout = serve_layout

if __name__ == '__main__':
    df_covid, df_cluster, df_cluster2 = update_the_data(df_covid, df_cluster, df_cluster2)
    # app.run_server(debug=True, port=8060, host='0.0.0.0') # for debug
    app.run_server(debug=True)

# gunicorn -w 2 -b 0.0.0.0:8050 myapp:server
