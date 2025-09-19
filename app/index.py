from dash import Dash, dash_table, html, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc

df = pd.read_csv('uncertainties.csv', skip_blank_lines=False)
df.dropna(subset=['ID'], inplace=True)
df.rename(columns={"ID": "id"}, inplace=True)
df.set_index('id', inplace=True, drop=False)

table1 = dash_table.DataTable(
    id='datatable-uncertainties',
    data=df.to_dict('records'),
    columns=[
        {"name": i, "id": i, "selectable": True} for i in df.columns
    ],
    fixed_rows={'headers': True},
    page_action='none',
    fixed_columns={'headers': True, 'data': 2},
    style_table={
        'height': '400px',
        'maxHeight': '400px',
        'minWidth': '100%',
        'padding-bottom': '50px',
        'padding-left': '30px'
    },
    style_cell_conditional=[
        {
            'if': {'column_id': 'id'},
            'width': '25px'
        },
        {
            'if': {'column_id': 'NAME'},
            'width': '150px'
        },
        {
            'if': {'column_id': 'CLASSIFICATION'},
            'width': '150px'
        },
    ],
    style_cell={
        'whiteSpace': 'normal',
        'textAlign': 'left',
        'lineHeight': '15px',
        'maxWidth': '450px',
        'padding': '5px'
    },
    sort_action='native',
    style_as_list_view=True,
    style_header={
        'fontWeight': 'bold',
        'backgroundColor': 'DodgerBlue',
        'color': 'white',
    },
    style_data={
        'backgroundColor': 'grey',
        'color': 'white',
    },
    filter_action="native",
    row_selectable='multi',
    selected_rows=[],
)

class MainApplication:

    def __init__(self):
        self.__app = Dash(
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
        self.set_layout()

    def app(self):
        return self.__app

    def set_layout(self):
        self.__app.layout= [
            html.H1(children='Software Uncertainties Repository - SURE!', style={'textAlign':'center'}),
            html.Div(
                dbc.Button("Toggle view", color="secondary", id='toggle-val', n_clicks=0, style={"margin-bottom": "10px"}),
                style={'display':'flex', "justify-content": "center"}
            ),
            html.Div([html.H2(children='Uncertainties', style={'textAlign':'left', 'padding-left': '30px'}), table1], style={'width':'1300px'}, id='datatable-div-uncertainties'),
            html.Div(style={'width':'1300px'}, id='datatable-requirements'),
        ]

    @callback(
        Output('datatable-div-uncertainties', 'children'),
        Input('toggle-val', 'n_clicks')
    )
    def update_uncertainties_table(n_clicks):
        if n_clicks % 2:
            style_cell = {
                'whiteSpace': 'normal',
                'textAlign': 'left',
                'lineHeight': '15px',
                'maxWidth': '450px',
                'padding': '5px'
            }
            tooltip_data = []
        else:
            style_cell = {
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'textAlign': 'left',
                'lineHeight': '15px',
                'maxWidth': '450px',
                'padding': '10px'
            }
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ]

        table1 = dash_table.DataTable(
            id='datatable-uncertainties',
            data=df.to_dict('records'),
            columns=[
                {"name": i, "id": i, "selectable": True} for i in df.columns
            ],
            fixed_rows={'headers': True},
            page_action='none',
            fixed_columns={'headers': True, 'data': 2},
            style_table={
                'height': '400px',
                'maxHeight': '400px',
                'minWidth': '100%',
                'padding-bottom': '50px',
                'padding-left': '30px'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': 'id'},
                    'width': '25px'
                },
                {
                    'if': {'column_id': 'NAME'},
                    'width': '150px'
                },
                {
                    'if': {'column_id': 'CLASSIFICATION'},
                    'width': '150px'
                },
            ],
            style_cell= style_cell,
            sort_action='native',
            style_as_list_view=True,
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'DodgerBlue',
                'color': 'white',
            },
            style_data={
                'backgroundColor': 'grey',
                'color': 'white',
            },
            filter_action="native",
            row_selectable='multi',
            selected_rows=[],
            tooltip_data = tooltip_data,
            tooltip_duration=None
        )
        return [html.H2(children='Uncertainties', style={'textAlign':'left', 'padding-left': '30px'}), table1]


    @callback(
        Output('datatable-requirements', "children"),
        Input('datatable-uncertainties', "selected_row_ids"),
        prevent_initial_call=True)
    def update_requirements_table(selected_row_ids):
        selected_id_set = set(selected_row_ids or [])
        req_df = pd.read_csv('relax_reqs.csv', skip_blank_lines=False)
        req_df = req_df.loc[req_df['U_ID'].isin(selected_id_set)]

        table2 = dash_table.DataTable(
            data=req_df.to_dict('records'),
            columns=[
                {"name": i, "id": i, "selectable": True} for i in req_df.columns
            ],
            fixed_rows={'headers': True},
            page_action='none',
            fixed_columns={'headers': True, 'data': 2},
            style_table={
                'height': '400px',
                'maxHeight': '400px',
                'minWidth': '100%',
                'padding-bottom': '30px',
                'padding-left': '30px'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': 'ID'},
                    'width': '50px'
                },
                {
                    'if': {'column_id': 'U_ID'},
                    'width': '70px'
                },
                {
                    'if': {'column_id': 'Requirement'},
                    'width': '150px'
                },
            ],
            style_cell={
                'whiteSpace': 'normal',
                'textAlign': 'left',
                'lineHeight': '15px',
                # 'width': '250px',
                'maxWidth': '250px',
                'padding': '5px'
            },
            sort_action='native',
            style_as_list_view=True,
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'DodgerBlue',
                'color': 'white',
            },
            style_data={
                'backgroundColor': 'grey',
                'color': 'white',
            },
        )
        if len(selected_id_set)> 0:
            return [html.H2(children='Requirements', style={'textAlign':'left', 'padding-left': '30px'}), table2]
        else:
            return []


Application = MainApplication()
app = Application.__app.server

if __name__ == "__main__":
    Application.__app.run(port=8080, dev_tools_ui=True, debug=True, host="0.0.0.0")