# Multi-Jurisdictional Smart Contract Generator

A React-based frontend application for generating smart contracts tailored to specific jurisdictions and requirements, powered by Gemini AI.

## Features

- **Contract Generator**: Generate smart contracts for different jurisdictions (India, EU, US) and contract types (Escrow, Insurance, Settlement)
- **MetaMask Integration**: Connect wallet and deploy contracts directly from the interface
- **Contract Library**: Browse and manage generated contracts with filtering capabilities
- **Dashboard**: View statistics and analytics of contract generation activity
- **Responsive Design**: Modern UI built with TailwindCSS and shadcn/ui components

## Tech Stack

- **Frontend**: React 18 with Vite
- **Styling**: TailwindCSS + shadcn/ui components
- **Icons**: Lucide React
- **Charts**: Recharts
- **Routing**: React Router DOM
- **Blockchain**: ethers.js for MetaMask integration
- **HTTP Client**: Axios
- **Code Highlighting**: react-syntax-highlighter

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn
- MetaMask browser extension (for wallet features)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Project Structure

```
src/
├── components/
│   ├── ui/           # shadcn/ui components
│   └── Navbar.jsx    # Navigation component
├── contexts/
│   └── WalletContext.jsx  # Wallet state management
├── pages/
│   ├── Dashboard.jsx      # Dashboard with stats
│   ├── ContractGenerator.jsx  # Contract generation form
│   └── ContractLibrary.jsx    # Contract management
├── lib/
│   └── utils.js      # Utility functions
└── App.jsx           # Main app component
```

## API Integration

The application is designed to work with a Flask backend. Update the API endpoints in the following files:

- `src/pages/ContractGenerator.jsx` - Contract generation endpoint
- `src/pages/ContractLibrary.jsx` - Contract listing endpoint  
- `src/pages/Dashboard.jsx` - Dashboard statistics endpoint

## MetaMask Integration

The application includes MetaMask wallet integration for:

- Connecting/disconnecting wallet
- Deploying contracts to blockchain
- Account management

Make sure you have MetaMask installed and configured for the network you want to deploy to.

## Customization

### Adding New Jurisdictions

Update the `jurisdictions` array in `src/pages/ContractGenerator.jsx`:

```javascript
const jurisdictions = [
  { value: 'india', label: 'India' },
  { value: 'eu', label: 'European Union' },
  { value: 'us', label: 'United States' },
  // Add new jurisdictions here
];
```

### Adding New Contract Types

Update the `contractTypes` array in `src/pages/ContractGenerator.jsx`:

```javascript
const contractTypes = [
  { value: 'escrow', label: 'Escrow Contract' },
  { value: 'insurance', label: 'Insurance Contract' },
  { value: 'settlement', label: 'Settlement Contract' },
  // Add new contract types here
];
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
