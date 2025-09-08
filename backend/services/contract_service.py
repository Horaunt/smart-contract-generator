import yaml
import os
from typing import Dict, Any, Optional
from .gemini_client import GeminiClient
from models import Contract, db
import json
import logging

logger = logging.getLogger(__name__)

class ContractService:
    def __init__(self):
        """Initialize contract service with legal rules"""
        self.gemini_client = GeminiClient()
        self.legal_rules = self._load_legal_rules()
    
    def _load_legal_rules(self) -> Dict[str, Any]:
        """Load legal rules from YAML file"""
        try:
            rules_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                'legal_rules', 
                'jurisdictions.yaml'
            )
            with open(rules_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Failed to load legal rules: {str(e)}")
            return {}
    
    def validate_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate contract generation request
        
        Args:
            payload: Request data
            
        Returns:
            Dict with validation results
        """
        errors = []
        warnings = []
        
        # Required fields validation
        required_fields = ['jurisdiction', 'contract_type', 'requirements']
        for field in required_fields:
            if not payload.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Jurisdiction validation
        jurisdiction = payload.get('jurisdiction', '').lower()
        valid_jurisdictions = list(self.legal_rules.get('jurisdictions', {}).keys())
        if jurisdiction and jurisdiction not in valid_jurisdictions:
            errors.append(f"Invalid jurisdiction. Valid options: {', '.join(valid_jurisdictions)}")
        
        # Contract type validation
        contract_type = payload.get('contract_type', '').lower()
        valid_types = list(self.legal_rules.get('contract_types', {}).keys())
        if contract_type and contract_type not in valid_types:
            errors.append(f"Invalid contract type. Valid options: {', '.join(valid_types)}")
        
        # Address validation (basic format check)
        for addr_field in ['payee_address', 'payer_address']:
            address = payload.get(addr_field)
            if address and not self._is_valid_ethereum_address(address):
                warnings.append(f"Invalid Ethereum address format for {addr_field}")
        
        # Jurisdiction-specific validation
        if jurisdiction in self.legal_rules.get('jurisdictions', {}):
            jurisdiction_rules = self.legal_rules['jurisdictions'][jurisdiction]
            required_fields = jurisdiction_rules.get('required_fields', [])
            
            for field in required_fields:
                if field not in payload or not payload[field]:
                    errors.append(f"Field '{field}' is required for {jurisdiction.upper()} jurisdiction")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def _is_valid_ethereum_address(self, address: str) -> bool:
        """Basic Ethereum address validation"""
        if not address:
            return False
        return (
            address.startswith('0x') and 
            len(address) == 42 and 
            all(c in '0123456789abcdefABCDEF' for c in address[2:])
        )
    
    def generate_contract(self, payload: Dict[str, Any]) -> Contract:
        """
        Generate a new smart contract
        
        Args:
            payload: Contract generation request data
            
        Returns:
            Contract: Generated contract instance
        """
        # Validate request
        validation = self.validate_request(payload)
        if not validation['valid']:
            raise ValueError(f"Validation failed: {', '.join(validation['errors'])}")
        
        try:
            # Generate contract using Gemini
            logger.info(f"Generating contract for {payload.get('jurisdiction')} - {payload.get('contract_type')}")
            result = self.gemini_client.generate_contract(payload, self.legal_rules)
            
            # Create contract instance
            contract = Contract(
                jurisdiction=payload.get('jurisdiction'),
                contract_type=payload.get('contract_type'),
                requirements=payload.get('requirements'),
                description=payload.get('description'),
                payee_address=payload.get('payee_address'),
                payer_address=payload.get('payer_address'),
                solidity_code=result['solidity_code'],
                deploy_script=result['deploy_script'],
                tests=result['tests'],
                contract_metadata=json.dumps(result['metadata']),
                status='draft'
            )
            
            # Save to database
            db.session.add(contract)
            db.session.commit()
            
            logger.info(f"Contract generated successfully with ID: {contract.id}")
            return contract
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Contract generation failed: {str(e)}")
            raise Exception(f"Failed to generate contract: {str(e)}")
    
    def get_contract(self, contract_id: int) -> Optional[Contract]:
        """Get contract by ID"""
        try:
            return Contract.query.get(contract_id)
        except Exception as e:
            logger.error(f"Error fetching contract {contract_id}: {str(e)}")
            return None
    
    def list_contracts(self, filters: Optional[Dict[str, Any]] = None) -> list:
        """
        List contracts with optional filters
        
        Args:
            filters: Optional filters (jurisdiction, contract_type, status)
            
        Returns:
            List of contracts
        """
        try:
            query = Contract.query
            
            if filters:
                if filters.get('jurisdiction'):
                    query = query.filter(Contract.jurisdiction == filters['jurisdiction'])
                if filters.get('contract_type'):
                    query = query.filter(Contract.contract_type == filters['contract_type'])
                if filters.get('status'):
                    query = query.filter(Contract.status == filters['status'])
            
            return query.order_by(Contract.created_at.desc()).all()
            
        except Exception as e:
            logger.error(f"Error listing contracts: {str(e)}")
            return []
    
    def update_contract_status(self, contract_id: int, status: str, 
                             transaction_hash: Optional[str] = None,
                             contract_address: Optional[str] = None) -> bool:
        """
        Update contract deployment status
        
        Args:
            contract_id: Contract ID
            status: New status (deployed, failed, etc.)
            transaction_hash: Transaction hash if deployed
            contract_address: Deployed contract address
            
        Returns:
            bool: Success status
        """
        try:
            contract = Contract.query.get(contract_id)
            if not contract:
                return False
            
            contract.status = status
            if transaction_hash:
                contract.transaction_hash = transaction_hash
            if contract_address:
                contract.contract_address = contract_address
            
            db.session.commit()
            logger.info(f"Contract {contract_id} status updated to {status}")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating contract status: {str(e)}")
            return False
    
    def get_deployment_data(self, contract_id: int) -> Optional[Dict[str, Any]]:
        """
        Get contract deployment data for MetaMask
        
        Args:
            contract_id: Contract ID
            
        Returns:
            Dict with deployment data or None
        """
        try:
            contract = self.get_contract(contract_id)
            if not contract:
                return None
            
            # Parse metadata
            metadata = json.loads(contract.contract_metadata) if contract.contract_metadata else {}
            
            # Extract constructor parameters from addresses
            constructor_params = []
            if contract.payee_address:
                constructor_params.append(contract.payee_address)
            if contract.payer_address:
                constructor_params.append(contract.payer_address)
            
            return {
                'contract_id': contract.id,
                'solidity_code': contract.solidity_code,
                'deploy_script': contract.deploy_script,
                'constructor_params': constructor_params,
                'metadata': metadata,
                'estimated_gas': 2000000,  # Default gas estimate
                'contract_name': metadata.get('contract_name', 'GeneratedContract')
            }
            
        except Exception as e:
            logger.error(f"Error getting deployment data: {str(e)}")
            return None
