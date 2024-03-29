import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

from database.data import get_all_patient_sensors, get_patients_df
from utils import (create_data_plot, create_figure, create_sensor_textbox,
                   parse_xaxis_range, update_anomalies_figure,
                   update_history_figure, сreate_dynamic_sensors)

app = dash.Dash(__name__)

header = "Simple Plotly Dash Steps Tracking Application"

data_plot = create_data_plot()
feet = create_figure(app)


app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H1(
                            children=header, style={"text-align": "center"}
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                    id="patient_selector",
                                    className="patient_selector",
                                    style={
                                        "backgroundColor": "#1E1E1E",
                                    },
                                    placeholder="Select a patient",
                                )
                            ],
                            style={"color": "#1E1E1E"},
                        ),
                        dash_table.DataTable(
                            id="div-for-bio",
                            style_as_list_view=True,
                            style_header={"display": "none"},
                            style_cell={
                                "textAlign": "left",
                                "backgroundColor": "rgb(50, 50, 50)",
                                "color": "white",
                            },
                        ),
                        html.Br(),
                        html.Br(),
                        html.Div(
                            className="div-for-plots",
                            children=[
                                dcc.Dropdown(
                                    id="plot_selector",
                                    className="plot_selector",
                                    style={
                                        "backgroundColor": "#1E1E1E",
                                    },
                                    placeholder="Select a plot type",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in ["History", "Anomalies"]
                                    ],
                                ),
                                dcc.Graph(
                                    id="data-plot",
                                    figure=data_plot,
                                    style={
                                        "margin-left": "auto",
                                        "margin-right": "auto",
                                        "vertical-align": "middle",
                                        "padding-bottom": "30px",
                                    },
                                ),
                                dcc.Tabs(
                                    id="sensors-tabs",
                                    parent_className="black-tabs",
                                    className="black-tabs-container",
                                    value="L0",
                                    children=[
                                        dcc.Tab(
                                            label="L0",
                                            value="L0",
                                            className="black-tab",
                                            selected_className="black-tab--selected",
                                        ),
                                        dcc.Tab(
                                            label="L1",
                                            value="L1",
                                            className="black-tab",
                                            selected_className="black-tab--selected",
                                        ),
                                        dcc.Tab(
                                            label="L2",
                                            value="L2",
                                            className="black-tab",
                                            selected_className="black-tab--selected",
                                        ),
                                        dcc.Tab(
                                            label="R0",
                                            value="R0",
                                            className="black-tab",
                                            selected_className="black-tab--selected",
                                        ),
                                        dcc.Tab(
                                            label="R1",
                                            value="R1",
                                            className="black-tab",
                                            selected_className="black-tab--selected",
                                        ),
                                        dcc.Tab(
                                            label="R2",
                                            value="R2",
                                            className="black-tab",
                                            selected_className="black-tab--selected",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="eight columns div-for-charts",
                    children=[
                        html.Span(
                            className="helper",
                            style={
                                "display": "inline-block",
                                "height": "20%",
                                "vertical-align": "middle",
                            },
                        ),
                        dcc.Graph(
                            id="feet-graph",
                            figure=feet,
                            style={
                                "display": "inline-block",
                                "margin-left": "auto",
                                "margin-right": "auto",
                                "vertical-align": "middle",
                            },
                        ),
                    ],
                    style={"background-color": "black"},
                ),
            ],
        ),
        dcc.Interval(
            id="interval-component", interval=1 * 1000, n_intervals=0
        ),
    ]
)


@app.callback(
    Output("patient_selector", "options"),
    Input("interval-component", "n_intervals"),
)
def update_dropdown_options(n):
    patients_df = get_patients_df()
    return [
        {"label": f'{row["firstname"]} {row["lastname"]}', "value": row.name}
        for i, row in patients_df.iterrows()
    ]


@app.callback(
    Output("div-for-bio", "columns"),
    Output("div-for-bio", "data"),
    Input("patient_selector", "value"),
    Input("interval-component", "n_intervals"),
)
def update_patient_info(patient_id, n):
    if patient_id is not None:
        patients_df = get_patients_df()
        patient = patients_df.loc[patient_id, :]
        patient = patient[["firstname", "lastname", "birthdate", "disabled"]]
        patient.index = patient.index.str.capitalize()
        patient_info = patient.T.reset_index()
        patient_info.columns = ["Info", "Value"]
        return [
            {"name": i, "id": i} for i in patient_info.columns
        ], patient_info.to_dict("records")
    else:
        empty_df = pd.DataFrame(
            np.empty((4, 2), dtype=object), columns=["Info", "Value"]
        )
        return [
            {"name": i, "id": i} for i in empty_df.columns
        ], empty_df.to_dict("records")


@app.callback(
    Output("feet-graph", "figure"),
    Input("patient_selector", "value"),
    Input("data-plot", "relayoutData"),
    Input("interval-component", "n_intervals"),
)
def update_feet_graph(patient_id, plot_x_range, n):
    feet = create_figure(app)
    if patient_id is not None:
        patient_sensors = get_all_patient_sensors(patient_id)

        feet = сreate_dynamic_sensors(
            feet,
            patient_sensors,
            ["L0", "L1", "L2", "R0", "R1", "R2"],
            [160, 125, 143, 227, 262, 244],
            [325, 295, 135, 325, 295, 135],
        )

        x_range = parse_xaxis_range(plot_x_range)

        feet = create_sensor_textbox(
            feet, [10, 400, 97.5, 490], patient_sensors, "L0", x_range
        )
        feet = create_sensor_textbox(
            feet, [10, 220, 97.5, 310], patient_sensors, "L1", x_range
        )
        feet = create_sensor_textbox(
            feet, [10, 40, 97.5, 130], patient_sensors, "L2", x_range
        )
        feet = create_sensor_textbox(
            feet, [290, 400, 377.5, 490], patient_sensors, "R0", x_range
        )
        feet = create_sensor_textbox(
            feet, [290, 220, 377.5, 310], patient_sensors, "R1", x_range
        )
        feet = create_sensor_textbox(
            feet, [290, 40, 377.5, 130], patient_sensors, "R2", x_range
        )

    return feet


@app.callback(
    Output("data-plot", "figure"),
    Input("patient_selector", "value"),
    Input("plot_selector", "value"),
    Input("sensors-tabs", "value"),
    Input("data-plot", "relayoutData"),
    Input("interval-component", "n_intervals"),
)
def update_data_plot(patient_id, plot_type, sensor_name, plot_x_range, n):
    data_plot = create_data_plot()

    if patient_id is not None and plot_type is not None:
        sensors = get_all_patient_sensors(patient_id)
        x_range = parse_xaxis_range(plot_x_range)

        if plot_type == "History":
            data_plot = update_history_figure(
                data_plot, sensor_name, sensors, x_range
            )
        elif plot_type == "Anomalies":
            data_plot = update_anomalies_figure(
                data_plot, sensor_name, sensors, x_range
            )

    return data_plot


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="5000", debug=True, threaded=True)
