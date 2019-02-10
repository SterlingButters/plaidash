// /* eslint no-magic-numbers: 0 */
import React, { Component } from 'react';
import { LoginForm } from '../lib';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {

        };
    }

    changeChild(data, func) {
        let changedData = data;
        // change data in here
        if (data === null || undefined) {
            changedData = "Empty";
        }
        console.log("Data Received By Parent:", changedData);

        // parent storing data for him
        // was "this.childData"
        // this.props.childData = changedData;
        // set data state in child via passed function
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
                savedToken={this.state.savedToken}
            >
            </LoginForm>
        );
    }
}

export default App;
