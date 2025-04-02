import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("fifa_world_cup_finals.csv")

# Clean data just in case
df['Winner'] = df['Winner'].replace({'West Germany': 'Germany'})
df['RunnerUp'] = df['RunnerUp'].replace({'West Germany': 'Germany'})

# Calculate win counts
win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # Needed for Render

# Layout
app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard"),

    html.H3("World Cup Winners Choropleth Map"),
    dcc.Graph(id='choropleth',
              figure=px.choropleth(win_counts,
                                   locations="Country",
                                   locationmode="country names",
                                   color="Wins",
                                   title="FIFA World Cup Wins by Country")),

    html.Br(),

    html.Label("Select a Country:"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in sorted(win_counts['Country'])],
        placeholder="Select a country"
    ),
    html.Div(id='country-output'),

    html.Br(),

    html.Label("Select a Year:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': y, 'value': y} for y in sorted(df['Year'])],
        placeholder="Select a year"
    ),
    html.Div(id='year-output')
])

# Callbacks
@app.callback(
    Output('country-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_info(country):
    if not country:
        return ""
    wins = win_counts[win_counts['Country'] == country]['Wins'].values[0]
    return f"{country} has won the FIFA World Cup {wins} times."

@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year_info(year):
    if not year:
        return ""
    row = df[df['Year'] == year]
    if row.empty:
        return "No data available."
    winner = row['Winner'].values[0]
    runner = row['RunnerUp'].values[0]
    return f"In {year}, {winner} won the World Cup, and {runner} was the runner-up."

# This line ensures the app is callable by gunicorn
app = app.server if __name__ != '__main__' else app

# Run locally (Render ignores this)
if __name__ == '__main__':
    app.run(debug=True)
