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
            >
            </LoginForm>
        );
    }
}

export default App;
