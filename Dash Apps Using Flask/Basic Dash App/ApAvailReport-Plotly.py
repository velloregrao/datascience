import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import boto3
import s3fs
import pandas as pd
import plotly.graph_objs as go

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

graphData = []
graphLabels = []
months = {'1':'january','2':'febuary','3':'March','4':'April','5':'May','6':'June','7':'July','8':'August','9':'September','10':'August','11':'November','12':'December'}
monthPaths = []

client = boto3.client('s3')  # low-level functional API
resource = boto3.resource('s3')  # high-level object-oriented API
my_bucket = resource.Bucket('healthsignals')  # subsitute this for your s3 bucket name.
files = list(my_bucket.objects.filter(Prefix='data/Access Point Availability/'))
li = []

for file in files:
    print(file)
    obj = file.get()
    key = obj['ContentLength']
    print(key)
    if key != 0:
        df = pd.read_csv(obj['Body'], index_col=None,sep=',',skiprows=6)
        monthPaths.append(df)
        month_df= pd.concat(monthPaths,axis=0,ignore_index=True)
        graphData.append(month_df['Uptime (%)'].values.mean())
#        graphLabels.append(months[str(x)])
        monthPaths.clear()
        li.append(df)

ap_df = pd.concat(li, axis=0, ignore_index=True)
print('Total Average AP Availability for Garden Spot Village: ' +str(ap_df['Uptime (%)'].values.mean())+' (%)')

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/':
        return html.Div([
            dcc.Graph(
                id='NFL_Data_Science_2018_2019',
                figure={
                    'data': [
                        go.Bar(
                            x=graphLabels,
                            y=graphData,
                            text=graphData
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

if __name__ == '__main__':
    application.run(debug=True)
