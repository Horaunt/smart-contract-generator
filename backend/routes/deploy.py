from flask import Blueprint, request, jsonify
from services.contract_service import ContractService
import logging

logger = logging.getLogger(__name__)

deploy_bp = Blueprint('deploy', __name__)
contract_service = ContractService()

@deploy_bp.route('/deploy/<int:contract_id>', methods=['POST'])
def prepare_deployment(contract_id):
    """
    Prepare contract deployment data for MetaMask
    
    Returns unsigned transaction data that can be signed by MetaMask
    """
    try:
        # Get deployment data
        deployment_data = contract_service.get_deployment_data(contract_id)
        
        if not deployment_data:
            return jsonify({'error': 'Contract not found or invalid'}), 404
        
        # Prepare response for frontend MetaMask integration
        response_data = {
            'success': True,
            'deployment_data': {
                'contract_id': deployment_data['contract_id'],
                'contract_name': deployment_data['contract_name'],
                'solidity_code': deployment_data['solidity_code'],
                'constructor_params': deployment_data['constructor_params'],
                'estimated_gas': deployment_data['estimated_gas'],
                'metadata': deployment_data['metadata']
            },
            'instructions': {
                'step1': 'Compile the Solidity code using your preferred method',
                'step2': 'Deploy using MetaMask with the provided constructor parameters',
                'step3': 'Call /deploy/{contract_id}/confirm with transaction hash after deployment'
            }
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error preparing deployment for contract {contract_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@deploy_bp.route('/deploy/<int:contract_id>/confirm', methods=['POST'])
def confirm_deployment(contract_id):
    """
    Confirm successful deployment with transaction hash
    
    Expected JSON payload:
    {
        "transaction_hash": "0x...",
        "contract_address": "0x...",
        "gas_used": 1234567
    }
    """
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        payload = request.get_json()
        transaction_hash = payload.get('transaction_hash')
        contract_address = payload.get('contract_address')
        
        if not transaction_hash:
            return jsonify({'error': 'Transaction hash is required'}), 400
        
        # Update contract status to deployed
        success = contract_service.update_contract_status(
            contract_id=contract_id,
            status='deployed',
            transaction_hash=transaction_hash,
            contract_address=contract_address
        )
        
        if not success:
            return jsonify({'error': 'Contract not found or update failed'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Deployment confirmed successfully',
            'contract_id': contract_id,
            'transaction_hash': transaction_hash,
            'contract_address': contract_address
        }), 200
        
    except Exception as e:
        logger.error(f"Error confirming deployment: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@deploy_bp.route('/deploy/<int:contract_id>/bytecode', methods=['GET'])
def get_contract_bytecode(contract_id):
    """
    Get compiled bytecode for contract deployment
    Note: This is a placeholder - in production, you'd use a Solidity compiler
    """
    try:
        deployment_data = contract_service.get_deployment_data(contract_id)
        
        if not deployment_data:
            return jsonify({'error': 'Contract not found'}), 404
        
        # In a real implementation, you would compile the Solidity code here
        # For now, return a placeholder bytecode
        placeholder_bytecode = "0x608060405234801561001057600080fd5b50600080fdfea2646970667358221220"
        
        return jsonify({
            'success': True,
            'contract_id': contract_id,
            'bytecode': placeholder_bytecode,
            'abi': [],  # Would contain actual ABI from compilation
            'constructor_params': deployment_data['constructor_params'],
            'note': 'This is placeholder bytecode. In production, compile the Solidity code first.'
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting bytecode: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@deploy_bp.route('/deploy/estimate-gas', methods=['POST'])
def estimate_gas():
    """
    Estimate gas for contract deployment
    
    Expected JSON payload:
    {
        "contract_type": "escrow|insurance|settlement",
        "jurisdiction": "india|eu|us"
    }
    """
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        payload = request.get_json()
        contract_type = payload.get('contract_type', '').lower()
        jurisdiction = payload.get('jurisdiction', '').lower()
        
        # Gas estimates based on contract complexity
        gas_estimates = {
            'escrow': {
                'base': 1500000,
                'india': 1600000,  # Additional compliance features
                'eu': 1700000,     # GDPR compliance
                'us': 1650000      # State-specific features
            },
            'insurance': {
                'base': 2000000,
                'india': 2100000,
                'eu': 2200000,
                'us': 2150000
            },
            'settlement': {
                'base': 1800000,
                'india': 1900000,
                'eu': 2000000,
                'us': 1950000
            }
        }
        
        # Get estimate
        base_gas = gas_estimates.get(contract_type, {}).get('base', 1500000)
        jurisdiction_gas = gas_estimates.get(contract_type, {}).get(jurisdiction, base_gas)
        
        return jsonify({
            'success': True,
            'estimated_gas': jurisdiction_gas,
            'contract_type': contract_type,
            'jurisdiction': jurisdiction,
            'note': 'Gas estimates are approximate and may vary based on network conditions'
        }), 200
        
    except Exception as e:
        logger.error(f"Error estimating gas: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
