#!/usr/bin/env python3
"""
Simple startup script for the Smart Contract Generator backend
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ required")
        return False
    else:
        print(f"✅ Python {sys.version.split()[0]}")
    
    # Check Gemini API key
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ GEMINI_API_KEY not found in environment")
        print("   Please add your Gemini API key to the .env file")
        return False
    else:
        print("✅ Gemini API key configured")
    
    # Check required packages
    try:
        import flask
        import flask_cors
        import flask_sqlalchemy
        import google.generativeai
        import yaml
        print("✅ All required packages installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🚀 Smart Contract Generator Backend")
    print("=" * 40)
    
    if not check_requirements():
        print("\n❌ Requirements check failed. Please fix the issues above.")
        sys.exit(1)
    
    print("\n✅ All requirements met. Starting server...")
    print("📡 Server will be available at: http://localhost:5000")
    print("📖 API documentation: http://localhost:5000/api")
    print("💚 Health check: http://localhost:5000/health")
    print("\n🔧 To test the API, run: python test_api.py")
    print("🌐 Frontend should connect to: http://localhost:5000")
    print("\n" + "=" * 40)
    
    # Import and run the Flask app
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    main()
