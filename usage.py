# https://plaid.com/docs/#exchange-token-flow
from dash.dependencies import Input, Output
import dash_html_components as html
import dash
import plaid
import plaidash
import datetime
from flask import jsonify

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    # html.Div(id='login-container'),
    # html.Div(id='display-transactions'),
    # html.Button('Open Plaid', id='open-form-button'),

    plaidash.LoginForm(
            id='plaid-link',
            clientName='Butters',
            env='sandbox',
            publicKey='7a3daf1db208b7d1fe65850572eeb1',
            product=['auth', 'transactions'],
        ),
])

# @app.callback(Output('login-container', 'children'),
#               [Input('open-form-button', 'n_clicks'),])
# def display_output(clicks):
#     if clicks is not None and clicks > 0:
#         return plaidash.LoginForm(
#             id='plaid-link',
#             clientName='Butters',
#             env='sandbox',
#             publicKey='7a3daf1db208b7d1fe65850572eeb1',
#             product=['auth', 'transactions'],
#         ),
#
#
# @app.callback(Output('display-transactions', 'children'),
#              [Input('plaid-link', 'access_token'),])
# def display_output(token):
#     print(token)
#
#     start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-30))
#     end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
#     try:
#         transactions_response = plaid.client.Transactions.get(access_token=token, start_date=start_date, end_date=end_date)
#     except plaid.errors.PlaidError as e:
#         return jsonify(format_error(e))
#
#     pretty_print_response(transactions_response)
#     return html.P(jsonify({'error': None, 'transactions': transactions_response}))


if __name__ == '__main__':
    app.run_server(debug=True)
