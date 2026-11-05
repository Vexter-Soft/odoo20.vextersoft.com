#!/usr/bin/env python3
"""
Odoo Query CLI Tool for odoo20.vextersoft.com
Connects via Odoo XML-RPC API to inspect version, modules, models, and records.
"""

import argparse
import os
import sys
import xmlrpc.client
from pprint import pprint


class OdooAPI:
    def __init__(self, url, db, username, password):
        self.url = url.rstrip("/")
        self.db = db
        self.username = username
        self.password = password
        self.common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common", allow_none=True)
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object", allow_none=True)
        self.uid = None

    def authenticate(self):
        if not self.uid:
            try:
                self.uid = self.common.authenticate(self.db, self.username, self.password, {})
            except Exception as e:
                print(f"[ERROR] Authentication failed: {e}", file=sys.stderr)
                return None
        return self.uid

    def get_version(self):
        return self.common.version()

    def list_modules(self, state=None, search=None, custom_only=False):
        uid = self.authenticate()
        if not uid:
            print("[ERROR] Could not authenticate. Provide valid credentials (--user, --password).", file=sys.stderr)
            return []

        domain = []
        if state:
            domain.append(("state", "=", state))
        if search:
            domain.append("|")
            domain.append(("name", "ilike", search))
            domain.append(("shortdesc", "ilike", search))
        if custom_only:
            domain.append(("name", "ilike", "stratos"))

        fields = ["name", "shortdesc", "state", "application", "author", "installed_version"]
        return self.models.execute_kw(
            self.db, uid, self.password,
            "ir.module.module", "search_read",
            [domain],
            {"fields": fields, "order": "application desc, name asc"}
        )

    def update_module_list(self):
        uid = self.authenticate()
        if not uid:
            print("[ERROR] Could not authenticate.", file=sys.stderr)
            return None
        return self.models.execute_kw(
            self.db, uid, self.password,
            "ir.module.module", "update_list",
            []
        )


def main():
    parser = argparse.ArgumentParser(description="Query Odoo 20 deployment via XML-RPC")
    parser.add_argument("--url", default=os.getenv("ODOO_URL", "https://odoo20.vextersoft.com"), help="Odoo server URL")
    parser.add_argument("--db", default=os.getenv("ODOO_DB", "odoo20"), help="Database name")
    parser.add_argument("--user", default=os.getenv("ODOO_USER", "admin"), help="Odoo login")
    parser.add_argument("--password", default=os.getenv("ODOO_PASSWORD", ""), help="Odoo password or API key")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Version command
    subparsers.add_parser("version", help="Print Odoo server version")

    # Modules command
    mod_parser = subparsers.add_parser("modules", help="List modules from ir.module.module")
    mod_parser.add_argument("--search", help="Filter by name or shortdesc")
    mod_parser.add_argument("--state", choices=["installed", "uninstalled", "to upgrade", "to install"], help="Filter by state")
    mod_parser.add_argument("--stratos-only", action="store_true", help="Only list Stratos custom modules")

    # Update list command
    subparsers.add_parser("update-list", help="Trigger update_list (Update Apps List)")

    args = parser.parse_args()
    api = OdooAPI(args.url, args.db, args.user, args.password)

    if args.command == "version":
        ver = api.get_version()
        print("Connected to:", args.url)
        print("Server Version:", ver.get("server_version"))
        pprint(ver)

    elif args.command == "modules":
        modules = api.list_modules(state=args.state, search=args.search, custom_only=args.stratos_only)
        if not modules:
            print("No modules found matching query.")
            return
        print(f"\nFound {len(modules)} module(s):")
        print(f"{'Technical Name':<25} {'State':<14} {'App?':<6} {'Name':<35} {'Version'}")
        print("-" * 95)
        for m in modules:
            app_flag = "Yes" if m.get("application") else "No"
            print(f"{m.get('name'):<25} {m.get('state'):<14} {app_flag:<6} {m.get('shortdesc', '')[:33]:<35} {m.get('installed_version', '-')}")

    elif args.command == "update-list":
        result = api.update_module_list()
        print("Update modules list result:", result)


if __name__ == "__main__":
    main()
