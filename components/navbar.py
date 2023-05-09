import dash_bootstrap_components as dbc
from helper_functions.custom_helpers import main_app
from dash import html

# right_side_nav_items = ([
#     dbc.NavItem(dbc.NavLink("About",href = main_app.environment_details['about_page_link'],active="exact")),
#     dbc.NavItem(dbc.NavLink("Logout",href = main_app.environment_details['logout_page_link'],active="exact"))
# ]) 

# left_side_nav_items = ([
#     dbc.NavItem(dbc.NavLink("Dmart",href = "#",active="exact"))
# ])

# navbar = dbc.Navbar([
#     dbc.Nav([
#         left_side_nav_items,
#         right_side_nav_items
#     ])
    
# ],color = "#B0DAFF", className = "fw-bold")

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About",href = main_app.environment_details['about_page_link'],active="exact")),
        dbc.NavItem(dbc.NavLink("Home",href = main_app.environment_details['home_page_link'],active="exact")),
        dbc.NavItem(dbc.NavLink("Logout",href = main_app.environment_details['logout_page_link'],active="exact")),
        # dbc.NavItem(dbc.NavLink("test2",href = "test2",active="exact")),
        # dbc.NavItem(dbc.NavLink("test3",href = "test3",active="exact")),
        # dbc.NavItem(dbc.NavLink("test4",href = "test4",active="exact")),
        # dbc.NavItem(dbc.NavLink("test5",href = "test5",active="exact")),
        # dbc.NavItem(dbc.NavLink("test6",href = "test6",active="exact")),
    ],
    brand="Dmart",
    brand_href="#",
    color="primary",
    dark="dark"
)
