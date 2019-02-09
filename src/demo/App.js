// /* eslint no-magic-numbers: 0 */
import React, { Component } from 'react';
import { LoginForm } from '../lib';

class App extends Component {
    constructor(props) {
        super(props);
    }
    handleOnSuccess(token, metadata) {
        console.log(token);
        console.log(metadata);
    }
    handleOnExit(error, metadata) {
        console.log('link: user exited');
        console.log(error, metadata);
    }
    handleOnLoad() {
        console.log('link: loaded');
    }
    handleOnEvent(eventname, metadata) {
        console.log('link: user event', eventname, metadata);
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
                apiVersion="v2"
                onSuccess={this.handleOnSuccess}
                onExit={this.handleOnExit}
                onEvent={this.handleOnEvent}
                onLoad={this.handleOnLoad}>
            </LoginForm>
        );
    }
}

export default App;
