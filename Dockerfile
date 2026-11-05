FROM odoo:20.0

USER root

# Copy custom Stratos addons into standard extra-addons directory
COPY ./addons/stratos_crm_rfp_20.0.1.1.0/stratos_crm_rfp /mnt/extra-addons/stratos_crm_rfp
COPY ./addons/stratos_social_20.0.1.2.0/stratos_social /mnt/extra-addons/stratos_social

# Ensure odoo user has ownership
RUN chown -R odoo:odoo /mnt/extra-addons

USER odoo
