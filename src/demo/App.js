// /* eslint no-magic-numbers: 0 */
import React, { Component } from 'react';
import { LoginForm } from '../lib';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {

        };
        let access_token = null;
    }

    changeChild(data, func) {
        let changedData = data;
        // change data in here
        if (data === '') {
            changedData = "Empty String";
        }
        // parent storing data for him
        this.childData = changedData;
        // send it back to the child
        func(changedData);
    };

    render() {
        console.log("LoginForm Rendered");
        return (
            <LoginForm
                id="Test"
                clientName="Plaid Client"
                env="sandbox"
                product={['auth', 'transactions']}
                publicKey="7a3daf1db208b7d1fe65850572eeb1"
                className="some-class-name"
                apiVersion="v2"
                updateToken={this.changeChild}
                token={this.state.childData}
            >
            </LoginForm>
        );
    }
}

export default App;
