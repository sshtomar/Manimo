#!/usr/bin/env python3
"""Build E2B template for Manimo notebooks.

Usage:
    E2B_API_KEY=e2b_xxx python build_template.py

This script builds and publishes the E2B template using the e2b CLI.
"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    # Check for E2B API key
    api_key = os.environ.get("E2B_API_KEY")
    if not api_key:
        print("Error: E2B_API_KEY environment variable not set")
        print("Get your API key from: https://e2b.dev/dashboard?tab=keys")
        sys.exit(1)

    template_dir = Path(__file__).parent
    template_name = "manimo-notebook"

    print(f"Building E2B template: {template_name}")
    print("=" * 50)

    # Run e2b template build
    try:
        result = subprocess.run(
            [
                "e2b", "template", "build",
                "--name", template_name,
                "--dockerfile", str(template_dir / "e2b.Dockerfile"),
                "--path", str(template_dir),
            ],
            env={**os.environ, "E2B_API_KEY": api_key},
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: e2b CLI not found")
        print("Install with: npm install -g @e2b/cli")
        sys.exit(1)

    print("=" * 50)
    print("Template built successfully!")
    print(f"Template name: {template_name}")
    print()
    print("Use in code:")
    print(f'  sandbox = Sandbox.create("{template_name}")')


if __name__ == "__main__":
    main()
