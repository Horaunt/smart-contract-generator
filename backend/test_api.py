#!/usr/bin/env python3
"""
Test script for the Smart Contract Generator API
Run this after starting the Flask server to test all endpoints
"""

import requests
import json
import sys
import time

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Flask app is running.")
        return False

def test_api_info():
    """Test API info endpoint"""
    print("\nTesting API info...")
    try:
        response = requests.get(f"{BASE_URL}/api")
        if response.status_code == 200:
            data = response.json()
            print("✅ API info retrieved successfully")
            print(f"   API Name: {data.get('name')}")
            print(f"   Version: {data.get('version')}")
            return True
        else:
            print(f"❌ API info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API info error: {str(e)}")
        return False

def test_validate_request():
    """Test request validation"""
    print("\nTesting request validation...")
    
    # Valid request
    valid_payload = {
        "jurisdiction": "india",
        "contract_type": "escrow",
        "requirements": "Simple escrow for freelance payment"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/validate",
            json=valid_payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('validation', {}).get('valid'):
                print("✅ Valid request validation passed")
            else:
                print(f"❌ Valid request marked as invalid: {data}")
                return False
        else:
            print(f"❌ Validation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Validation error: {str(e)}")
        return False
    
    # Invalid request
    invalid_payload = {
        "jurisdiction": "invalid",
        "contract_type": "unknown"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/validate",
            json=invalid_payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if not data.get('validation', {}).get('valid'):
                print("✅ Invalid request validation passed")
                return True
            else:
                print(f"❌ Invalid request marked as valid: {data}")
                return False
        else:
            print(f"❌ Invalid validation test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Invalid validation error: {str(e)}")
        return False

def test_contract_generation():
    """Test contract generation (requires Gemini API key)"""
    print("\nTesting contract generation...")
    
    payload = {
        "jurisdiction": "india",
        "contract_type": "escrow",
        "requirements": "Simple escrow contract for freelance payment of $1000",
        "description": "Escrow contract between freelancer and client",
        "payee_address": "0x742d35Cc6634C0532925a3b8D4B9b4e4e4e4e4e4",
        "payer_address": "0x8ba1f109551bD432803012645Hac136c22C177e9"
    }
    
    try:
        print("   Generating contract (this may take 10-30 seconds)...")
        response = requests.post(
            f"{BASE_URL}/api/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 201:
            data = response.json()
            contract = data.get('contract')
            if contract and contract.get('solidity_code'):
                print("✅ Contract generation successful")
                print(f"   Contract ID: {contract.get('id')}")
                print(f"   Status: {contract.get('status')}")
                print(f"   Code length: {len(contract.get('solidity_code', ''))} characters")
                return contract.get('id')
            else:
                print(f"❌ Contract generation incomplete: {data}")
                return None
        else:
            print(f"❌ Contract generation failed: {response.status_code}")
            if response.text:
                print(f"   Error: {response.text}")
            return None
    except requests.exceptions.Timeout:
        print("❌ Contract generation timed out (check Gemini API key)")
        return None
    except Exception as e:
        print(f"❌ Contract generation error: {str(e)}")
        return None

def test_list_contracts():
    """Test contract listing"""
    print("\nTesting contract listing...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/contracts")
        
        if response.status_code == 200:
            data = response.json()
            contracts = data.get('contracts', [])
            print(f"✅ Contract listing successful ({len(contracts)} contracts)")
            return len(contracts) > 0
        else:
            print(f"❌ Contract listing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Contract listing error: {str(e)}")
        return False

def test_get_contract(contract_id):
    """Test getting specific contract"""
    if not contract_id:
        print("\nSkipping contract retrieval (no contract ID)")
        return False
    
    print(f"\nTesting contract retrieval for ID {contract_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/contracts/{contract_id}")
        
        if response.status_code == 200:
            data = response.json()
            contract = data.get('contract')
            if contract:
                print("✅ Contract retrieval successful")
                print(f"   Type: {contract.get('contract_type')}")
                print(f"   Jurisdiction: {contract.get('jurisdiction')}")
                return True
            else:
                print(f"❌ Contract retrieval incomplete: {data}")
                return False
        else:
            print(f"❌ Contract retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Contract retrieval error: {str(e)}")
        return False

def test_deployment_preparation(contract_id):
    """Test deployment preparation"""
    if not contract_id:
        print("\nSkipping deployment preparation (no contract ID)")
        return False
    
    print(f"\nTesting deployment preparation for contract {contract_id}...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/deploy/{contract_id}")
        
        if response.status_code == 200:
            data = response.json()
            deployment_data = data.get('deployment_data')
            if deployment_data:
                print("✅ Deployment preparation successful")
                print(f"   Contract name: {deployment_data.get('contract_name')}")
                print(f"   Estimated gas: {deployment_data.get('estimated_gas')}")
                return True
            else:
                print(f"❌ Deployment preparation incomplete: {data}")
                return False
        else:
            print(f"❌ Deployment preparation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Deployment preparation error: {str(e)}")
        return False

def test_gas_estimation():
    """Test gas estimation"""
    print("\nTesting gas estimation...")
    
    payload = {
        "contract_type": "escrow",
        "jurisdiction": "india"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/deploy/estimate-gas",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            estimated_gas = data.get('estimated_gas')
            if estimated_gas:
                print("✅ Gas estimation successful")
                print(f"   Estimated gas: {estimated_gas}")
                return True
            else:
                print(f"❌ Gas estimation incomplete: {data}")
                return False
        else:
            print(f"❌ Gas estimation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Gas estimation error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Smart Contract Generator API Test Suite")
    print("=" * 50)
    
    # Basic connectivity tests
    if not test_health_check():
        print("\n❌ Server not accessible. Please start the Flask app first.")
        sys.exit(1)
    
    if not test_api_info():
        print("\n❌ API info endpoint failed.")
        sys.exit(1)
    
    # Validation tests
    if not test_validate_request():
        print("\n❌ Request validation failed.")
        sys.exit(1)
    
    # Contract operations
    contract_id = test_contract_generation()
    
    # List contracts
    test_list_contracts()
    
    # Get specific contract
    test_get_contract(contract_id)
    
    # Deployment tests
    test_deployment_preparation(contract_id)
    test_gas_estimation()
    
    print("\n" + "=" * 50)
    print("🎉 API test suite completed!")
    
    if contract_id:
        print(f"\n📝 Generated contract ID: {contract_id}")
        print("   You can view it in the frontend or call the API directly.")
    else:
        print("\n⚠️  Contract generation failed. Check your Gemini API key in .env file.")

if __name__ == "__main__":
    main()
