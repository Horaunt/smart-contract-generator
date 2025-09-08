from flask import Blueprint, request, jsonify
from services.contract_service import ContractService
import logging

logger = logging.getLogger(__name__)

contracts_bp = Blueprint('contracts', __name__)
contract_service = ContractService()

@contracts_bp.route('/generate', methods=['POST'])
def generate_contract():
    """
    Generate a new smart contract
    
    Expected JSON payload:
    {
        "jurisdiction": "india|eu|us",
        "contract_type": "escrow|insurance|settlement", 
        "requirements": "Contract requirements text",
        "description": "Optional description",
        "payee_address": "0x...",
        "payer_address": "0x..."
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        payload = request.get_json()
        if not payload:
            return jsonify({'error': 'Empty request body'}), 400
        
        # Generate contract
        contract = contract_service.generate_contract(payload)
        
        # Return contract data
        response_data = {
            'success': True,
            'contract': contract.to_dict(),
            'message': 'Contract generated successfully'
        }
        
        return jsonify(response_data), 201
        
    except ValueError as e:
        logger.warning(f"Validation error in contract generation: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error generating contract: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@contracts_bp.route('/contracts', methods=['GET'])
def list_contracts():
    """
    List all contracts with optional filters
    
    Query parameters:
    - jurisdiction: Filter by jurisdiction
    - contract_type: Filter by contract type
    - status: Filter by status
    """
    try:
        # Get query parameters
        filters = {}
        if request.args.get('jurisdiction'):
            filters['jurisdiction'] = request.args.get('jurisdiction')
        if request.args.get('contract_type'):
            filters['contract_type'] = request.args.get('contract_type')
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        
        # Get contracts
        contracts = contract_service.list_contracts(filters)
        
        # Convert to summary format for listing
        contracts_data = [contract.to_summary_dict() for contract in contracts]
        
        return jsonify({
            'success': True,
            'contracts': contracts_data,
            'count': len(contracts_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing contracts: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@contracts_bp.route('/contracts/<int:contract_id>', methods=['GET'])
def get_contract(contract_id):
    """Get a specific contract by ID"""
    try:
        contract = contract_service.get_contract(contract_id)
        
        if not contract:
            return jsonify({'error': 'Contract not found'}), 404
        
        return jsonify({
            'success': True,
            'contract': contract.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching contract {contract_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@contracts_bp.route('/contracts/<int:contract_id>/status', methods=['PUT'])
def update_contract_status(contract_id):
    """
    Update contract status
    
    Expected JSON payload:
    {
        "status": "deployed|failed|draft",
        "transaction_hash": "0x...",
        "contract_address": "0x..."
    }
    """
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        payload = request.get_json()
        status = payload.get('status')
        
        if not status:
            return jsonify({'error': 'Status is required'}), 400
        
        # Valid status values
        valid_statuses = ['draft', 'deployed', 'failed']
        if status not in valid_statuses:
            return jsonify({'error': f'Invalid status. Valid options: {", ".join(valid_statuses)}'}), 400
        
        # Update contract
        success = contract_service.update_contract_status(
            contract_id=contract_id,
            status=status,
            transaction_hash=payload.get('transaction_hash'),
            contract_address=payload.get('contract_address')
        )
        
        if not success:
            return jsonify({'error': 'Contract not found or update failed'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Contract status updated successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating contract status: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@contracts_bp.route('/validate', methods=['POST'])
def validate_contract_request():
    """
    Validate contract generation request without generating
    
    Same payload as /generate endpoint
    """
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        payload = request.get_json()
        if not payload:
            return jsonify({'error': 'Empty request body'}), 400
        
        # Validate request
        validation = contract_service.validate_request(payload)
        
        return jsonify({
            'success': True,
            'validation': validation
        }), 200
        
    except Exception as e:
        logger.error(f"Error validating request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
