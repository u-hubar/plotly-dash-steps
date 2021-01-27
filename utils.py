import plotly.graph_objects as go
import plotly.express as px


def create_data_plot():
    plot = px.line(template="plotly_dark")
    plot.update_layout(
        height=360,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
    )
    plot.update_xaxes(
        showgrid=False,
        zeroline=False,
        visible=False,
    )
    plot.update_yaxes(
        showgrid=False,
        zeroline=False,
        visible=False,
    )
    return plot


def parse_xaxis_range(plot_x_range):
    x_range = None
    if 'xaxis.range[0]' in plot_x_range.keys() and 'xaxis.range[1]' in plot_x_range.keys():
        x_range = [
            plot_x_range['xaxis.range[0]'],
            plot_x_range['xaxis.range[1]']
        ]
    return x_range


def update_history_figure(fig, plot_type, sensors, x_range):
    fig = px.line(
        sensors, x="measured_at", y=f"{plot_type}_val", template="plotly_dark"
    )
    fig.update_layout(
        height=360,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        yaxis=dict(
            fixedrange=True
        )
    )

    if x_range is not None:
        fig.update_xaxes(
            type="date",
            range=x_range,
        )
    return fig


def update_anomalies_figure(fig, sensor_name, sensors, x_range):
    sensor_anomalies = sensors[sensors[f"{sensor_name}_anom"] == 1]
    fig = px.line(
        sensor_anomalies, x="measured_at", y=f"{sensor_name}_val", template="plotly_dark"
    )
    fig.update_layout(
        height=360,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
    )

    if x_range is not None:
        fig.update_xaxes(
            type="date",
            range=x_range,
        )
    return fig


def create_figure(app):
    feet = go.Figure()
    feet.update_layout(
        width=1094,
        height=800,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="Black",
        plot_bgcolor="Black",
    )
    feet.add_layout_image(
        dict(
            source=app.get_asset_url("image.png"),
            xref="x",
            yref="y",
            x=100,
            y=420,
            sizex=700,
            sizey=350,
            sizing="contain",
            opacity=1.0,
            layer="below",
        )
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
    return feet


def сreate_dynamic_sensors(fig, sensors, sensors_list, cord_x, cord_y):
    last_sensors = sensors[
        sensors["measured_at"] == sensors["measured_at"].max()
    ]
    fig.add_scatter(
        x=cord_x,
        y=cord_y,
        mode="markers",
        marker=dict(
            colorscale=[
                [0, "rgb(255,255,255)"],
                [0.2, "rgb(255,133,102)"],
                [0.4, "rgb(255,112,77)"],
                [0.6, "rgb(255,92,51)"],
                [0.8, "rgb(255,71,26)"],
                [1, "rgb(255,0,0)"],
            ],
            color=[last_sensors[f"{s}_val"].item() for s in sensors_list],
            size=[50] * len(sensors_list),
            line=dict(width=2, color="#000000"),
            showscale=False,
        ),
    )
    for i, s in enumerate(sensors_list):
        fig.add_annotation(
            x=cord_x[i],
            y=cord_y[i],
            text=last_sensors[f"{s}_val"].item(),
            showarrow=False,
            font=dict(
                family="Courier New, monospace", size=16, color="#000000"
            ),
        )
    return fig


def create_sensor_textbox(fig, cord, sensors, sensor_name, x_range):
    fig.add_shape(
        type="rect",
        x0=cord[0],
        y0=cord[1],
        x1=cord[2],
        y1=cord[3],
        line_color="#636363",
        line_width=3,
    )

    if x_range is not None:
        x_min, x_max = x_range
        boolean_mask = (sensors["measured_at"] > x_min) & (sensors["measured_at"] <= x_max)
        sensors = sensors.loc[boolean_mask]

    mean = sensors[f"{sensor_name}_val"].mean()
    min = sensors[f"{sensor_name}_val"].min()
    max = sensors[f"{sensor_name}_val"].max()

    text = [
        f"Sensor: {sensor_name}",
        f"Mean: {mean:.2f}",
        f"Min: {min}",
        f"Max: {max}",
    ]
    for i, line in enumerate(text):
        fig.add_annotation(
            x=(cord[0] + ((cord[2] - cord[0]) / 2)),
            y=(cord[3] - (i + 1) * ((cord[3] - cord[1]) / (len(text) + 1))),
            text=line,
            showarrow=False,
            font=dict(
                family="Courier New, monospace", size=16, color="#ffffff"
            ),
        )
    return fig


def create_sensor_arrow(fig, cord):
    fig.add_annotation(
        x=cord[0],
        y=cord[1],
        ax=3 * (cord[2] - cord[0]),
        ay=2 * (cord[1] - cord[3]),
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
    )
    return fig
