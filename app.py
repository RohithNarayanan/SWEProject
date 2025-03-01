import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize Flask app
server = Flask(__name__)
server.config['SECRET_KEY'] = 'your-secret-key'
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(server)
login_manager = LoginManager(server)
login_manager.login_view = 'login'

# Initialize Dash app
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True  # Suppress callback exceptions
)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # user, vendor, admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create database tables
with server.app_context():
    db.create_all()

# Custom styles
app_layout_style = {
    'backgroundColor': '#F0EADC',  # Eggshell background
    'minHeight': '100vh',
    'padding': '20px',
    'fontFamily': 'Times New Roman'
}

title_style = {
    'color': '#576238',  # Moss color
    'textAlign': 'center',
    'marginTop': '20px',
    'marginBottom': '40px',
    'fontFamily': 'Times New Roman'
}

button_style = {
    'margin': '10px',
    'width': '100px',
    'backgroundColor': '#FFD95D',  # Mustard buttons
    'color': 'black',
    'fontFamily': 'Times New Roman'
}

navbar_style = {
    'display': 'flex',
    'justifyContent': 'flex-end',
    'padding': '10px'
}

beige_box_style = {
    'backgroundColor': '#F0EADC',  # Eggshell color
    'width': '80%',
    'height': '200px',
    'margin': 'auto',
    'marginTop': '50px',
    'padding': '20px',
    'textAlign': 'center',
    'borderRadius': '10px',
    'fontFamily': 'Times New Roman'
}

# Layout of the Dash app
app.layout = dbc.Container(style=app_layout_style, children=[
    dcc.Location(id='url', refresh=False),
    html.Div(style=navbar_style, children=[
        dbc.Button("Login", id='login-button', href='/login', style=button_style),
        dbc.Button("Register", id='register-button', href='/register', style=button_style)
    ]),
    html.Div(id='page-content'),
    html.Div(style=beige_box_style, children=[
        html.H3("Image Gallery", style={'fontFamily': 'Times New Roman'}),
        html.Div(id='image-container')
    ])
])

# Login callback
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    prevent_initial_call=True
)
def display_page(pathname):
    if pathname == '/login':
        return html.Div([
            html.H1("Login", style=title_style),
            dbc.Input(id='login-email', type='email', placeholder="Email", style={'margin': '10px'}),
            dbc.Input(id='login-password', type='password', placeholder="Password", style={'margin': '10px'}),
            dbc.Button("Submit", id='login-submit-button', n_clicks=0, style=button_style),
            html.Div(id='login-message')
        ])
    elif pathname == '/register':
        return html.Div([
            html.H1("Register", style=title_style),
            dbc.Input(id='register-name', type='text', placeholder="Name", style={'margin': '10px'}),
            dbc.Input(id='register-email', type='email', placeholder="Email", style={'margin': '10px'}),
            dbc.Input(id='register-password', type='password', placeholder="Password", style={'margin': '10px'}),
            dbc.Button("Submit", id='register-submit-button', n_clicks=0, style=button_style),
            html.Div(id='register-message')
        ])
    return html.H1("Welcome to RentitEase", style=title_style)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)