import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useWallet } from '../contexts/WalletContext';
import { Button } from './ui/button';
import { Wallet, FileText, BarChart3, Zap } from 'lucide-react';

const Navbar = () => {
  const { account, connectWallet, disconnectWallet, isConnecting } = useWallet();
  const location = useLocation();

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: BarChart3 },
    { path: '/generator', label: 'Generator', icon: Zap },
    { path: '/library', label: 'Library', icon: FileText },
  ];

  const formatAddress = (address) => {
    if (!address) return '';
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  };

  return (
    <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center space-x-8">
            <Link to="/" className="flex items-center space-x-2">
              <Zap className="h-6 w-6 text-primary" />
              <span className="text-xl font-bold">Smart Contract Generator</span>
            </Link>
            
            <div className="hidden md:flex items-center space-x-6">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-primary text-primary-foreground'
                        : 'text-muted-foreground hover:text-foreground hover:bg-accent'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {account ? (
              <div className="flex items-center space-x-2">
                <div className="flex items-center space-x-2 px-3 py-2 bg-secondary rounded-md">
                  <Wallet className="h-4 w-4 text-green-600" />
                  <span className="text-sm font-medium">{formatAddress(account)}</span>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={disconnectWallet}
                >
                  Disconnect
                </Button>
              </div>
            ) : (
              <Button
                onClick={connectWallet}
                disabled={isConnecting}
                className="flex items-center space-x-2"
              >
                <Wallet className="h-4 w-4" />
                <span>{isConnecting ? 'Connecting...' : 'Connect Wallet'}</span>
              </Button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
