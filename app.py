import dash
import dash_core_components as dcc
import dash_html_components as html
import recruitment_analysis as recruit
import pandas as pd
import plotly.graph_objs as go
import data as data 
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Recruitment Analysis Data'),
    html.Div(children = '''Visualizations of CKM Recruitment Data'''),
    dcc.Graph(
        id = 'overview',
        figure = recruit.time_traces(data.applicants, 'M')
    ),
    
    dcc.Graph(
        id = 'general-graph',
        figure = recruit.make_figure(data.general, 'is_bootcamp')
        ),
    dcc.Graph(
        id = 'by-school',
        figure = recruit.make_figure(data.school_ppl, 'source')
    ),
    dcc.Graph(
        id = 'by-bootcamp',
        figure = recruit.make_figure(data.bootcamp_ppl, 'source')
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
