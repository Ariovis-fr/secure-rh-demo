package com.example.keycloak;

import org.keycloak.authentication.AuthenticationFlowContext;
import org.keycloak.authentication.Authenticator;
import org.keycloak.models.UserModel;
import org.keycloak.models.KeycloakSession;
import org.keycloak.models.RealmModel;
import org.jboss.logging.Logger;

public class DefaultThemeAuthenticator implements Authenticator {

    private static final Logger logger = Logger.getLogger(DefaultThemeAuthenticator.class);

    @Override
    public void authenticate(AuthenticationFlowContext context) {
        // Log the start of the authentication flow
        logger.info("start flow defaultThemeAuthenticator");
        // Explicitly set the theme to default
        context.getRealm().setLoginTheme("attributes");
        context.success();
    }

    @Override
    public void action(AuthenticationFlowContext context) {
        // Not required in this case, as we're only modifying the theme during the authentication process
    }

    @Override
    public boolean requiresUser() {
        return false;
    }

    @Override
    public boolean configuredFor(KeycloakSession session, RealmModel realm, UserModel user) {
        return true;  // Always configured for any user
    }

    @Override
    public void setRequiredActions(KeycloakSession session, RealmModel realm, UserModel user) {
        // No specific actions are required
    }

    @Override
    public void close() {
        // Close any resources if needed
    }
}