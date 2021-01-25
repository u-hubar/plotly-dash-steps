import plotly.graph_objects as go


def create_data_plot():
    plot = go.Figure()
    plot.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="Black",
        plot_bgcolor="Black",
    )
    plot.update_xaxes(
        range=[0, 10],
    )
    plot.update_yaxes(
        range=[0, 1500],
    )
    return plot


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
            source=app.get_asset_url('image.png'),
            xref="x",
            yref="y",
            x=100,
            y=420,
            sizex=700,
            sizey=350,
            sizing="contain",
            opacity=1.0,
            layer="below"
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


def сreate_dynamic_sensors(fig, patient, sensors, cord_x, cord_y):
    fig.add_scatter(
        x=cord_x,
        y=cord_y,
        mode='markers',
        marker=dict(
            colorscale=[
                [0, 'rgb(255,255,255)'],
                [0.2, 'rgb(255,133,102)'],
                [0.4, 'rgb(255,112,77)'],
                [0.6, 'rgb(255,92,51)'],
                [0.8, 'rgb(255,71,26)'],
                [1, 'rgb(255,0,0)']
            ],
            color=[patient[f"{sensor} value"].item() for sensor in sensors],
            size=[50]*len(sensors),
            line=dict(width=2, color='#000000'),
            showscale=False
        ),
    )
    return fig


def create_sensor_textbox(fig, cord, patient, sensor):
    fig.add_shape(
        type="rect",
        x0=cord[0],
        y0=cord[1],
        x1=cord[2],
        y1=cord[3],
        line_color="#636363",
        line_width=3,
    )

    text = [
        f"Sensor: {sensor}",
        f"Value: {patient[f'{sensor} value'].item()}",
        f"Anomaly: {patient[f'{sensor} anomaly'].item()}"
    ]
    for i, line in enumerate(text):
        fig.add_annotation(
            x=(cord[0] + ((cord[2] - cord[0]) / 2)),
            y=(cord[3] - (i+1)*((cord[3] - cord[1]) / 4)),
            text=line,
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="#ffffff"
            ),
        )
    return fig


def create_sensor_arrow(fig, cord):
    fig.add_annotation(
        x=cord[0],
        y=cord[1],
        ax=3*(cord[2] - cord[0]),
        ay=2*(cord[1] - cord[3]),
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
    )
    return fig
