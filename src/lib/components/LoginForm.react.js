import React, { Component } from 'react';
import Script from 'react-load-script';
import PropTypes from 'prop-types';

/**
 * Description of LoginForm
 */
class LoginForm extends Component {
    constructor(props) {
        super(props);

        this.state = {
            linkLoaded: false,
            initializeURL: 'https://cdn.plaid.com/link/v2/stable/link-initialize.js',
        };

        this.onScriptError = this.onScriptError.bind(this);
        this.onScriptLoaded = this.onScriptLoaded.bind(this);

        this.handleLinkOnLoad = this.handleLinkOnLoad.bind(this);

        this.handleOnExit = this.handleOnExit.bind(this);
        this.handleOnEvent = this.handleOnEvent.bind(this);
        this.handleOnSuccess = this.handleOnSuccess.bind(this);
    }

    onScriptError() {
        console.error('There was an issue loading the link-initialize.js script');
    }

    onScriptLoaded() {
        window.linkHandler = window.Plaid.create({
            apiVersion: this.props.apiVersion,
            clientName: this.props.clientName,
            env: this.props.env,
            key: this.props.publicKey,
            onExit: this.handleOnExit,
            onLoad: this.handleLinkOnLoad,
            onEvent: this.handleOnEvent,
            onSuccess: this.handleOnSuccess,
            product: this.props.product,
            selectAccount: this.props.selectAccount,
            token: this.props.token,
            webhook: this.props.webhook,
        });
        const institution = this.props.institution || null;
        window.linkHandler.open(institution);
    }

    handleLinkOnLoad() {
        console.log("loaded");
        this.setState({ linkLoaded: true });
    }
    handleOnSuccess(token, metadata) {
        console.log(token);
        console.log(metadata);
        this.props.setProps({public_token: token})
    }
    handleOnExit(error, metadata) {
        console.log('PlaidLink: user exited');
        console.log(error, metadata);
    }
    handleOnLoad() {
        console.log('PlaidLink: loaded');
    }
    handleOnEvent(eventname, metadata) {
        console.log('PlaidLink: user event', eventname, metadata);
    }

    static exit(configurationObject) {
        if (window.linkHandler) {
            window.linkHandler.exit(configurationObject);
        }
    }

    render() {
        return (
            <div id={this.props.id}
            >
                <Script
                    url={this.state.initializeURL}
                    onError={this.onScriptError}
                    onLoad={this.onScriptLoaded}
                />
            </div>
        );
    }
}

LoginForm.defaultProps = {
    apiVersion: 'v2',
    institution: null,
    selectAccount: false,
};

LoginForm.propTypes = {
    /**
     * id
     */
    id: PropTypes.string,

    /**
     * ApiVersion flag to use new version of Plaid API
     */
    apiVersion: PropTypes.string,

    /**
     * Displayed once a user has successfully linked their account
     */
    clientName: PropTypes.string.isRequired,

    /**
     * The Plaid API environment on which to create user accounts.
     * For development and testing, use tartan. For production, use production
     */
    env: PropTypes.oneOf(['tartan', 'sandbox', 'development', 'production']).isRequired,

    /**
     * Open link to a specific institution, for a more custom solution
     */
    institution: PropTypes.string,

    /**
     * The public_key associated with your account; available from
     * the Plaid dashboard (https://dashboard.plaid.com)
     */
    publicKey: PropTypes.string.isRequired,

    /**
     * The Plaid products you wish to use, an array containing some of connect,
     * auth, identity, income, transactions, assets
     */
    product: PropTypes.arrayOf(
        PropTypes.oneOf([
            // legacy product names
            'connect',
            'info',
            // normal product names
            'auth',
            'identity',
            'income',
            'transactions',
            'assets',
        ])
    ).isRequired,

    /**
     * Specify an existing user's public token to launch Link in update mode.
     * This will cause Link to open directly to the authentication step for
     * that user's institution.
     */
    token: PropTypes.string,

    /**
     * This is the token that will be returned for use in Dash. Can also be
     * understood as the "output" of this component
     */
    public_token: PropTypes.string,

    /**
     * Set to true to launch Link with the 'Select Account' pane enabled.
     * Allows users to select an individual account once they've authenticated
     */
    selectAccount: PropTypes.bool,

    /**
     * Specify a webhook to associate with a user.
     */
    webhook: PropTypes.string,

    /**
     * A function that is called when a user has successfully onboarded their
     * account. The function should expect two arguments, the public_key and a
     * metadata object
     */
    onSuccess: PropTypes.func,

    /**
     * A function that is called when a user has specifically exited Link flow
     */
    onExit: PropTypes.func,

    /**
     * A function that is called when the Link module has finished loading.
     * Calls to plaidLinkHandler.open() prior to the onLoad callback will be
     * delayed until the module is fully loaded.
     */
    onLoad: PropTypes.func,

    /**
     * A function that is called during a user's flow in Link.
     */
    onEvent: PropTypes.func,

    /**
     * Dash-assigned callback that should be called whenever any of the
     * properties change
     */
    setProps: PropTypes.func
};

export default LoginForm;
