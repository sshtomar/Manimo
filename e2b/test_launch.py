#!/usr/bin/env python3
"""E2B Notebook Launcher Test.

Tests the E2B sandbox launch functionality.

Usage:
    # Set environment variables
    export E2B_API_KEY=e2b_xxx
    export R2_ENDPOINT=https://xxx.r2.cloudflarestorage.com
    export R2_ACCESS_KEY_ID=xxx
    export R2_SECRET_ACCESS_KEY=xxx
    export ANTHROPIC_API_KEY=sk-ant-xxx

    # Run test
    python test_launch.py
"""

import os
import sys
import time

# Add src to path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def check_environment():
    """Check required environment variables."""
    required = [
        "E2B_API_KEY",
        "R2_ENDPOINT",
        "R2_ACCESS_KEY_ID",
        "R2_SECRET_ACCESS_KEY",
    ]

    missing = [var for var in required if not os.environ.get(var)]
    if missing:
        print("Missing required environment variables:")
        for var in missing:
            print(f"  - {var}")
        print("\nSet these before running the test.")
        sys.exit(1)


def test_notebook_launch():
    """Test spawning a notebook sandbox."""
    from manimo_e2b.sandbox import spawn_notebook_sandbox, check_sandbox_status

    print("E2B Notebook Launcher Test")
    print("=" * 40)
    print()

    # Generate a test notebook ID
    test_id = f"test-{int(time.time())}"
    user_id = "test-user"

    print(f"1. Spawning sandbox for: {user_id}/{test_id}/notebook.py")

    start = time.time()
    result = spawn_notebook_sandbox(
        notebook_id=test_id,
        user_id=user_id,
    )
    elapsed = time.time() - start

    print(f"\n   Result:")
    print(f"   - Sandbox ID: {result['sandbox_id']}")
    print(f"   - Marimo URL: {result['marimo_url']}")
    print(f"   - Status: {result['status']}")
    print(f"   - Time: {elapsed:.1f}s")

    print()
    print(f"2. Checking sandbox status...")
    status = check_sandbox_status(result["sandbox_id"])
    print(f"   Status: {status['status']}")
    print(f"   Active: {status['active']}")

    print()
    print("=" * 40)
    print("Test completed!")
    print()
    print(f"Open Marimo at: {result['marimo_url']}")
    print()
    print("Note: The sandbox will auto-terminate after 30 minutes of inactivity.")

    return result


def test_render_video():
    """Test video rendering (optional - requires existing notebook with Scene)."""
    print("\nVideo rendering test skipped (requires notebook with Manim Scene)")


if __name__ == "__main__":
    check_environment()

    try:
        test_notebook_launch()
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
