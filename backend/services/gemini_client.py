import google.generativeai as genai
import json
import os
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini client with API key"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not provided")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_contract(self, payload: Dict[str, Any], legal_rules: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate smart contract using Gemini API
        
        Args:
            payload: Contract generation request data
            legal_rules: Jurisdiction-specific legal rules
            
        Returns:
            Dict containing solidity_code, deploy_script, tests, and metadata
        """
        try:
            prompt = self._build_prompt(payload, legal_rules)
            
            # Generate content with structured output request
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=4000,
                )
            )
            
            # Parse and validate response
            result = self._parse_response(response.text)
            return result
            
        except Exception as e:
            logger.error(f"Error generating contract with Gemini: {str(e)}")
            raise Exception(f"Contract generation failed: {str(e)}")
    
    def _build_prompt(self, payload: Dict[str, Any], legal_rules: Dict[str, Any]) -> str:
        """Build structured prompt for Gemini API"""
        jurisdiction = payload.get('jurisdiction', '').lower()
        contract_type = payload.get('contract_type', '').lower()
        
        # Get jurisdiction-specific rules
        jurisdiction_rules = legal_rules.get('jurisdictions', {}).get(jurisdiction, {})
        contract_type_rules = legal_rules.get('contract_types', {}).get(contract_type, {})
        
        prompt = f"""
You are an expert smart contract developer specializing in multi-jurisdictional compliance. Generate a complete Solidity smart contract based on the following requirements:

## Contract Requirements:
- **Jurisdiction**: {payload.get('jurisdiction', 'N/A')}
- **Contract Type**: {payload.get('contract_type', 'N/A')}
- **Requirements**: {payload.get('requirements', 'N/A')}
- **Description**: {payload.get('description', 'N/A')}
- **Payee Address**: {payload.get('payee_address', 'N/A')}
- **Payer Address**: {payload.get('payer_address', 'N/A')}

## Legal Framework:
{jurisdiction_rules.get('legal_framework', 'Standard contract law')}

## Compliance Rules:
{chr(10).join(jurisdiction_rules.get('compliance_rules', []))}

## Contract-Specific Clauses:
{chr(10).join(jurisdiction_rules.get('contract_clauses', {}).get(contract_type, []))}

## Required Functions:
{chr(10).join(contract_type_rules.get('required_functions', []))}

## Security Considerations:
{chr(10).join(contract_type_rules.get('security_considerations', []))}

Please generate a response in the following JSON format:

```json
{{
  "solidity_code": "Complete Solidity contract code with proper licensing, imports, and comprehensive functionality",
  "deploy_script": "JavaScript deployment script for Hardhat or similar framework",
  "tests": "Comprehensive test suite in JavaScript/TypeScript for the contract",
  "metadata": {{
    "contract_name": "Name of the generated contract",
    "compiler_version": "Recommended Solidity compiler version",
    "optimization": true,
    "license": "SPDX license identifier",
    "description": "Brief description of contract functionality",
    "functions": ["list", "of", "main", "functions"],
    "events": ["list", "of", "events"],
    "security_features": ["list", "of", "security", "features"]
  }}
}}
```

Requirements for the Solidity contract:
1. Use Solidity ^0.8.19 or later
2. Include proper SPDX license identifier
3. Implement all required functions for the contract type
4. Add comprehensive error handling and input validation
5. Include relevant events for transparency
6. Follow best practices for security (reentrancy protection, access control, etc.)
7. Add detailed comments explaining functionality
8. Include jurisdiction-specific compliance features
9. Implement proper state management
10. Add emergency functions if appropriate

The contract should be production-ready and thoroughly tested.
"""
        
        return prompt
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse and validate Gemini response"""
        try:
            # Extract JSON from response (handle markdown code blocks)
            response_text = response_text.strip()
            if '```json' in response_text:
                start = response_text.find('```json') + 7
                end = response_text.find('```', start)
                json_text = response_text[start:end].strip()
            elif '```' in response_text:
                start = response_text.find('```') + 3
                end = response_text.rfind('```')
                json_text = response_text[start:end].strip()
            else:
                json_text = response_text
            
            # Parse JSON
            result = json.loads(json_text)
            
            # Validate required fields
            required_fields = ['solidity_code', 'deploy_script', 'tests', 'metadata']
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate metadata structure
            metadata = result['metadata']
            if not isinstance(metadata, dict):
                raise ValueError("Metadata must be a dictionary")
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            # Return a fallback response
            return self._create_fallback_response()
        except Exception as e:
            logger.error(f"Error parsing response: {str(e)}")
            raise Exception(f"Failed to parse contract generation response: {str(e)}")
    
    def _create_fallback_response(self) -> Dict[str, Any]:
        """Create a fallback response when parsing fails"""
        return {
            "solidity_code": """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title BasicContract
 * @dev A basic smart contract template
 */
contract BasicContract {
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }
    
    function updateOwner(address newOwner) external onlyOwner {
        require(newOwner != address(0), "Invalid address");
        owner = newOwner;
    }
}""",
            "deploy_script": """const { ethers } = require("hardhat");

async function main() {
    const Contract = await ethers.getContractFactory("BasicContract");
    const contract = await Contract.deploy();
    await contract.deployed();
    console.log("Contract deployed to:", contract.address);
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});""",
            "tests": """const { expect } = require("chai");

describe("BasicContract", function () {
    it("Should deploy successfully", async function () {
        const Contract = await ethers.getContractFactory("BasicContract");
        const contract = await Contract.deploy();
        expect(contract.address).to.not.equal(0);
    });
});""",
            "metadata": {
                "contract_name": "BasicContract",
                "compiler_version": "^0.8.19",
                "optimization": True,
                "license": "MIT",
                "description": "Basic contract template",
                "functions": ["updateOwner"],
                "events": [],
                "security_features": ["onlyOwner modifier"]
            }
        }
