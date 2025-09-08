import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { WalletProvider } from './contexts/WalletContext';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import ContractGenerator from './pages/ContractGenerator';
import ContractLibrary from './pages/ContractLibrary';

function App() {
  return (
    <WalletProvider>
      <Router>
        <div className="min-h-screen bg-background">
          <Navbar />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/generator" element={<ContractGenerator />} />
              <Route path="/library" element={<ContractLibrary />} />
            </Routes>
          </main>
        </div>
      </Router>
    </WalletProvider>
  );
}

export default App;
