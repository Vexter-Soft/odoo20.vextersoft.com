# System Architecture: Odoo 20 Demo Deployment (odoo20.vextersoft.com)

## 1. High-Level Overview
`odoo20.vextersoft.com` is a containerized, production-grade deployment of **Odoo 20.0** configured for internal demonstration, capability benchmarking, and module testing within VexterSoft.

The deployment provides zero-trust public access via a Cloudflare Tunnel, eliminating exposed public host ports while ensuring end-to-end SSL/TLS termination, edge caching, and DDoS mitigation. In addition, a local development environment (`docker-compose.yml`) mirrors production configurations with exposed local port `8020` for pre-deployment validation.

---

## 2. Infrastructure Topography & Networking

```
+-------------------------------------------------------------+
|                      Internet User                          |
+-------------------------------------------------------------+
                              |
                              | HTTPS (Port 443)
                              v
+-------------------------------------------------------------+
|               Cloudflare Edge Network                       |
|           (SSL Termination, DDoS, Edge Cache)               |
+-------------------------------------------------------------+
                              |
                              | Encrypted Tunnel (QUIC/TLS)
                              v
+-------------------------------------------------------------+
|                 Cloudflare Tunnel Ingress                   |
|                   (vextersoft-tunnel)                       |
+-------------------------------------------------------------+
                              |
          [vextersoft-tunnel-egress Network]
                              |
                              v
+-------------------------------------------------------------+
|               Odoo 20 Web Container                         |
|             (odoo20-web | odoo:20.0)                        |
|                    Port 8069                                |
|  - Extra Addons: /mnt/extra-addons/stratos_crm_rfp          |
|  - Extra Addons: /mnt/extra-addons/stratos_social           |
+-------------------------------------------------------------+
                              |
               [odoo20-private Network] (Internal only)
                              |
                              v
+-------------------------------------------------------------+
|             PostgreSQL 16 Database                          |
|         (odoo20-db | postgres:16-alpine)                    |
|                    Port 5432                                |
+-------------------------------------------------------------+
```

---

## 3. Core Software Stack & Addons

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Application Layer** | Odoo Community / Enterprise Base | `20.0-20261102` | Core ERP & business application platform |
| **Database Layer** | PostgreSQL | `16-alpine` | Relational data persistence & transactional integrity |
| **Custom Addon 1** | `stratos_crm_rfp` | `20.0.1.1.0` | International RFP tracking, deadline crons, and RFP dashboards |
| **Custom Addon 2** | `stratos_social` | `20.0.1.2.0` | Stratos Social Marketing for Meta, YouTube, and TikTok posting |
| **Ingress & Egress** | Cloudflare Tunnel (`cloudflared`) | Latest | Secure reverse proxy without open inbound firewall ports |
| **Stack Management** | Portainer (Git Repository Stack) | Latest | Continuous deployment via GitHub pull-and-redeploy (no SSH needed) |
| **Local Proxy** | Direct host bind | Port `8020` | Local developer inspection and sanity testing |

---

## 4. Custom Addons Architecture & Mounting Invariants

### Directory Hierarchy & Mounting Pattern
Source code for custom addons is maintained in the version-tagged directory tree:
- `addons/stratos_crm_rfp_20.0.1.1.0/stratos_crm_rfp`
- `addons/stratos_social_20.0.1.2.0/stratos_social`

**Container Invariant**:
Odoo's `/etc/odoo/odoo.conf` specifies `addons_path = /mnt/extra-addons`. To avoid breaking Odoo's module discovery (which expects `__manifest__.py` directly in immediate subfolders of the addons path), each module is individually bind-mounted:
```yaml
volumes:
  - ./addons/stratos_crm_rfp_20.0.1.1.0/stratos_crm_rfp:/mnt/extra-addons/stratos_crm_rfp
  - ./addons/stratos_social_20.0.1.2.0/stratos_social:/mnt/extra-addons/stratos_social
```

### Module Specifications
1. **`stratos_crm_rfp`**:
   - Technical name: `stratos_crm_rfp`
   - Dependencies: `crm`
   - Assets: Backend dashboard bundle (`web.assets_backend`) with custom OWL JS widget, XML template, and SCSS.
   - Automation: Automated reminder crons (`ir_cron_data.xml`) for submission deadlines.
2. **`stratos_social`**:
   - Technical name: `stratos_social`
   - Dependencies: `base_setup`, `mail`, `utm`
   - Python Dependencies: `requests >= 2.31.0`
   - Security: Multi-level security access groups (`User`, `Manager`) defined in `stratos_social_security.xml` and `ir.access.csv`.
   - Channels: Meta Graph API (Facebook/Instagram), Google YouTube v3 Data API, TikTok Content Posting API.

---

## 5. Network Isolation & Security Architecture

### Zero Public Inbound Ports on Production
- In production (`docker-compose-prod.yaml`), no host ports are bound.
- Ingress is mediated exclusively through the Docker bridge network `vextersoft-tunnel-egress`.

### Multi-Tier Network Segmentation
1. **`vextersoft-tunnel-egress` (External Bridge)**:
   - Shared exclusively with the Cloudflare Tunnel agent.
   - Only `odoo20-web` is joined to this network; the database is completely isolated.
2. **`odoo20-private` (Internal Bridge, `internal: true`)**:
   - Strictly isolated between `odoo20-web` and `odoo20-db`.

---

## 6. Storage & Persistence Invariants

1. **Database Data Volume (`odoo20-db-data` / `odoo20-local-db-data`)**:
   - Mount: `/var/lib/postgresql/data`
   - Invariant: Persists PostgreSQL tables, indexes, and write-ahead logs (WAL).
2. **Filestore Volume (`odoo20-web-data` / `odoo20-local-web-data`)**:
   - Mount: `/var/lib/odoo`
   - Invariant: Contains Odoo filestore (`/var/lib/odoo/filestore`), attachments, and session stores.
