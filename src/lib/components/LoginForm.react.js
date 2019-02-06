import React, {Component} from 'react';
import PropTypes from 'prop-types';
import PlaidAuthenticator from '../private/PlaidAuthenticator.js'

export default class LoginForm extends Component {
    render() {
        const {id, environment, public_key, products} = this.props;

        return (
                <PlaidAuthenticator
                    id={id}
                    onMessage={this.onMessage}
                    publicKey={public_key}
                    env={environment}
                    product={products}
                    clientName="Butters"
                    selectAccount={false}
                />);
    }
}

LoginForm.defaultProps = {};

LoginForm.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks
     */
    id: PropTypes.string,

    /**
     * The ID used to identify this component in Dash callbacks
     */
    data: PropTypes.string,

    /**
     * Dash-assigned callback that should be called whenever any of the
     * properties change
     */
    setProps: PropTypes.func,

    /**
     *
     */
    environment: PropTypes.string.isRequired,

    /**
     *
     */
    public_key: PropTypes.string.isRequired,

    /**
     *
     */
    products: PropTypes.string
};