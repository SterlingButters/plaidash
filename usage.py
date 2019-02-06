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
        clientName='Butters',
        env='development',
        # institution=,
        publicKey='7a3daf1db208b7d1fe65850572eeb1',
        # product=,
        # token=,
    ),
    html.Div(id='output')
])

@app.callback(Output('output', 'children'), [Input('input', 'value')])
def display_output(value):
    return 'You have entered {}'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
