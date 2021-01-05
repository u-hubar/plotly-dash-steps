import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from data import get_patients_df_async

app = dash.Dash(__name__)

header = 'Simple Plotly Dash Steps Tracking Application'

feet_image = 'image.png'

feet = go.Figure()
feet.update_layout(
    width=448,
    height=490,
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="White",
)
feet.add_layout_image(
        dict(
            source=app.get_asset_url(feet_image),
            xref="x",
            yref="y",
            x=0,
            y=490,
            sizex=460,
            sizey=490,
            sizing="contain",
            opacity=1.0,
            layer="below")
)
feet.update_xaxes(
    range=[0, 390],
    showgrid=False,
    zeroline=False,
    visible=False,
)
feet.update_yaxes(
    range=[0, 490],
    showgrid=False,
    zeroline=False,
    visible=False,
)

L1 = feet.add_shape(
    type="circle",
    xref="x", yref="y",
    x0=120, y0=350, x1=150, y1=380,
    line_color="LightSeaGreen",
)

L2 = feet.add_shape(
    type="circle",
    xref="x", yref="y",
    x0=40, y0=300, x1=70, y1=330,
    line_color="LightSeaGreen",
)

L3 = feet.add_shape(
    type="circle",
    xref="x", yref="y",
    x0=75, y0=80, x1=105, y1=110,
    line_color="LightSeaGreen",
)

L4 = feet.add_shape(
    type="circle",
    xref="x", yref="y",
    x0=280, y0=350, x1=250, y1=380,
    line_color="LightSeaGreen",
)

L5 = feet.add_shape(
    type="circle",
    xref="x", yref="y",
    x0=360, y0=300, x1=330, y1=330,
    line_color="LightSeaGreen",
)

L6 = feet.add_shape(
    type="circle",
    xref="x", yref="y",
    x0=315, y0=80, x1=285, y1=110,
    line_color="LightSeaGreen",
)

app.layout = html.Div(children=[
    html.Div(className='row', children=[
        html.Div(className='four columns div-user-controls', children=[
            html.H1(children=header, style={'text-align': 'center'}),
            html.Div(className='div-for-dropdown', children=[
                dcc.Dropdown(id='patient_selector',
                             style={'backgroundColor': '#1E1E1E'},
                             className='patient_selector')
            ], style={'color': '#1E1E1E'}),
            dash_table.DataTable(id='div-for-bio',
                                 style_as_list_view=True,
                                 style_header={'display': 'none'},
                                 style_cell={
                                    'textAlign': 'left',
                                    'backgroundColor': 'rgb(50, 50, 50)',
                                    'color': 'white'
                                 })
        ]),
        html.Div(className='eight columns div-for-charts', children=[
            html.Span(className='helper', style={'display': 'inline-block', 'height': '20%', 'vertical-align': 'middle'}),
            dcc.Graph(figure=feet, style={'display': 'inline-block',
                                          'margin-left': 'auto',
                                          'margin-right': 'auto',
                                          'vertical-align': 'middle'}),
        ], style={'background-color': 'black'})
    ]),
    dcc.Interval(
            id='interval-component',
            interval=1*1000,
            n_intervals=0
        )
])


@app.callback(Output('patient_selector', 'options'),
              Input('interval-component', 'n_intervals'))
def update_dropdown_options(n):
    patients_df = get_patients_df_async()
    return [{'label': i, 'value': i} for i in patients_df["Full Name"]]


@app.callback(Output('div-for-bio', 'columns'),
              Output('div-for-bio', 'data'),
              Input('interval-component', 'n_intervals'),
              Input('patient_selector', 'value'))
def update_patient_info(n, patient_name):
    if patient_name is not None:
        patients_df = get_patients_df_async()
        patient = patients_df[patients_df["Full Name"] == patient_name]
        patient = patient.drop(columns='Full Name')
        patient_info = patient.T.reset_index()
        patient_info.columns = ['Info', 'Value']
        return [{"name": i, "id": i} for i in patient_info.columns], patient_info.to_dict('records')
    else:
        return None, None


if __name__ == '__main__':
    app.run_server(debug=True)
