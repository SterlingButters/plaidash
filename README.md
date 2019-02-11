# Plaidash LoginForm
The purpose of this project is to create a dash component for the plaid link for easy rendering and use 
with python once an `access_token` is retrieved.

![alt text](https://github.com/SterlingButters/plaidash/blob/master/PlaidDemo.gif)

### Component written in 
`src/lib/components/LoginForm.react.js`. 

### Acknowledgements
A special thanks to:
 [@tcbegley](https://community.plot.ly/u/tcbegley)
 [@pbernasconi](https://github.com/pbernasconi/react-plaid-link)



# TODO:
- The demo app is in `src/demo` and you will import your example component code into your demo app.
- Test your code in a Python environment:
    1. Build your code
        ```
        $ npm run build:all
        ```
    2. Run and modify the `usage.py` sample dash app:
        ```
        $ python usage.py
        ```
        
##### Sample Usage:

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
        html.Div(id='login-container'),
        html.Div(id='display-transactions'),
        html.Button('Open Plaid', id='open-form-button'),
    ])
    
    @app.callback(Output('login-container', 'children'),
                  [Input('open-form-button', 'n_clicks'),])
    def display_output(clicks):
        if clicks is not None and clicks > 0:
            return plaidash.LoginForm(
                id='plaid-link',
                clientName='Butters',
                env='sandbox',
                publicKey='7a3daf1db208b7d1fe65850572eeb1',
                product=['auth', 'transactions'],
            ),
   
   
    @app.callback(Output('display-transactions', 'children'),
                 [Input('plaid-link', 'access_token'),])
    def display_output(token):
        print(token)
   
        start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-30))
        end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
        try:
            transactions_response = plaid.client.Transactions.get(access_token=token, start_date=start_date, end_date=end_date)
        except plaid.errors.PlaidError as e:
            return jsonify(format_error(e))
   
        pretty_print_response(transactions_response)
        return html.P(jsonify({'error': None, 'transactions': transactions_response}))
    
    
    if __name__ == '__main__':
        app.run_server(debug=True)

- Write tests for your component.
    - A sample test is available in `tests/test_usage.py`, it will load `usage.py` and you can then automate interactions with selenium.
    - Run the tests with `$ pytest tests`.
    - The Dash team uses these types of integration tests extensively. Browse the Dash component code on GitHub for more examples of testing (e.g. https://github.com/plotly/dash-core-components)
- Add custom styles to your component by putting your custom CSS files into your distribution folder (`plaidash`).
    - Make sure that they are referenced in `MANIFEST.in` so that they get properly included when you're ready to publish your component.
    - Make sure the stylesheets are added to the `_css_dist` dict in `plaidash/__init__.py` so dash will serve them automatically when the component suite is requested.
- [Review your code](./review_checklist.md)

### Create a production build and publish:

1. Build your code:
    ```
    $ npm run build:all
    ```
2. Create a Python tarball
    ```
    $ python setup.py sdist
    ```
    This distribution tarball will get generated in the `dist/` folder

3. Test your tarball by copying it into a new environment and installing it locally:
    ```
    $ pip install plaidash-0.0.1.tar.gz
    ```

4. If it works, then you can publish the component to NPM and PyPI:
    1. Cleanup the dist folder (optional)
        ```
        $ rm -rf dist
        ```
    2. Publish on PyPI
        ```
        $ twine upload dist/*
        ```
    3. Publish on NPM (Optional if chosen False in `publish_on_npm`)
        ```
        $ npm publish
        ```
        _Publishing your component to NPM will make the JavaScript bundles available on the unpkg CDN. By default, Dash servers the component library's CSS and JS from the remote unpkg CDN, so if you haven't published the component package to NPM you'll need to set the `serve_locally` flags to `True` (unless you choose `False` on `publish_on_npm`). We will eventually make `serve_locally=True` the default, [follow our progress in this issue](https://github.com/plotly/dash/issues/284)._
