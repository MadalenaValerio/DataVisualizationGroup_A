import dash
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_html_components as html
from dash.dependencies import Input, Output



df = pd.read_csv("result.csv")

#path_datasets = 'https://raw.githubusercontemt.com/mariarencode/COVID_19_Dataset_Challenge/master/Cleaned_Datasets/'
#path_geo_points = 'https://raw.githubusercontent.com/nalpalhao/DV_Practival/master/datasets/Lesson_4/'
#df_country_points = pd.read_csv(path_geo_points + 'country_points.csv')

#result = pd.merge(df, df_country_points, how="inner", on=["Team"])
#result.head()

#--------------------------------------------------------------------------------------------------------------
medal_options = [
    {'label': 'Total Medals', "value" : 'Total_Medal'},
    {'label': 'Gold Medals', 'value': 'Gold'},
    {'label': 'Silver Medals', 'value': 'Silver'},
    {'label': 'Bronze Medals', 'value': 'Bronze'},
    {'label': 'No Medals', 'value': 'Sem_Medalha'},

]

#--------------------------------------------------------------------------------------------------------

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Olympic Medals"),

    html.Div([
       dcc.Dropdown(
        id='medal_drop',
        options=medal_options,
        value="Sem_Medalha",
        multi=False,
    ),

    html.Div([

        html.H1('Olympic Medals Choropleth')
    ]),
    dcc.Graph(
        id='world graph',
        ),

    ])
 ])


#-----------------------------------------------------------------
@app.callback(
    Output('world graph','figure'),
    [Input('medal_drop','value')]
)

def update_graph(medal):
    df1 = df.groupby(['region','NOC'])[medal].sum()
    df1 = df1.reset_index()
    a = df1[medal].values.tolist()
    print(df1.NOC)
    b = df1.NOC.values.tolist()



    data_choropleth = dict(type='choropleth',
            locations=df1.NOC,
            locationmode='ISO-3',
            z=a,
            text=df1['region'],
            colorscale='blues',
            zmin = 0,
            zmax = 500,
        )

    layout_choropleth = dict(geo=dict(scope='world',  # default
                                      projection=dict(type='equirectangular'),
                                      showland=True,  # default = True
                                      landcolor='white',
                                      lakecolor='white',
                                      showocean=True,  # default = False
                                      oceancolor='azure'
                                     ),
                             title=dict(text='Olympic Medal Choropleth Map',
                                        x=.5  # Title relative position according to the xaxis, range (0,1)
                                        )
                      )
    fig_choropleth = go.Figure(data=data_choropleth, layout=layout_choropleth)

    return fig_choropleth


if __name__ == '__main__':
    app.run_server(debug=True)