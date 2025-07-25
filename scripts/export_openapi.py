#!/usr/bin/env python3
"""
Export OpenAPI specification to JSON file for documentation.
"""

import json
import sys
import os

# Add parent directory to path to import our app
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app

def export_openapi():
    """Export OpenAPI specification to JSON file."""
    try:
        # Get OpenAPI schema
        openapi_schema = app.openapi()
        
        # Create docs directory if it doesn't exist
        docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
        os.makedirs(docs_dir, exist_ok=True)
        
        # Write to JSON file
        output_file = os.path.join(docs_dir, 'openapi.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
        
        print(f"✅ OpenAPI specification exported to: {output_file}")
        print(f"📊 Found {len(openapi_schema.get('paths', {}))} endpoints")
        
        # Print some basic info
        info = openapi_schema.get('info', {})
        print(f"📝 API Title: {info.get('title', 'N/A')}")
        print(f"🔢 API Version: {info.get('version', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error exporting OpenAPI specification: {e}")
        return False

if __name__ == "__main__":
    success = export_openapi()
    sys.exit(0 if success else 1)
