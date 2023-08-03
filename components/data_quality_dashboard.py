from dash import html, dcc 

layout = html.Div([
    html.Div([
            html.Div([
                dcc.Graph(id="fig_1"),
                dcc.Graph(id="fig_2"),
        ],className="top-figures",id="top_figures"), 
        html.Div(id="top_table",className="top-table")
    ],id="home_page_contents_top",className="home-page-contents-top"),
    html.Div([
        html.Div(id="bottom_table",className = "bottom-table"),
        html.Div(id="bottom_table_failed_records",className="bottom-table-failed-records")
    ],id="home_page_contents_bottom",className="home-page-contents-bottom"),
],id = "data_quality_dashboard")