// /* eslint no-magic-numbers: 0 */
import React, { Component } from 'react';
import { LoginForm } from '../lib';

class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <LoginForm
                id="Test"
                clientName="Plaid Client"
                env="sandbox"
                product={['auth', 'transactions']}
                publicKey="7a3daf1db208b7d1fe65850572eeb1"
                className="some-class-name"
                apiVersion="v2">
            </LoginForm>
        );
    }
}

export default App;
