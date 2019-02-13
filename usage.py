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

app = dash.Dash(__name__)
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

app.layout = html.Div([
    # Will lose the data when browser/tab closes.
    dcc.Store(id='public-tokens', storage_type='session'),
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
    html.Button('Load Transactions', id='load-button'),
    html.Div(id='display-transactions'),
])

client = plaid.Client(client_id=PLAID_CLIENT_ID,
                      secret=PLAID_SECRET,
                      public_key=PLAID_PUBLIC_KEY,
                      environment=PLAID_ENV,
                      api_version='2018-05-22')


##################################################################
@app.callback(Output('public-tokens', 'data'),
              [Input('store-button', 'n_clicks')],
              [State('plaid-link', 'public_token'),
               State('public-tokens', 'data'),])
def on_click(clicks, public_token, data):
    if clicks is None:
        # Preventing the None callbacks is important with the store component,
        # you don't want to update the store for nothing.
        raise PreventUpdate

    if data is None:
        data = {'tokens': []}
    else:
        stored_tokens = data['tokens'] or []
        stored_tokens.append(public_token)
        data = {'tokens': stored_tokens}
    return data


# output the stored clicks in the table cell.
@app.callback(Output('display-tokens', 'children'),
              [Input('public-tokens', 'modified_timestamp')],
              [State('public-tokens', 'data')])
def on_data(ts, data):
    if ts is None:
        raise PreventUpdate

    data = data or {}
    STORED_TOKENS = data.get('tokens')
    print(STORED_TOKENS)
    return dcc.Markdown('''```{}```'''.format(pd.Series(STORED_TOKENS)))
##################################################################


@app.callback(Output('display-transactions', 'children'),
              [Input('load-button', 'n_clicks')],
              [State('plaid-link', 'public_token')])
def display_output(clicks, public_token):
    if clicks is not None and clicks > 0:
        response = client.Item.public_token.exchange(public_token)
        access_token = response['access_token']
        print("Public Token {} was exchanged for Access Token {}".format(public_token, access_token))

        start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-30))
        end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
        try:
            transactions_response = client.Transactions.get(access_token=access_token, start_date=start_date, end_date=end_date)
        except plaid.errors.PlaidError as e:
            # return html.P(jsonify(format_error(e)))
            return html.P('There was an error')

        # print(pretty_response(transactions_response))
        return dcc.Markdown('''```json
        {}```'''.format(pretty_response(transactions_response)))


def pretty_response(response):
    return json.dumps(response, indent=2, sort_keys=True)


def format_error(e):
    return {'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type,}} # 'error_message': e.message } }


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)
