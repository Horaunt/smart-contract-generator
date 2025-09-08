from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Contract(db.Model):
    __tablename__ = 'contracts'
    
    id = db.Column(db.Integer, primary_key=True)
    jurisdiction = db.Column(db.String(50), nullable=False)
    contract_type = db.Column(db.String(50), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    payee_address = db.Column(db.String(42))  # Ethereum address length
    payer_address = db.Column(db.String(42))
    solidity_code = db.Column(db.Text)
    deploy_script = db.Column(db.Text)
    tests = db.Column(db.Text)
    contract_metadata = db.Column(db.Text)  # JSON string for additional data
    status = db.Column(db.String(20), default='draft')  # draft, deployed, failed
    transaction_hash = db.Column(db.String(66))  # Ethereum tx hash
    contract_address = db.Column(db.String(42))  # Deployed contract address
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert contract to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'jurisdiction': self.jurisdiction,
            'contract_type': self.contract_type,
            'requirements': self.requirements,
            'description': self.description,
            'payee_address': self.payee_address,
            'payer_address': self.payer_address,
            'solidity_code': self.solidity_code,
            'deploy_script': self.deploy_script,
            'tests': self.tests,
            'metadata': json.loads(self.contract_metadata) if self.contract_metadata else {},
            'status': self.status,
            'transaction_hash': self.transaction_hash,
            'contract_address': self.contract_address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_summary_dict(self):
        """Convert contract to summary dictionary for listing"""
        return {
            'id': self.id,
            'jurisdiction': self.jurisdiction,
            'contract_type': self.contract_type,
            'description': self.description,
            'status': self.status,
            'contract_address': self.contract_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Contract {self.id}: {self.contract_type} ({self.jurisdiction})>'
