# https://plaid.com/docs/#exchange-token-flow
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_html_components as html
import dash_core_components as dcc
import dash
import json
import plaid
import pandas as pd
import os
import plaidash
import datetime
from flask import jsonify

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=stylesheet)
app.config['suppress_callback_exceptions'] = True

with open('/Users/sterlingbutters/.plaid/.credentials.json') as CREDENTIALS:
    KEYS = json.load(CREDENTIALS)
    print(json.dumps(KEYS, indent=2))

    PLAID_CLIENT_ID = KEYS['client_id']
    PLAID_PUBLIC_KEY = KEYS['public_key']
    ENV = 'sandbox'
    if ENV == 'development':
        PLAID_SECRET = KEYS['development_secret']
    else:
        PLAID_SECRET = KEYS['sandbox_secret']
    PLAID_ENV = os.getenv('PLAID_ENV', ENV)
    PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS', ['auth', 'transactions'])


def pretty_response(response):
    return json.dumps(response, indent=2, sort_keys=True)


def format_error(e):
    return {'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type,}} # 'error_message': e.message } }


app.layout = html.Div([
    # Will lose the data when browser/tab closes.
    dcc.Store(id='public-tokens', storage_type='session', data={'tokens': []}),
    html.Button('Store current token', id='store-button'),
    html.Div(id='display-tokens'),

    plaidash.LoginForm(
            id='plaid-link',
            clientName='Butters',
            env=PLAID_ENV,
            publicKey=PLAID_PUBLIC_KEY,
            product=PLAID_PRODUCTS,
            # institution=
        ),
    html.Div(id='transaction-table'),
])

client = plaid.Client(client_id=PLAID_CLIENT_ID,
                      secret=PLAID_SECRET,
                      public_key=PLAID_PUBLIC_KEY,
                      environment=PLAID_ENV,
                      api_version='2018-05-22')


##################################################################
# Commit to Memory
@app.callback(Output('public-tokens', 'data'),
              [Input('store-button', 'n_clicks')],
              [State('plaid-link', 'public_token'),
               State('public-tokens', 'data')])
def on_click(clicks, public_token, data):
    if clicks is None:
        raise PreventUpdate

    stored_tokens = data['tokens'] or []
    stored_tokens.append(public_token)
    data = {'tokens': stored_tokens}

    return data

##################################################################


# Display from Memory
@app.callback(Output('transaction-table', 'children'),
              [Input('public-tokens', 'modified_timestamp')],
              [State('public-tokens', 'data')])
def display_output(timestamp, data):
    if timestamp is None:
        raise PreventUpdate

    data = data or {}
    STORED_TOKENS = data.get('tokens')

    if len(STORED_TOKENS) >= 1:
        if STORED_TOKENS[-1] is not None:
            public_token = STORED_TOKENS[-1]
            response = client.Item.public_token.exchange(public_token)
            access_token = response['access_token']
            print("Public Token '{}' was exchanged for Access Token '{}'".format(public_token, access_token))

            start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-30))
            end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
            try:
                transactions_response = client.Transactions.get(access_token=access_token, start_date=start_date,
                                                                end_date=end_date)

            except plaid.errors.PlaidError as e:
                # return html.P(jsonify(format_error(e)))
                return html.P('There was an error')

            transactions = transactions_response.get('transactions')

            names = [transaction['name'] for transaction in transactions]
            categories = [transaction['category'] for transaction in transactions]
            locations = [transaction['location'] for transaction in transactions]
            statuses = [transaction['pending'] for transaction in transactions]
            amounts = [transaction['amount'] for transaction in transactions]
            # Payment Method: payment_meta
            dates = [transaction['date'] for transaction in transactions]
            id = [transaction['transaction_id'] for transaction in transactions]

            TOKEN_MEAT = []
            for a in range(len(STORED_TOKENS)):
                if a is not None:
                    TOKEN_MEAT.append(html.Tr([html.Td(STORED_TOKENS[a]), '']))

            INFO_MEAT = []
            for b in range(len(transactions)):
                INFO_MEAT.append(html.Tr([html.Td(names[b]), html.Td(amounts[b]), html.Td(dates[b])]))

            return html.Div([
                            html.Table([
                                html.Thead([
                                    html.Tr([
                                        html.Th('Stored Public Tokens'),
                                    ]),
                                    html.Tbody([
                                        *TOKEN_MEAT,
                                        ])
                                    ]),

                            html.Table([
                                html.Thead([
                                    html.Tr([
                                        html.Th('Name'),
                                        html.Th('Amount'),
                                        html.Th('Date')
                                        ])
                                    ]),
                                    html.Tbody([
                                        *INFO_MEAT,
                                        ])
                                    ])
                            ])
            ])

        else:
            return "Navigate Plaid Link to Obtain Token"


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)
