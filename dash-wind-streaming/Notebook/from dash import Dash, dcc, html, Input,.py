from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import pandas as pd

app = Dash(__name__)

df = pd.read_csv("Onlinedata_Juli_August.csv")
df.sort_values(by=['time_utc'], inplace=True, ascending=True)
date = [int((i[5:7]+i[8:10])) for i in df['time_utc']]
df['date'] = date
july = df[df.date <= 731]
id = july.control_state_id.to_list()
id = [str(i) for i in id]
july['control_state_id'] = id


app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        july['date'].min(),
        july['date'].max(),
        step=None,
        value=july['date'].min(),
        marks={str(date): str(date) for date in july['date'].unique()},
        id='time-slider'
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('time-slider', 'value'))
def update_figure(selected_date):
    filtered_df = july[july.date == selected_date]

    fig = px.scatter(filtered_df, x='wind_speed', y="active_power_watt", color="control_state_id",
                   hover_name="external_mapping_id")

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == 'main':
    app.run_server(debug=True)