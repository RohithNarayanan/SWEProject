import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import sqlite3
import pandas as pd

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Sample product data (Replace with database integration)
products = [
    {"id": 1, "name": "Laptop", "price": 50000, "brand": "Brand A", "size": "Medium", "design": "Modern", "location": "Hyderabad", "image": "https://via.placeholder.com/150"},
    {"id": 2, "name": "Camera", "price": 30000, "brand": "Brand B", "size": "Small", "design": "Classic", "location": "Bangalore", "image": "https://via.placeholder.com/150"},
    {"id": 3, "name": "Bike", "price": 150000, "brand": "Brand C", "size": "Large", "design": "Minimalist", "location": "Chennai", "image": "https://via.placeholder.com/150"}
]

# Layout with sidebar and search bar
app.layout = html.Div([
    html.Div([
        html.H2("RentItEase", style={'textAlign': 'center', 'color': 'white'}),
        html.Hr(),
        dcc.Link('Browse Items', href='/', style={'display': 'block', 'color': 'white', 'padding': '10px'}),
        dcc.Link('My Profile', href='/profile', style={'display': 'block', 'color': 'white', 'padding': '10px'}),
        dcc.Link('Rental History', href='/history', style={'display': 'block', 'color': 'white', 'padding': '10px'})
    ], style={
        'width': '200px', 'position': 'fixed', 'top': 0, 'left': 0, 'bottom': 0, 'background': '#90EE90',
        'padding': '20px', 'color': 'white'
    }),
    
    html.Div([
        dcc.Input(
            id='search-bar',
            type='text',
            placeholder='Search products...',
            style={
                'width': '50%', 'padding': '10px', 'borderRadius': '20px', 'border': '1px solid #ccc',
                'display': 'block', 'margin': '20px auto', 'textAlign': 'center'
            }
        ),
        html.Div([
            dcc.Checklist(
                id='brand-filter',
                options=[
                    {'label': 'Brand A', 'value': 'A'},
                    {'label': 'Brand B', 'value': 'B'},
                    {'label': 'Brand C', 'value': 'C'}
                ],
                labelStyle={'display': 'inline-block', 'marginRight': '10px'}
            ),
            dcc.Checklist(
                id='size-filter',
                options=[
                    {'label': 'Small', 'value': 'S'},
                    {'label': 'Medium', 'value': 'M'},
                    {'label': 'Large', 'value': 'L'}
                ],
                labelStyle={'display': 'inline-block', 'marginRight': '10px'}
            ),
            dcc.Checklist(
                id='design-filter',
                options=[
                    {'label': 'Modern', 'value': 'Modern'},
                    {'label': 'Classic', 'value': 'Classic'},
                    {'label': 'Minimalist', 'value': 'Minimalist'}
                ],
                labelStyle={'display': 'inline-block', 'marginRight': '10px'}
            )
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),
        dcc.RangeSlider(
            id='price-slider',
            min=0,
            max=200000,
            step=1000,
            marks={i: f'₹{i}' for i in range(0, 200001, 50000)},
            value=[10000, 100000],
        ),
        html.Div(id='product-grid', style={'display': 'grid', 'gridTemplateColumns': 'repeat(3, 1fr)', 'gap': '20px', 'padding': '20px'})
    ], style={'marginLeft': '220px', 'padding': '20px', 'background': '#FFFF99'})
])

@app.callback(
    Output('product-grid', 'children'),
    [Input('search-bar', 'value')]
)
def update_products(search_query):
    filtered_products = [p for p in products if search_query.lower() in p['name'].lower()] if search_query else products
    return [
        html.Div([
            html.Img(src=p['image'], style={'width': '100%', 'borderRadius': '10px'}),
            html.H4(p['name']),
            html.P(f"Price: ₹{p['price']}", style={'color': 'green'}),
            html.P(f"Brand: {p['brand']}", style={'color': 'blue'}),
            html.P(f"Location: {p['location']}", style={'color': 'gray'})
        ], style={'border': '1px solid #ddd', 'padding': '10px', 'borderRadius': '10px', 'background': 'white'})
        for p in filtered_products
    ]

if __name__ == '__main__':
    app.run_server(debug=True)