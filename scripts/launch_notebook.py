#!/usr/bin/env python3
"""Launch a Marimo notebook session via Modal."""

import sys
import subprocess
import json

if __name__ == "__main__":
    notebook_id = sys.argv[1] if len(sys.argv) > 1 else "test-notebook-001"
    user_id = sys.argv[2] if len(sys.argv) > 2 else "default"
    
    print(f"Launching notebook: {notebook_id} for user: {user_id}")
    
    # Use modal run and capture output
    result = subprocess.run(
        [
            "modal", "run",
            "modal/src/manimo_modal/app.py::launch_marimo_session",
            "--notebook-id", notebook_id,
            "--user-id", user_id
        ],
        capture_output=True,
        text=True,
        cwd="/Users/explorer/Manimo"
    )
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr, file=sys.stderr)
    
    # The URL should be in the output or we need to check Modal dashboard
    print(f"\n✅ Check the Modal dashboard for the sandbox URL:")
    print(f"https://modal.com/apps/autodidact24/main/deployed/manimo-notebooks")

