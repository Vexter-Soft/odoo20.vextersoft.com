# Repository Map

## Project Root Directory (`e:\myapps\odoo20.vextersoft.com`)

- **`Dockerfile`**:
  - Image definition extending `odoo:20.0`. Copies `stratos_crm_rfp` and `stratos_social` into `/mnt/extra-addons` with `odoo:odoo` permissions, ensuring reliable Portainer Git Stack builds.

- **`docker-compose-prod.yml`**:
  - Declarative service definitions for the live production/demo stack on `odoo20.vextersoft.com`.
  - Configures `odoo20-db` (PostgreSQL 16 Alpine) and `odoo20-web` (built from `Dockerfile`).
  - Connects to `vextersoft-tunnel-egress` external network with no host ports exposed.

- **`docker-compose.yml`**:
  - Standalone local Docker development stack with exposed port `8020:8069`.
  - Used for local pre-deployment validation, addon unit testing, and UI sanity verification.

- **`.env.example`**:
  - Template environment file defining required secrets (`ODOO20_DB_PASSWORD`) and port overrides.

- **`.gitignore`**:
  - Excludes active `.env` secret files, Python caches, dumps, and OS logs.

- **`addons/`**:
  - **`stratos_crm_rfp_20.0.1.1.0/stratos_crm_rfp/`**:
    - `models/`: `crm_lead.py` (RFP fields, status logic, submission dates), `res_config_settings.py`.
    - `views/`: `crm_lead_views.xml` (RFP tab, kanban badges, filters), `res_config_settings_views.xml`.
    - `data/`: `rfp_data.xml`, `ir_cron_data.xml` (automated deadline activities).
    - `static/src/dashboard/`: Custom OWL JavaScript dashboard component, XML templates, and SCSS styling.
    - `tests/`: `test_rfp.py` (comprehensive flow, deadline, and activity tests).
  - **`stratos_social_20.0.1.2.0/stratos_social/`**:
    - `models/`: `social_account.py`, `social_post.py`, `social_live_post.py`, `meta_api.py`, `google_api.py`, `tiktok_api.py`.
    - `controllers/`: OAuth authentication callbacks for Meta, Google, and TikTok.
    - `wizard/`: `social_token_wizard.py` for direct access token input.
    - `views/`: Social account, post, settings, and menu views.
    - `security/`: `stratos_social_security.xml`, `ir.access.csv`.
    - `tests/`: `test_social_post.py`, `test_tiktok.py`, `test_youtube.py`.

- **`.agents/`**:
  - `AGENTS.md`: Foundational AI instructions, defining the AI bootstrap read sequence and documentation ownership rules.

- **`.ai/`**:
  - Canonical knowledge base preserving architectural intent, repository indexing, operational standards, and transient sprint states.
  - **`README.md`**: Master index and AI bootstrap sequence.
  - **`permanent/`**:
    - `architecture/01-system-architecture.md`: System topography, addon mounting model, network isolation, persistence, and health checks.
    - `standards/01-coding-standards.md`: Operational, container, and configuration standards.
    - `glossary/01-terms.md`: Core terminology and architectural concepts.
  - **`indexes/`**:
    - `repository.md`: This file; structural map of code and configuration assets.
    - `dependency-map.md`: Mermaid relationship graph of infrastructure components.
  - **`transient/`**:
    - `sprint/00-current-state.md`: Live system status, active capabilities, endpoint health, and immediate objectives.
    - `handoffs/`: Chat session milestones and state transitions.
