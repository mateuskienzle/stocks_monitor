# from datetime import date
# from dash import Dash, html, dcc
# from dash.dependencies import Input, Output

# from datetime import date

# # app = Dash(__name__)
# hoje = date.today()
# # app.layout = html.Div([
#     dcc.DatePickerSingle(
#         id='my-date-picker-single',
#         min_date_allowed=date(2005, 1, 1),
#         max_date_allowed=date(hoje.year, hoje.month, hoje.day),
#         initial_visible_month=date(2017, 8, 5),
#         date=date(hoje.year, hoje.month, hoje.day)
#     ),
#     html.Div(id='output-container-date-picker-single')
# ])


# @app.callback(
#     Output('output-container-date-picker-single', 'children'),
#     Input('my-date-picker-single', 'date'))
# def update_output(date_value):
#     if date_value is not None:
#         date_object = date.fromisoformat(date_value)
#         date_string = date_object.strftime('%B %d, %Y')
#         return date_string


# # if __name__ == '__main__':
# #     app.run_server(debug=True)
