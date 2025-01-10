package com.example.keycloak;

import org.keycloak.authentication.Authenticator;
import org.keycloak.authentication.AuthenticatorFactory;
import org.keycloak.authentication.ConfigurableAuthenticatorFactory;
import org.keycloak.models.KeycloakSession;
import org.keycloak.models.KeycloakSessionFactory;
import org.keycloak.provider.ProviderConfigProperty;
import org.keycloak.models.AuthenticationExecutionModel;

import java.util.Collections;
import java.util.List;

public class DefaultThemeAuthenticatorFactory implements AuthenticatorFactory {

    public static final String PROVIDER_ID = "defaultThemeAuthenticator";  // Unique identifier for this authenticator

    @Override
    public Authenticator create(KeycloakSession session) {
        // Return a new instance of your DefaultThemeAuthenticator
        return new DefaultThemeAuthenticator();
    }

    @Override
    public void init(org.keycloak.Config.Scope config) {
        // Initialize if required, can be left empty if no configuration is needed
    }

    @Override
    public void postInit(KeycloakSessionFactory sessionFactory) {
        // Post-initialization tasks can be handled here, or left empty if not needed
    }

    @Override
    public String getId() {
        // The unique identifier for the authenticator
        return PROVIDER_ID;
    }

    @Override
    public String getDisplayType() {
        // Display name for the authenticator, shown in the Keycloak admin console
        return "Default Theme Switcher";
    }

    @Override
    public boolean isConfigurable() {
        // Whether the authenticator has configurable settings; false since we are not adding any custom configuration
        return false;
    }

    @Override
    public boolean isUserSetupAllowed() {
        // Whether users can configure this authenticator; false as this is a static setting for the flow
        return false;
    }

    @Override
    public AuthenticationExecutionModel.Requirement[] getRequirementChoices() {
        // Define the valid requirements for this authenticator
        return new AuthenticationExecutionModel.Requirement[] {
            AuthenticationExecutionModel.Requirement.REQUIRED,
            AuthenticationExecutionModel.Requirement.DISABLED
        };
    }

    @Override
    public void close() {
        // Close any resources if necessary, not needed in this case
    }

    @Override
    public String getReferenceCategory() {
        // Return null, as this doesn't belong to any specific category
        return null;
    }

    @Override
    public List<ProviderConfigProperty> getConfigProperties() {
        // Return null as no configuration properties are needed for this authenticator
        return null;
    }

    @Override
    public String getHelpText() {
        // Description of the authenticator, shown in the admin console for reference
        return "This authenticator sets the theme to the default theme during authentication.";
    }
}
