import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Input } from '../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { FileText, Calendar, MapPin, CheckCircle, Clock, Search, Eye } from 'lucide-react';
import axios from 'axios';

const ContractLibrary = () => {
  const [contracts, setContracts] = useState([]);
  const [filteredContracts, setFilteredContracts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [jurisdictionFilter, setJurisdictionFilter] = useState('all');
  const [selectedContract, setSelectedContract] = useState(null);

  useEffect(() => {
    fetchContracts();
  }, []);

  useEffect(() => {
    filterContracts();
  }, [contracts, searchTerm, statusFilter, jurisdictionFilter]);

  const fetchContracts = async () => {
    try {
      // Mock data - replace with actual API call
      const mockContracts = [
        {
          id: 1,
          type: 'Escrow',
          jurisdiction: 'India',
          date: '2024-01-15',
          status: 'deployed',
          address: '0x1234...5678',
          description: 'Real estate transaction escrow contract',
          code: '// SPDX-License-Identifier: MIT\npragma solidity ^0.8.19;\n\ncontract EscrowContract {\n    // Contract implementation\n}'
        },
        {
          id: 2,
          type: 'Insurance',
          jurisdiction: 'EU',
          date: '2024-01-20',
          status: 'draft',
          address: null,
          description: 'Travel insurance smart contract',
          code: '// SPDX-License-Identifier: MIT\npragma solidity ^0.8.19;\n\ncontract InsuranceContract {\n    // Contract implementation\n}'
        },
        {
          id: 3,
          type: 'Settlement',
          jurisdiction: 'US',
          date: '2024-01-25',
          status: 'deployed',
          address: '0xabcd...efgh',
          description: 'Dispute settlement contract',
          code: '// SPDX-License-Identifier: MIT\npragma solidity ^0.8.19;\n\ncontract SettlementContract {\n    // Contract implementation\n}'
        },
        {
          id: 4,
          type: 'Escrow',
          jurisdiction: 'India',
          date: '2024-02-01',
          status: 'draft',
          address: null,
          description: 'Freelance payment escrow',
          code: '// SPDX-License-Identifier: MIT\npragma solidity ^0.8.19;\n\ncontract FreelanceEscrow {\n    // Contract implementation\n}'
        },
        {
          id: 5,
          type: 'Insurance',
          jurisdiction: 'US',
          date: '2024-02-05',
          status: 'deployed',
          address: '0x9876...5432',
          description: 'Health insurance contract',
          code: '// SPDX-License-Identifier: MIT\npragma solidity ^0.8.19;\n\ncontract HealthInsurance {\n    // Contract implementation\n}'
        }
      ];

      setContracts(mockContracts);
      
      // Actual API call would be:
      // const response = await axios.get('/api/contracts');
      // setContracts(response.data);
    } catch (error) {
      console.error('Error fetching contracts:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterContracts = () => {
    let filtered = contracts;

    if (searchTerm) {
      filtered = filtered.filter(contract =>
        contract.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
        contract.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (statusFilter !== 'all') {
      filtered = filtered.filter(contract => contract.status === statusFilter);
    }

    if (jurisdictionFilter !== 'all') {
      filtered = filtered.filter(contract => contract.jurisdiction.toLowerCase() === jurisdictionFilter);
    }

    setFilteredContracts(filtered);
  };

  const getStatusBadge = (status) => {
    const variants = {
      deployed: 'default',
      draft: 'secondary'
    };

    const icons = {
      deployed: CheckCircle,
      draft: Clock
    };

    const Icon = icons[status];

    return (
      <Badge variant={variants[status]} className="flex items-center gap-1">
        <Icon className="h-3 w-3" />
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </Badge>
    );
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const ContractModal = ({ contract, onClose }) => {
    if (!contract) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-background rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
          <div className="p-6 border-b">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">{contract.type} Contract</h2>
                <p className="text-muted-foreground">{contract.description}</p>
              </div>
              <Button variant="outline" onClick={onClose}>
                Close
              </Button>
            </div>
          </div>
          
          <div className="p-6 space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Jurisdiction</p>
                <p className="font-medium">{contract.jurisdiction}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">Status</p>
                {getStatusBadge(contract.status)}
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">Created</p>
                <p className="font-medium">{formatDate(contract.date)}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">Address</p>
                <p className="font-medium text-xs">
                  {contract.address || 'Not deployed'}
                </p>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">Contract Code</h3>
              <div className="bg-muted p-4 rounded-md overflow-auto max-h-96">
                <pre className="text-sm">
                  <code>{contract.code}</code>
                </pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading contracts...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Contract Library</h1>
        <p className="text-muted-foreground">
          Browse and manage your generated smart contracts.
        </p>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle>Filters</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Search</label>
              <div className="relative">
                <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search contracts..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-8"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Status</label>
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="deployed">Deployed</SelectItem>
                  <SelectItem value="draft">Draft</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Jurisdiction</label>
              <Select value={jurisdictionFilter} onValueChange={setJurisdictionFilter}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Jurisdictions</SelectItem>
                  <SelectItem value="india">India</SelectItem>
                  <SelectItem value="eu">EU</SelectItem>
                  <SelectItem value="us">US</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Results</label>
              <p className="text-2xl font-bold">{filteredContracts.length}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Contracts Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {filteredContracts.map((contract) => (
          <Card key={contract.id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-2">
                  <FileText className="h-5 w-5 text-primary" />
                  <CardTitle className="text-lg">{contract.type}</CardTitle>
                </div>
                {getStatusBadge(contract.status)}
              </div>
              <CardDescription className="line-clamp-2">
                {contract.description}
              </CardDescription>
            </CardHeader>
            
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-center text-sm text-muted-foreground">
                  <MapPin className="h-4 w-4 mr-2" />
                  {contract.jurisdiction}
                </div>
                <div className="flex items-center text-sm text-muted-foreground">
                  <Calendar className="h-4 w-4 mr-2" />
                  {formatDate(contract.date)}
                </div>
                {contract.address && (
                  <div className="text-sm text-muted-foreground">
                    <span className="font-medium">Address:</span>
                    <br />
                    <code className="text-xs">{contract.address}</code>
                  </div>
                )}
              </div>

              <Button
                variant="outline"
                className="w-full"
                onClick={() => setSelectedContract(contract)}
              >
                <Eye className="h-4 w-4 mr-2" />
                View Details
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredContracts.length === 0 && (
        <div className="text-center py-12">
          <FileText className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <h3 className="text-lg font-semibold mb-2">No contracts found</h3>
          <p className="text-muted-foreground">
            Try adjusting your filters or generate your first contract.
          </p>
        </div>
      )}

      {/* Contract Details Modal */}
      {selectedContract && (
        <ContractModal
          contract={selectedContract}
          onClose={() => setSelectedContract(null)}
        />
      )}
    </div>
  );
};

export default ContractLibrary;
