import plaidash
import dash
from dash.dependencies import Input, Output
import dash_html_components as html

app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.layout = html.Div([
    plaidash.LoginForm(
        id='plaid-link',
        clientName='Btters',
        env='development',
        publicKey='7a3daf1db208b7d1fe65850572eeb1',
        product=['auth', 'transactions'],
    ),
    html.Div(id='display-token')
])


@app.callback(Output('display-token', 'children'),
             [Input('plaid-link', 'token'),])
def display_output(token):
    return html.P('Token: {}'.format(token))


if __name__ == '__main__':
    app.run_server(debug=True)
