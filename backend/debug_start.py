#!/usr/bin/env python3
"""
Debug startup script to identify and fix backend issues
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check current directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    # Check if we're in the backend directory
    if not current_dir.endswith('backend'):
        print("❌ Not in backend directory")
        return False
    
    # Check if required files exist
    required_files = ['app.py', 'models.py', 'requirements.txt']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing file: {file}")
            return False
        else:
            print(f"✅ Found: {file}")
    
    return True

def create_instance_directory():
    """Create instance directory for SQLite database"""
    print("\n📁 Creating instance directory...")
    
    instance_dir = Path('instance')
    instance_dir.mkdir(exist_ok=True)
    print(f"✅ Instance directory created: {instance_dir.absolute()}")
    
    # Test database path
    db_path = instance_dir / 'contracts.db'
    print(f"Database will be created at: {db_path.absolute()}")
    
    return True

def test_imports():
    """Test if all required modules can be imported"""
    print("\n📦 Testing imports...")
    
    try:
        import flask
        print(f"✅ Flask {flask.__version__}")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import flask_cors
        print("✅ Flask-CORS")
    except ImportError as e:
        print(f"❌ Flask-CORS import failed: {e}")
        return False
    
    try:
        import flask_sqlalchemy
        print("✅ Flask-SQLAlchemy")
    except ImportError as e:
        print(f"❌ Flask-SQLAlchemy import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    return True

def test_database_creation():
    """Test database creation"""
    print("\n🗄️ Testing database creation...")
    
    try:
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from models import db, Contract
        
        # Create test app
        app = Flask(__name__)
        
        # Configure database
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'contracts.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Initialize database
        db.init_app(app)
        
        with app.app_context():
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Test creating a contract
            test_contract = Contract(
                jurisdiction='india',
                contract_type='escrow',
                requirements='Test requirements',
                status='draft'
            )
            
            db.session.add(test_contract)
            db.session.commit()
            print("✅ Test contract created successfully")
            
            # Clean up test data
            db.session.delete(test_contract)
            db.session.commit()
            print("✅ Test data cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting Flask server...")
    
    try:
        from app import create_app
        
        app = create_app()
        print("✅ Flask app created successfully")
        
        print("🌐 Starting server on http://localhost:5000")
        print("📖 API docs: http://localhost:5000/api")
        print("💚 Health check: http://localhost:5000/health")
        print("\nPress Ctrl+C to stop the server")
        
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main debug function"""
    print("🔧 Smart Contract Generator Backend - Debug Mode")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed")
        return
    
    # Create directories
    if not create_instance_directory():
        print("\n❌ Directory creation failed")
        return
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed")
        print("Run: pip install -r requirements.txt")
        return
    
    # Test database
    if not test_database_creation():
        print("\n❌ Database test failed")
        return
    
    print("\n✅ All checks passed! Starting server...")
    print("=" * 50)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
