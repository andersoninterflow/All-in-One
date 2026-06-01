from __future__ import annotations

import argparse
import json
import sys

from scripts.stitch_orchestrator import load_state, sync_projects, sync_summary, write_manifest
from scripts.validate_stitch_mcp_config import validate_stitch_mcp_config


def main() -> int:
    parser = argparse.ArgumentParser(description="Executa plano, validacao e sincronizacao remota do Stitch.")
    parser.add_argument("--require-remote", action="store_true", help="Falha quando STITCH_API_KEY nao estiver presente.")
    parser.add_argument("--dry-run", action="store_true", help="Valida e mostra o status sem chamar o MCP remoto.")
    args = parser.parse_args()

    manifest = write_manifest()
    errors = validate_stitch_mcp_config(require_secret=args.require_remote)
    if errors:
        print("\nFalhas de validacao do sync Stitch:")
        for error in errors:
            print(f"- {error}")
        return 1

    if not args.dry_run:
        state = sync_projects(manifest)
    else:
        state = load_state()

    summary = sync_summary(manifest, state)
    print(json.dumps(summary, indent=2, ensure_ascii=True))
    if args.require_remote and (
        summary["synced_projects"] != summary["expected_projects"]
        or summary["synced_screens"] != summary["expected_screens"]
    ):
        print("\nSincronizacao Stitch remota incompleta.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
