from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import logging
from datetime import datetime, timezone

# Load environment variables
load_dotenv()

# Import models and routes
from models import db, Contract
from routes.contracts import contracts_bp
from routes.deploy import deploy_bp

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Set up database path - use relative path for simplicity
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///contracts.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Configure CORS
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    CORS(app, origins=[frontend_url])
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s'
    )
    
    # Register blueprints
    app.register_blueprint(contracts_bp, url_prefix='/api')
    app.register_blueprint(deploy_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        # Create all tables (SQLite will create the file automatically)
        db.create_all()
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'version': '1.0.0'
        })
    
    # API info endpoint
    @app.route('/api')
    def api_info():
        return jsonify({
            'name': 'Multi-Jurisdictional Smart Contract Generator API',
            'version': '1.0.0',
            'description': 'Backend API for generating jurisdiction-specific smart contracts',
            'endpoints': {
                'contracts': {
                    'POST /api/generate': 'Generate new smart contract',
                    'GET /api/contracts': 'List all contracts',
                    'GET /api/contracts/<id>': 'Get specific contract',
                    'PUT /api/contracts/<id>/status': 'Update contract status',
                    'POST /api/validate': 'Validate contract request'
                },
                'deployment': {
                    'POST /api/deploy/<id>': 'Prepare contract deployment',
                    'POST /api/deploy/<id>/confirm': 'Confirm deployment',
                    'GET /api/deploy/<id>/bytecode': 'Get contract bytecode',
                    'POST /api/deploy/estimate-gas': 'Estimate deployment gas'
                }
            },
            'supported_jurisdictions': ['india', 'eu', 'us'],
            'supported_contract_types': ['escrow', 'insurance', 'settlement']
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400
    
    return app

# Create Flask app
app = create_app()

if __name__ == '__main__':
    # Check for required environment variables
    required_env_vars = ['GEMINI_API_KEY', 'SECRET_KEY', 'DATABASE_URL', 'FRONTEND_URL']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("Please create a .env file based on .env.example")
    
    # Run the application
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=debug_mode
    )
