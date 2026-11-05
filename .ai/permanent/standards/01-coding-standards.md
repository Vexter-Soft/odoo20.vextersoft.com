# Operational & Deployment Standards: Odoo 20

## 1. Container Configuration Standards
1. **Pinned Tags**: Base images must always specify explicit major/minor releases (e.g. `odoo:20.0`, `postgres:16-alpine`), never generic `latest`.
2. **Explicit Healthchecks**: State-dependent backend services (such as PostgreSQL) must implement active Docker healthchecks before downstream dependents (`odoo20-web`) start.
3. **Graceful Restart**: All continuous services must specify `restart: unless-stopped`.

---

## 2. Security & Network Invariants
1. **No Unnecessary Port Bindings**:
   - Web application traffic must route exclusively through internal or egress bridge networks to the tunnel daemon.
   - Database ports (`5432`) must never be mapped to host ports or attached to egress networks.
2. **Mandatory Environment Variable Interpolation**:
   - Sensitive credentials like `POSTGRES_PASSWORD` must use required shell/compose expansion (`${VARIABLE:?Error message}`) to prevent containers from booting with blank or default passwords.
3. **TLS & Edge Headers**:
   - The Cloudflare Tunnel terminates SSL. If proxy headers are required by Odoo, configure `proxy_mode = True` in `/etc/odoo/odoo.conf` or pass appropriate command arguments (`--proxy-mode`).

---

## 3. Data Integrity & Volume Lifecycle
1. **Named Volumes**: All container storage layers holding persistent state (database records, uploaded files, attachments, sessions) must reside on named Docker volumes.
2. **Backup Invariant**: Before database updates, module upgrades, or migration tests, perform a consistent snapshot:
   - PostgreSQL dump via `docker exec odoo20-db pg_dump -U odoo postgres > backup.sql`.
   - Filestore archive from `/var/lib/odoo/filestore`.

---

## 4. Odoo 20 Module & Customization Rules
1. **Module Manifests**: Any custom modules developed for this instance must specify `"version": "20.0.1.0.0"`.
2. **ORM Compatibility**: Respect Odoo 20 API patterns (Python 3.12+, new OWL frontend components, updated web client layouts).
