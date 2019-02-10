// /* eslint no-magic-numbers: 0 */
import React, { Component } from 'react';
import { LoginForm } from '../lib';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            access_token: null
        };
        this.handleUpdateToken = this.handleUpdateToken.bind(this)
    }

    handleUpdateToken(access_token) {
        this.setState({ access_token: access_token });
    }

    render() {
        return (
            <LoginForm
                id="Test"
                access_token={this.state.access_token}

                clientName="Plaid Client"
                env="sandbox"
                product={['auth', 'transactions']}
                publicKey="7a3daf1db208b7d1fe65850572eeb1"
                className="some-class-name"
                apiVersion="v2"
                onTokenUpdate={this.handleUpdateToken}
            >
            </LoginForm>
        );
    }
}

export default App;
