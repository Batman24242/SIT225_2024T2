import dash
from dash import Dash, dcc, html, dash_table, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('arpit.csv')

df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%dT%H:%M:%S.%f', errors='coerce')

app = Dash(__name__)

app.layout = html.Div([

    html.Div('Please select a Graph Type'),
    dcc.Dropdown(
        id='type_of_graph',
        options=[
            {'label' : 'Line Chart', 'value' : 'line'},
            {'label' : 'Scatter Plot', 'value' : 'scatter'},
            {'label' : 'Histogram', 'value' : 'histogram'}
        ],
        value='line'
    ),

    html.Div('Select the data Variables'),
    dcc.Dropdown(
        id='variables',
        options=[
            {'label' : 'X', 'value' : 'x'},
            {'label' : 'Y', 'value' : 'y'},
            {'label' : 'Z', 'value' : 'z'},
            {'label' : 'All', 'value' : 'all'}
        ],
        value=['x'],
        multi=True  #To include multiple values
    ),

    html.Label("Number of samples: "),
    dcc.Input(id='sample-size', type='number', value=100),
    html.Button('Previous', id='prev_button', n_clicks=0),
    html.Button('Next', id='next_button', n_clicks=0),
   
    dcc.Graph(id='gyro-graph'),

    html.H2("Data Summary"),
    dash_table.DataTable(
        id='data_summary',
        columns=[{'name': col, 'id': col} for col in ['Statistic', 'X', 'Y', 'Z']]
    ),
    dcc.Store(id='store-start-index', data=0) 
    
])

@app.callback(
    
    [Output('gyro-graph', 'figure'),
     Output('data_summary', 'data'),
     Output('store-start-index', 'data')],
    [Input('type_of_graph', 'value'),
     Input('variables', 'value'),
     Input('sample-size', 'value'),
     Input('prev_button', 'n_clicks'),
     Input('next_button', 'n_clicks')],
    [State('store-start-index', 'data')]
)

def update_graph(graph_type, variables, sample_size, prev_clicks, next_clicks, start_idx):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    # Handle navigation
    total_samples = len(df)
    if button_id == 'prev_button':
        start_idx = max(0, start_idx - sample_size)
    elif button_id == 'next_button':
        start_idx = min(total_samples - sample_size, start_idx + sample_size)
    
    # Slice data
    end_idx = start_idx + sample_size
    filtered_df = df.iloc[start_idx:end_idx]
    
    # Handle 'All' selection
    if 'all' in variables:
        selected_vars = ['x', 'y', 'z']
    else:
        selected_vars = variables
    
    # Generate plot
    if graph_type == 'line':
        fig = px.line(filtered_df, x='Time', y=selected_vars, title='Gyroscope Line Chart')
    elif graph_type == 'scatter':
        fig = px.scatter(filtered_df, x='Time', y=selected_vars, title='Gyroscope Scatter Plot')
    else:
        fig = px.histogram(filtered_df, x=selected_vars, barmode='overlay', title='Gyroscope Distributions')
    
    # Calculate summary stats
    stats = []
    for stat in ['mean', 'std', 'min', 'max']:
        row = {'Statistic': stat.capitalize()}
        for var in ['x', 'y', 'z']:
            row[var.upper()] = round(getattr(filtered_df[var], stat)(), 2)
        stats.append(row)
    
    return fig, stats, start_idx
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
