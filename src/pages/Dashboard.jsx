import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { FileText, CheckCircle, Globe, TrendingUp } from 'lucide-react';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalContracts: 0,
    deployedContracts: 0,
    jurisdictions: 0,
    contractTypes: []
  });

  const [contractData, setContractData] = useState([]);
  const [jurisdictionData, setJurisdictionData] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Mock data for now - replace with actual API calls
      const mockStats = {
        totalContracts: 24,
        deployedContracts: 18,
        jurisdictions: 3,
        contractTypes: [
          { name: 'Escrow', count: 12 },
          { name: 'Insurance', count: 8 },
          { name: 'Settlement', count: 4 }
        ]
      };

      const mockContractData = [
        { month: 'Jan', contracts: 4 },
        { month: 'Feb', contracts: 7 },
        { month: 'Mar', contracts: 5 },
        { month: 'Apr', contracts: 8 },
        { month: 'May', contracts: 6 },
        { month: 'Jun', contracts: 9 }
      ];

      const mockJurisdictionData = [
        { name: 'India', value: 10, color: '#8884d8' },
        { name: 'EU', value: 8, color: '#82ca9d' },
        { name: 'US', value: 6, color: '#ffc658' }
      ];

      setStats(mockStats);
      setContractData(mockContractData);
      setJurisdictionData(mockJurisdictionData);

      // Uncomment when backend is ready
      // const response = await axios.get('/api/dashboard/stats');
      // setStats(response.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const StatCard = ({ title, value, description, icon: Icon, trend }) => (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className="text-xs text-muted-foreground">{description}</p>
        {trend && (
          <div className="flex items-center pt-1">
            <TrendingUp className="h-3 w-3 text-green-600 mr-1" />
            <span className="text-xs text-green-600">{trend}</span>
          </div>
        )}
      </CardContent>
    </Card>
  );

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Overview of your smart contract generation and deployment activity.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Contracts"
          value={stats.totalContracts}
          description="Contracts generated"
          icon={FileText}
          trend="+12% from last month"
        />
        <StatCard
          title="Deployed Contracts"
          value={stats.deployedContracts}
          description="Successfully deployed"
          icon={CheckCircle}
          trend="+8% from last month"
        />
        <StatCard
          title="Jurisdictions"
          value={stats.jurisdictions}
          description="Different jurisdictions"
          icon={Globe}
        />
        <StatCard
          title="Success Rate"
          value={`${Math.round((stats.deployedContracts / stats.totalContracts) * 100)}%`}
          description="Deployment success rate"
          icon={TrendingUp}
          trend="+2% from last month"
        />
      </div>

      {/* Charts */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Contract Generation Trend</CardTitle>
            <CardDescription>Monthly contract generation over time</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={contractData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="contracts" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Contracts by Jurisdiction</CardTitle>
            <CardDescription>Distribution of contracts across jurisdictions</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={jurisdictionData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {jurisdictionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Contract Types */}
      <Card>
        <CardHeader>
          <CardTitle>Contract Types</CardTitle>
          <CardDescription>Breakdown of generated contract types</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {stats.contractTypes.map((type, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 rounded-full bg-primary"></div>
                  <span className="font-medium">{type.name}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-32 bg-secondary rounded-full h-2">
                    <div
                      className="bg-primary h-2 rounded-full"
                      style={{ width: `${(type.count / stats.totalContracts) * 100}%` }}
                    ></div>
                  </div>
                  <span className="text-sm text-muted-foreground">{type.count}</span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;
