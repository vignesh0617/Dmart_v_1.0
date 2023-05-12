import dash_bootstrap_components as dbc
from helper_functions.custom_helpers import main_app
from dash import html


navbar = html.Div([dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About",href = main_app.environment_details['about_page_link'],active="exact")),
        dbc.NavItem(dbc.NavLink("Home",href = main_app.environment_details['home_page_link'],active="exact")),
        dbc.NavItem(dbc.NavLink("Logout",href = main_app.environment_details['logout_page_link'],active="exact")),
    ],
    brand="Dmart",
    brand_href="#",
    color="primary",
    dark="dark"
)], className="navbar")
