FROM quay.io/phasetwo/phasetwo-keycloak:26.0.7

# Add any customizations or configurations here, for example:
# Copy custom scripts, configuration files, or plugins
# COPY ./custom-config /opt/keycloak/config/

# Change to root user to install additional packages
USER root

# Add realm configuration with bash script
COPY ./realm-config /realm-config
COPY ./import-realm.sh /opt/keycloak/bin/
RUN chmod +x /opt/keycloak/bin/import-realm.sh
RUN bash /opt/keycloak/bin/import-realm.sh /realm-config/realm.json /opt/keycloak/data/import/realm.json

# Add custom authentificator 
COPY themeOrgAuthentificator/build/libs/themeOrgAuthentificator.jar /opt/keycloak/providers/

# Expose any additional ports if needed
EXPOSE 8080