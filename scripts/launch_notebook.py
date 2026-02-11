#!/usr/bin/env python3
"""Launch a Marimo notebook session via E2B sandbox."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "e2b", "src"))


if __name__ == "__main__":
    notebook_id = sys.argv[1] if len(sys.argv) > 1 else "test-notebook-001"
    user_id = sys.argv[2] if len(sys.argv) > 2 else "default"

    print(f"Launching notebook: {notebook_id} for user: {user_id}")

    import asyncio
    from manimo_e2b.sandbox import launch_notebook

    result = asyncio.run(launch_notebook(notebook_id, user_id))
    print(f"\nNotebook URL: {result.get('url', 'N/A')}")
    print(f"Sandbox ID: {result.get('sandbox_id', 'N/A')}")
