#!/usr/bin/env python3
"""
E-commerce Sales Chatbot Backend Server
Run this script to start the Flask development server
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.absolute()
project_root = backend_dir.parent
sys.path.insert(0, str(backend_dir))

# Change to backend directory for relative imports
os.chdir(backend_dir)

# Import and run the Flask application
if __name__ == '__main__':
    from app import create_app
    
    print("🤖 Starting E-commerce Sales Chatbot Backend...")
    print("📁 Backend directory:", backend_dir)
    print("🌐 Server will be available at: http://localhost:5000")
    print("📖 API documentation available in docs/TECHNICAL_DOCUMENTATION.md")
    print("=" * 60)
    
    # Create Flask app
    app = create_app()
    
    # Run the development server
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
