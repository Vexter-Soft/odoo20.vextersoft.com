# Project Glossary

## Core Terminology

- **Odoo 20 (`odoo:20.0`)**: The major 2026 release of the Odoo ERP platform, featuring updated OWL framework components, modernized web client interface, and performance optimizations.
- **Cloudflare Tunnel (`cloudflared`)**: An outbound-only daemon that connects local Docker network endpoints to the Cloudflare global network, providing ingress without public port forwarding or static public IPs.
- **`vextersoft-tunnel-egress`**: The designated external Docker bridge network facilitating connectivity between application containers and the host Cloudflare Tunnel connector.
- **`odoo20-private`**: An internal (`internal: true`) Docker network dedicated strictly to inter-container communication between the Odoo web service and the PostgreSQL database.
- **Filestore**: The filesystem directory (`/var/lib/odoo/filestore`) where binary attachments, media assets, documents, and report templates are persisted outside of the PostgreSQL database tables.
- **Internal Demo Instance**: A dedicated environment deployed at `https://odoo20.vextersoft.com` designed for stakeholder walkthroughs, module testing, and workflow validation prior to client-facing releases.
