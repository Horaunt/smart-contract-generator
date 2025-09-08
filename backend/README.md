# Multi-Jurisdictional Smart Contract Generator - Backend

Flask-based backend API for generating jurisdiction-specific smart contracts using Google's Gemini AI.

## Features

- **Contract Generation**: AI-powered smart contract generation using Gemini API
- **Multi-Jurisdictional Support**: India, EU, and US legal compliance
- **Contract Types**: Escrow, Insurance, and Settlement contracts
- **Database Storage**: SQLite with SQLAlchemy ORM
- **MetaMask Integration**: Deployment preparation for frontend wallet integration
- **Legal Rules Engine**: YAML-based jurisdiction-specific compliance rules

## Setup

### Prerequisites

- Python 3.11+
- pip (Python package manager)
- Google Gemini API key

### Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Contract Operations

#### Generate Contract
```http
POST /api/generate
Content-Type: application/json

{
  "jurisdiction": "india|eu|us",
  "contract_type": "escrow|insurance|settlement",
  "requirements": "Contract requirements description",
  "description": "Optional additional description",
  "payee_address": "0x...",
  "payer_address": "0x..."
}
```

#### List Contracts
```http
GET /api/contracts?jurisdiction=india&contract_type=escrow&status=deployed
```

#### Get Specific Contract
```http
GET /api/contracts/{id}
```

#### Update Contract Status
```http
PUT /api/contracts/{id}/status
Content-Type: application/json

{
  "status": "deployed|failed|draft",
  "transaction_hash": "0x...",
  "contract_address": "0x..."
}
```

#### Validate Request
```http
POST /api/validate
Content-Type: application/json

{
  "jurisdiction": "india",
  "contract_type": "escrow",
  "requirements": "Basic escrow requirements"
}
```

### Deployment Operations

#### Prepare Deployment
```http
POST /api/deploy/{id}
```

#### Confirm Deployment
```http
POST /api/deploy/{id}/confirm
Content-Type: application/json

{
  "transaction_hash": "0x...",
  "contract_address": "0x...",
  "gas_used": 1234567
}
```

#### Get Contract Bytecode
```http
GET /api/deploy/{id}/bytecode
```

#### Estimate Gas
```http
POST /api/deploy/estimate-gas
Content-Type: application/json

{
  "contract_type": "escrow",
  "jurisdiction": "india"
}
```

## Project Structure

```
backend/
├── app.py                    # Flask application entry point
├── models.py                 # SQLAlchemy database models
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── routes/
│   ├── contracts.py         # Contract-related endpoints
│   └── deploy.py           # Deployment-related endpoints
├── services/
│   ├── gemini_client.py    # Gemini API integration
│   └── contract_service.py # Business logic for contracts
├── legal_rules/
│   └── jurisdictions.yaml  # Legal compliance rules
└── instance/
    └── contracts.db        # SQLite database (auto-created)
```

## Legal Rules Engine

The system uses YAML-based rules in `legal_rules/jurisdictions.yaml` to ensure compliance:

- **Jurisdiction-specific requirements**: Required fields and validation rules
- **Contract type specifications**: Function requirements and security considerations
- **Compliance clauses**: Legal framework integration for each jurisdiction

## Database Schema

### Contract Table
- `id`: Primary key
- `jurisdiction`: Contract jurisdiction (india/eu/us)
- `contract_type`: Type of contract (escrow/insurance/settlement)
- `requirements`: User requirements text
- `description`: Optional description
- `payee_address`: Ethereum address of payee
- `payer_address`: Ethereum address of payer
- `solidity_code`: Generated Solidity contract code
- `deploy_script`: Deployment script
- `tests`: Test suite for the contract
- `metadata`: JSON metadata about the contract
- `status`: Current status (draft/deployed/failed)
- `transaction_hash`: Deployment transaction hash
- `contract_address`: Deployed contract address
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `FLASK_ENV` | Flask environment | development |
| `FLASK_DEBUG` | Enable debug mode | True |
| `SECRET_KEY` | Flask secret key | dev-secret-key |
| `DATABASE_URL` | Database connection string | sqlite:///instance/contracts.db |
| `FRONTEND_URL` | Frontend URL for CORS | http://localhost:5173 |
| `PORT` | Server port | 5000 |

## Testing

### Health Check
```bash
curl http://localhost:5000/health
```

### API Info
```bash
curl http://localhost:5000/api
```

### Generate Contract Example
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "jurisdiction": "india",
    "contract_type": "escrow",
    "requirements": "Simple escrow for freelance payment",
    "payee_address": "0x742d35Cc6634C0532925a3b8D4B9b4e4e4e4e4e4",
    "payer_address": "0x8ba1f109551bD432803012645Hac136c22C177e9"
  }'
```

## Security Considerations

- API keys are loaded from environment variables
- CORS is configured for frontend integration
- Input validation on all endpoints
- No private keys stored on backend
- Deployment preparation returns unsigned transactions for client-side signing

## Error Handling

The API returns consistent error responses:

```json
{
  "error": "Error description",
  "details": "Additional error details (if available)"
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created (for contract generation)
- `400`: Bad Request (validation errors)
- `404`: Not Found
- `500`: Internal Server Error

## Development

### Adding New Jurisdictions

1. Update `legal_rules/jurisdictions.yaml`
2. Add validation logic in `contract_service.py`
3. Update API documentation

### Adding New Contract Types

1. Add contract type to `jurisdictions.yaml`
2. Update validation in `contract_service.py`
3. Extend Gemini prompts if needed

## Production Deployment

1. Set `FLASK_ENV=production`
2. Use a production WSGI server (gunicorn, uWSGI)
3. Configure proper database (PostgreSQL recommended)
4. Set up proper logging and monitoring
5. Use environment-specific configuration
