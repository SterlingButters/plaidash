# https://plaid.com/docs/#exchange-token-flow
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash
import json
import plaid
import os
import plaidash
import datetime
from flask import jsonify

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.Div(id='login-container'),
    html.Button('Open Plaid', id='open-form-button'),
])

PLAID_CLIENT_ID = ''
PLAID_SECRET = ''
PLAID_PUBLIC_KEY = ''
PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS', ['auth', 'transactions'])

client = plaid.Client(client_id=PLAID_CLIENT_ID,
                      secret=PLAID_SECRET,
                      public_key=PLAID_PUBLIC_KEY,
                      environment=PLAID_ENV,
                      api_version='2018-05-22')


@app.callback(Output('login-container', 'children'),
              [Input('open-form-button', 'n_clicks'),])
def display_output(clicks):
    if clicks is not None and clicks > 0:
        return html.Div([
            plaidash.LoginForm(
            id='plaid-link',
            clientName='Butters',
            env=PLAID_ENV,
            publicKey=PLAID_PUBLIC_KEY,
            product=PLAID_PRODUCTS,
            # institution=
        ),
            html.Button('Load Transactions', id='load-button'),
            html.Div(id='display-transactions'),
        ])


@app.callback(Output('display-transactions', 'children'),
             [Input('load-button', 'n_clicks')],
             [State('plaid-link', 'access_token')])
def display_output(clicks, token):
    if clicks is not None and clicks > 0:
        print(token)
        response = client.Item.public_token.exchange(token)
        access_token = response['access_token']
        print(access_token)

        start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-30))
        end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
        try:
            transactions_response = client.Transactions.get(access_token=access_token, start_date=start_date, end_date=end_date)
        except plaid.errors.PlaidError as e:
            # return html.P(jsonify(format_error(e)))
            return html.P('There was an error')

        print(pretty_response(transactions_response))
        # return html.P(str(jsonify({'error': None, 'transactions': transactions_response})))
        return html.P(pretty_response(transactions_response))


def pretty_response(response):
    return json.dumps(response, indent=2, sort_keys=True)


def format_error(e):
    return {'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type,}} # 'error_message': e.message } }


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)
