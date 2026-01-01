#!/usr/bin/env python3
"""Get the notebook URL from a launched session."""

import modal
import sys

if __name__ == "__main__":
    notebook_id = sys.argv[1] if len(sys.argv) > 1 else "test-notebook-001"
    user_id = sys.argv[2] if len(sys.argv) > 2 else "default"
    
    print(f"Launching notebook: {notebook_id} for user: {user_id}")
    
    # Import the app
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "manimo_modal.app",
        "/Users/explorer/Manimo/modal/src/manimo_modal/app.py"
    )
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    
    app = app_module.app
    
    # Call the function
    with app.run():
        result = app.launch_marimo_session.remote(notebook_id, user_id)
        print(f"\n✅ Notebook launched!")
        print(f"📓 Notebook ID: {result['notebook_id']}")
        print(f"🌐 URL: {result['url']}")
        print(f"📊 Status: {result['status']}")
        print(f"\n🔗 Open this URL in your browser to access the notebook:")
        print(f"   {result['url']}")

