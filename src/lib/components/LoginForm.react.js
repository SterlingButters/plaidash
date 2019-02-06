import React, {Component} from 'react';
import PropTypes from 'prop-types';
import PlaidLink from 'react-plaid-link'

export default class LoginForm extends Component {
    constructor(props) {
        super(props);
        this.state = props
    }

    handleOnSuccess(token, metadata) {
        // send token to client server
        this.props.setProps({token: token})
    }
    handleOnExit() {
        // handle the case when your user exits Link
    }
    render() {
        let id;
        let clientName;
        let environment;
        let publicKey;
        let token;

        if (this.props.setProps) {
            id = this.props.id;
            clientName = this.props.clientName;
            environment = this.props.env;
            publicKey = this.props.publicKey;
            token = this.props.token;
        } else {
            id = this.state.id;
            clientName = this.state.clientName;
            environment = this.state.env;
            publicKey = this.state.publicKey;
            token = this.state.token;
        }
        return (
            <div id={id}>
                <PlaidLink
                    clientName={clientName}
                    env={environment}
                    institution={null}
                    publicKey={publicKey}
                    product={["auth", "transactions"]}
                    token={token}
                    // webhook="https://webhooks.test.com"
                    // onEvent={this.handleOnEvent}
                    onExit={this.handleOnExit}
                    // onLoad={this.handleOnLoad}
                    onSuccess={this.handleOnSuccess}>
                    Open Link and connect your bank!
                </PlaidLink>
                <p>Test</p>
            </div>
        )
    }
}

LoginForm.defaultProps = {};

LoginForm.propTypes = {
    /**
     *
     */
    id: PropTypes.string,

    /**
     *
     */
    clientName: PropTypes.string,

    /**
     * Dash-assigned callback that should be called whenever any of the
     * properties change
     */
    env: PropTypes.string.isRequired,

    /**
     *
     */
    publicKey: PropTypes.string.isRequired,

    /**
     *
     */
    product: PropTypes.array.isRequired,

    /**
     *
     */
    onExit: PropTypes.func,

    /**
     *
     */
    onSuccess: PropTypes.func,

    /**
     *
     */
    setProps: PropTypes.func.isRequired,

    token: PropTypes.string
};