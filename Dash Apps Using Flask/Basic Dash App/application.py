import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import boto3
import s3fs

s3 = boto3.client('s3')

print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),
    # content will be rendered in this element
    html.Div(id='page-content')
])

#df = pd.read_csv('gdp-life-exp-2007.csv')
df = pd.read_csv('s3://gpgdatascience/gdp-life-exp-2007.csv')
nfl_df = pd.read_csv('s3://gpgdatascience/NFL_Data_Science_2018_2019.csv', header=1)
nfl_df.drop(nfl_df.columns[0], axis=1, inplace=True)
nfl_df.drop([0], axis=0, inplace=True)
nfl_df.drop("Opposing Team Win %", axis=1, inplace=True)

x =  nfl_df['PPG']
y = nfl_df['PA']

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/life-expectancy':
        print(pathname)
        return html.Div([
                dcc.Graph(
                    id='life-exp-vs-gdp',
                    figure={
                        'data': [
                            go.Scatter(
                                x=df[df['continent'] == i]['gdp per capita'],
                                y=df[df['continent'] == i]['life expectancy'],
                                text=df[df['continent'] == i]['country'],
                                mode='markers',
                                opacity=0.7,
                                marker={
                                    'size': 15,
                                    'line': {'width': 0.5, 'color': 'white'}
                                },
                                name=i
                            ) for i in df.continent.unique()
                        ],
                        'layout': go.Layout(
                            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                            yaxis={'title': 'Life Expectancy'},
                            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                            legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
                    }
                )
            ])
    elif pathname == '/nfl':
        print(pathname)
        return html.Div([
                    dcc.Graph(
                        id='NFL_Data_Science_2018_2019',
                        figure={
                            'data': [
                                go.Bar(
                                    x=x,
                                    y=y,
                                    text=y
                                )
                            ],
                            'layout': go.Layout(
                                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                                yaxis={'title': 'Life Expectancy'},
                                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                                legend={'x': 0, 'y': 1},
                                hovermode='closest'
                            )
                        }
                    )
            ])
    else:
        print("Data Science")
        return html.Div([
            html.H3('You are on page {}'.format(pathname))
        ])


if __name__ == '__main__':
    application.run(debug=True)