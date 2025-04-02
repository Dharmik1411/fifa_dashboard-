server = app.server

import pandas as pd

# Step 1: Scrape tables from Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"
tables = pd.read_html(url)

# Step 2: Select the correct table (Table 3)
df = tables[3]

# Step 3: Clean column names safely
df = df.rename(columns=lambda col: str(col).strip())

# Step 4: Keep only the necessary columns
df = df[['Year', 'Winners', 'Runners-up']]
df.columns = ['Year', 'Winner', 'RunnerUp']

# Step 5: Filter numeric years only
df = df[df['Year'].astype(str).str.isnumeric()]
df['Year'] = df['Year'].astype(int)

# Step 6: Merge West Germany and Germany
df['Winner'] = df['Winner'].replace({'West Germany': 'Germany'})
df['RunnerUp'] = df['RunnerUp'].replace({'West Germany': 'Germany'})

# Optional: Save to CSV
df.to_csv('fifa_world_cup_finals.csv', index=False)

# Preview the result
print(df.head())



import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('fifa_world_cup_finals.csv')

# Calculate win counts
win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']

# Merge Germany & West Germany already handled

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # required for Render deployment

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
        options=[{'label': c, 'value': c} for c in sorted(win_counts['Country'])],
        id='country-dropdown'
    ),
    html.Div(id='country-output'),

    html.Br(),

    html.Label("Select a Year:"),
    dcc.Dropdown(
        options=[{'label': y, 'value': y} for y in sorted(df['Year'])],
        id='year-dropdown'
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

if __name__ == '__main__':
    app.run(debug=True)




