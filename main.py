import base64
import io

import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, State, callback_context, dash_table
import numpy as np

FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in content_type:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), skipinitialspace=True, na_values=["-"])
        else:
            return None, 'Unsupported file type.'
    except Exception as e:
        print(e)
        return None, 'There was an error processing the file.'
    return df, ''

app = Dash(__name__, external_stylesheets=[FA], title="Torque Logs Visualizer")

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select a .csv File')]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
            'textAlign': 'center', 'margin': '10px 0', 'cursor': 'pointer',
        },
        multiple=False
    ),
    dcc.Dropdown(
        id='value-dropdown',
        placeholder='Select a value...',
        style={'margin': '10px 0'}
    ),
    html.Div(id='output-data-upload', style={'margin': '20px 0'}),
    html.A(
        className="github-fab",
        href="https://github.com/alessandrodd/torque_logs_visualizer",
        target="_blank",
        children=html.I(className="fab fa-github fa-2x"),
        style={
            'position': 'fixed', 'bottom': '20px', 'right': '20px',
            'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
            'color': 'white', 'backgroundColor': '#000', 'borderRadius': '50%',
            'width': '50px', 'height': '50px', 'textAlign': 'center',
            'textDecoration': 'none', 'boxShadow': '2px 2px 3px rgba(0,0,0,0.2)',
        }
    ),
])

@app.callback(
    [Output('output-data-upload', 'children'),
     Output('value-dropdown', 'options')],
    [Input('upload-data', 'contents'),
     Input('value-dropdown', 'value')]
)
def update_output(list_of_contents, selected_value):
    triggered_by = [p['prop_id'] for p in callback_context.triggered][0]
    
    if list_of_contents:
        df, error_message = parse_contents(list_of_contents)
        if df is None:
            return error_message, []
        
        valid_columns = [col for col in df.columns if df[col].dtype in ['float64', 'int64']]
        dropdown_options = [{'label': col, 'value': col} for col in valid_columns]
        
        if 'upload-data' in triggered_by:
            selected_value = valid_columns[0] if len(valid_columns) > 0 else None

        if selected_value:
            fig_map = px.scatter_mapbox(df, lat='Latitude', lon='Longitude', color=selected_value,
                                         zoom=10, height=500, color_continuous_scale=px.colors.sequential.Jet, hover_data=df.columns)
            fig_map.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0})

            statistics = {
                'Statistic': ['Average', 'Maximum', 'Minimum', 'Start', 'End', '25th Percentile', 'Median', '75th Percentile', '90th Percentile'],
                'Value': [
                    df[selected_value].mean(), df[selected_value].max(), df[selected_value].min(),
                    df[selected_value].iloc[0], df[selected_value].iloc[-1],
                    np.percentile(df[selected_value].dropna(), 25), np.percentile(df[selected_value].dropna(), 50),
                    np.percentile(df[selected_value].dropna(), 75), np.percentile(df[selected_value].dropna(), 90)
                ]
            }

            stats_df = pd.DataFrame(statistics)

            return html.Div([
                dcc.Graph(id='map-plot', figure=fig_map),
                dash_table.DataTable(
                    data=stats_df.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in stats_df.columns],
                    style_cell={'textAlign': 'left'},
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    },
                    style_data_conditional=[
                        {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
                    ]
                )
            ]), dropdown_options
        
    return "No file uploaded.", []

if __name__ == '__main__':
    app.run_server(debug=False)
