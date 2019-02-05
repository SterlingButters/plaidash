import React, {Component} from 'react';
import PropTypes from 'prop-types';
import PlaidAuthenticator from 'react-native-plaid-link/index.js';

export default class LoginForm extends Component {
    render() {
        const {id, data, environment, public_key, products} = this.props;

        return (
            <div id={id}>
                <PlaidAuthenticator
                    onMessage={this.onMessage}
                    publicKey={public_key}
                    env={environment}
                    product={products}
                    clientName="Butters"
                    selectAccount={false}
                />

                onMessage = (data) => {
                this.setState({data})
                }
            </div>
        );
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
