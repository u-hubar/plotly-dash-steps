import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

from data import get_patients_df_async
from utils import (create_data_plot, create_figure, create_sensor_arrow,
                   create_sensor_textbox, сreate_dynamic_sensors)

app = dash.Dash(__name__)

header = 'Simple Plotly Dash Steps Tracking Application'

data_plot = create_data_plot()
feet = create_figure(app)


app.layout = html.Div(children=[
    html.Div(className='row', children=[
        html.Div(className='four columns div-user-controls', children=[
            html.H1(children=header, style={'text-align': 'center'}),
            html.Div(className='div-for-dropdown', children=[
                dcc.Dropdown(id='patient_selector',
                             className='patient_selector',
                             style={
                                'backgroundColor': '#1E1E1E',
                                },
                             placeholder='Select a patient')
            ], style={'color': '#1E1E1E'}),
            dash_table.DataTable(id='div-for-bio',
                                 style_as_list_view=True,
                                 style_header={'display': 'none'},
                                 style_cell={'textAlign': 'left',
                                             'backgroundColor': 'rgb(50, 50, 50)',
                                             'color': 'white'}),
            html.Br(),
            html.Br(),
            html.Div(className='div-for-plots', children=[
                dcc.Dropdown(id='plot_selector',
                             className='plot_selector',
                             style={
                                'backgroundColor': '#1E1E1E',
                                },
                             placeholder='Select a plot type',
                             options=[{'label': i, 'value': i} for i in ['History', 'Anomalies']]),
                html.Br(),
                dcc.Graph(id='data-plot', figure=data_plot, style={'margin-left': 'auto',
                                                                   'margin-right': 'auto',
                                                                   'vertical-align': 'middle'})
            ]),
        ]),
        html.Div(className='eight columns div-for-charts', children=[
            html.Span(className='helper', style={'display': 'inline-block',
                                                 'height': '20%',
                                                 'vertical-align': 'middle'}),
            dcc.Graph(id='feet-graph', figure=feet, style={'display': 'inline-block',
                                                           'margin-left': 'auto',
                                                           'margin-right': 'auto',
                                                           'vertical-align': 'middle'}),
        ], style={'background-color': 'black'})
    ]),
    dcc.Interval(
            id='interval-component',
            interval=1*400,
            n_intervals=0
        )
])


@app.callback(Output('patient_selector', 'options'),
              Input('interval-component', 'n_intervals'))
def update_dropdown_options(n):
    patients_df = get_patients_df_async()
    return [{'label': row["Full Name"], 'value': row["ID"]} for i, row in patients_df.iterrows()]


@app.callback(Output('div-for-bio', 'columns'),
              Output('div-for-bio', 'data'),
              Input('patient_selector', 'value'),
              Input('interval-component', 'n_intervals'),)
def update_patient_info(patient_id, n):
    if patient_id is not None:
        patients_df = get_patients_df_async()
        patient = patients_df[patients_df["ID"] == patient_id]
        patient = patient[["ID", "Name", "Surname", "Birthdate", "Disabled"]]
        patient_info = patient.T.reset_index()
        patient_info.columns = ['Info', 'Value']
        return [{"name": i, "id": i} for i in patient_info.columns], patient_info.to_dict('records')
    else:
        empty_df = pd.DataFrame(np.empty((5, 2), dtype=object), columns=['Info', 'Value'])
        return [{"name": i, "id": i} for i in empty_df.columns], empty_df.to_dict('records')


@app.callback(Output('feet-graph', 'figure'),
              Input('patient_selector', 'value'),
              Input('interval-component', 'n_intervals'),)
def update_feet_graph(patient_id, n):
    feet = create_figure(app)
    if patient_id is not None:
        patients_df = get_patients_df_async()
        patient = patients_df[patients_df["ID"] == patient_id]

        feet = сreate_dynamic_sensors(feet, patient,
                                      ['L0', 'L1', 'L2', 'R0', 'R1', 'R2'],
                                      [160, 125, 143, 227, 262, 244],
                                      [325, 295, 135, 325, 295, 135])

        feet = create_sensor_textbox(feet, [10, 400, 97.5, 490], patient, 'L0')
        feet = create_sensor_textbox(feet, [10, 220, 97.5, 310], patient, 'L1')
        feet = create_sensor_textbox(feet, [10, 40, 97.5, 130], patient, 'L2')
        feet = create_sensor_textbox(feet, [290, 400, 377.5, 490], patient, 'R0')
        feet = create_sensor_textbox(feet, [290, 220, 377.5, 310], patient, 'R1')
        feet = create_sensor_textbox(feet, [290, 40, 377.5, 130], patient, 'R2')

        feet = create_sensor_arrow(feet, [153, 335, 100, 430])
        feet = create_sensor_arrow(feet, [117, 287.5, 97.5, 265])
        feet = create_sensor_arrow(feet, [135, 127.5, 99, 85])
        feet = create_sensor_arrow(feet, [234, 335, 287.5, 430])
        feet = create_sensor_arrow(feet, [269.5, 287.5, 290, 265])
        feet = create_sensor_arrow(feet, [251.5, 127.5, 288.5, 85])

    return feet


if __name__ == '__main__':
    app.run_server(debug=True)
