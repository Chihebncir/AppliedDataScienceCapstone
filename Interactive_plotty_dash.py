# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 17:06:09 2023

@author: chihe
"""

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    # dcc.RangeSlider(id='payload-slider',...)
    html.P("Payload range (Kg):"),
    # Add a range slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 10000: '10000'},
                    value=[min_payload, max_payload]),
    html.Br(),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value')])
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Calculate the total successful launches for all sites
        total_success = len(spacex_df[spacex_df['class'] == 1])
        # Calculate the total failed launches for all sites
        total_failed = len(spacex_df[spacex_df['class'] == 0])
        # Create a pie chart for all sites
        fig = px.pie(names=['Successful', 'Failed'], values=[total_success, total_failed],
                     title='Total Successful Launches')
    else:
        # Filter the dataframe for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Calculate the successful launches for the selected site
        site_success = len(filtered_df[filtered_df['class'] == 1])
        # Calculate the failed launches for the selected site
        site_failed = len(filtered_df[filtered_df['class'] == 0])
        # Create a pie chart for the selected site
        fig = px.pie(names=['Successful', 'Failed'], values=[site_success, site_failed],
                     title=f'Successful Launches for {selected_site}')

    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        # Filter the dataframe based on the selected payload range
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        # Create a scatter plot for all sites
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        fig.update_layout(title='Payload vs Launch Outcome (All Sites)',
                          xaxis_title='Payload Mass (kg)',
                          yaxis_title='Launch Outcome')
    else:
        # Filter the dataframe for the selected site and payload range
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) &
                                (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        # Create a scatter plot for the selected site
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        fig.update_layout(title=f'Payload vs Launch Outcome for {selected_site}',
                          xaxis_title='Payload Mass (kg)',
                          yaxis_title='Launch Outcome')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
