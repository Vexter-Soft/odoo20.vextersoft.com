# Dependency Map

```mermaid
graph TD
    User["End User / Browser"] -->|"HTTPS / 443"| CF["Cloudflare Edge Network"]
    CF -->|"Tunnel Protocol (QUIC)"| CFTunnel["Cloudflare Tunnel Daemon<br/>(vextersoft-tunnel)"]
    
    subgraph Host["Host Docker Engine"]
        subgraph EgressNet["Network: vextersoft-tunnel-egress (External)"]
            CFTunnel -->|"HTTP / 8069"| OdooWeb["odoo20-web<br/>(odoo:20.0)"]
        end

        subgraph PrivateNet["Network: odoo20-private (Internal)"]
            OdooWeb -->|"PostgreSQL / 5432"| OdooDB["odoo20-db<br/>(postgres:16-alpine)"]
        end

        subgraph Storage["Persistent Storage Volumes"]
            OdooDB --- VolDB[("odoo20-db-data<br/>/var/lib/postgresql/data")]
            OdooWeb --- VolWeb[("odoo20-web-data<br/>/var/lib/odoo")]
        end
    end
```

### Component Dependencies
1. **`CFTunnel` depends on Cloudflare Edge**: Establishes outbound persistent tunnel connection to Cloudflare PoPs.
2. **`odoo20-web` depends on `odoo20-db`**: Strictly sequenced with `service_healthy` condition on `pg_isready`.
3. **`odoo20-web` depends on `vextersoft-tunnel-egress`**: Network must be created beforehand on the host Docker engine (`docker network create vextersoft-tunnel-egress`).
