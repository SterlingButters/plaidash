// /* eslint no-magic-numbers: 0 */
import React, { Component } from 'react';
import { LoginForm } from '../lib';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
        };

        this.setProps = this.setProps.bind(this);
    }

    setProps(newProps) {
        console.log(newProps);
        this.setState(newProps);
    }

    render() {
        return (
            <LoginForm
                setProps={this.setProps}
                {...this.state}

                // id="Test"
                // clientName="Plaid Client"
                // env="sandbox"
                // product={['auth', 'transactions']}
                // publicKey="7a3daf1db208b7d1fe65850572eeb1"
                // apiVersion="v2"
            >
            </LoginForm>
        );
    }
}

export default App;
