from dash.dependencies import Output, Input, State
from callback_functions.custom_helpers import main_app

@main_app.app.callback(
    Output("show-hide-button","className"),
    Output("show-hide-popover","children"),
    Output("side-filter-tab-container","style"),
    Output("main-content-container","style"),
    Input("show-hide-button","n_clicks"),
    State("show-hide-button","className"),
    prevent_initial_call=True)
def toggle_buttons(n_clicks,class_name):
    if(n_clicks%2==1):
        return class_name.replace("right","left"),"Hide Filters",{"left":"0px"},{"width":"70%","margin-left":"30%"}
    else:
        return class_name.replace("left","right"),"Show Filters",{},{}
