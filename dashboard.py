import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash import dcc, html, Input, Output

#initializing dash
app = dash.Dash()

#reading csv file into dataframe
df = pd.read_csv('covid.csv')

#backend for world map
fig = px.choropleth(
    data_frame=df,
    locationmode='country names',
    locations='Country/Region',
    labels={'Country/Region': 'Country', 'Confirmed' : 'Total Cases'},
    scope='world',
    color='Confirmed',
    hover_data=['Country/Region', 'Confirmed', 'Deaths'],
    color_continuous_scale=px.colors.sequential.YlOrRd,
    template='plotly_dark',
    )

#frontend for world map
fig.update_layout(
    title_text="Confirmed covid cases all over the world",
    title_xanchor="center",
    title_font=dict(size=20),
    title_x=0.5,
    geo=dict(scope='world'),
    height = 600
)


#backend for pie chart 1
fig2 = px.pie(df, names='WHO Region', values='Confirmed', color_discrete_sequence=px.colors.sequential.YlGnBu, template='plotly_dark')

#frontend for pie chart 1
fig2.update_layout(
    title_text="Percentage of confirmed cases in WHO regions",
    title_xanchor="center",
    title_font=dict(size=20),
    title_x=0.5
)


#backend for pie chart 2
fig3 = px.pie(df, names='WHO Region', values='Deaths', color_discrete_sequence=px.colors.sequential.RdBu, template='plotly_dark')

#frontend for pie chart 2
fig3.update_layout(
    title_text="Percentage of deaths in WHO regions",
    title_xanchor="center",
    title_font=dict(size=20),
    title_x=0.5
)


#organising different graphs on the webpage
app.layout = html.Div(style={'backgroundColor': '#e0b0ff'}, 
    children=[
    html.H1("Dashboard", style={'text-align': 'center'}),
    dcc.Graph(id="world-chart", figure=fig, style={'width': '90%', 'margin-left' : '5%'}),
    dcc.Graph(id="bargraph", figure={}, style={'margin-top': '3vw', 'width': '50%','padding-left':'25%', 'display': 'inline-block'}),
    dcc.RadioItems(id="region",
                 options=[
                     {"label": "Europe", "value": "Europe"},
                     {"label": "Eastern Mediterranean", "value": "Eastern Mediterranean"},
                     {"label": "Africa", "value": "Africa"},
                     {"label": "Americas", "value": "Americas"},
                     {"label": "Western Pacific", "value": "Western Pacific"},
                     {"label": "South-East Asia", "value": "South-East Asia"}],
                 value="Europe",
                 labelStyle={'display': 'block'},
                 style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'},
                 ),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Graph(figure=fig2, style={'margin-left': '2vw', 'display': 'inline-block'}),
    dcc.Graph(figure=fig3, style={'margin-left': '3vw', 'display': 'inline-block'}),
    ])


#Connecting the bar graph with Dash Components (RadioItems above)
@app.callback(
    Output(component_id='bargraph', component_property='figure'),
    [Input(component_id='region', component_property='value')]
)
def update_graph(input_option):
    dff = df.copy()
    dff = dff[dff['WHO Region'] == input_option]

    fig4 = px.bar(x=dff.columns[1:8], 
                  y=list(dff.iloc[:, 1:8].sum(axis=0)), 
                  text=list(dff.iloc[:, 1:8].sum(axis=0)), 
                  labels=dict(x="Cases in "+input_option, y="Frequency"),
                  color_discrete_sequence=px.colors.sequential.Viridis,
                  template='ggplot2',
                  )

    fig4.update_layout(
        title_text="Details of covid cases in WHO Regions",
        title_xanchor="center",
        title_font=dict(size=20),
        title_x=0.5,
    )

    return fig4

if __name__ == "__main__":
    app.run_server(debug=True)