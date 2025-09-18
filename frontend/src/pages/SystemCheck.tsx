import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  RefreshCw, 
  ArrowLeft,
  Database,
  Cpu,
  Settings,
  Navigation,
  FileCheck
} from "lucide-react";
import { runSystemIntegrityCheck, quickHealthCheck, SystemIntegrityResult } from "@/utils/systemIntegrityChecker";
import { useNavigate } from "react-router-dom";

const SystemCheck = () => {
  const navigate = useNavigate();
  const [isRunning, setIsRunning] = useState(false);
  const [results, setResults] = useState<SystemIntegrityResult | null>(null);
  const [quickHealth, setQuickHealth] = useState<boolean | null>(null);

  useEffect(() => {
    // Run quick health check on mount
    const health = quickHealthCheck();
    setQuickHealth(health);
  }, []);

  const runFullCheck = async () => {
    setIsRunning(true);
    
    // Simulate some delay for better UX
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    try {
      const checkResults = runSystemIntegrityCheck();
      setResults(checkResults);
    } catch (error) {
      console.error('System check failed:', error);
    } finally {
      setIsRunning(false);
    }
  };

  const getStatusIcon = (status: 'PASS' | 'FAIL' | 'WARNING') => {
    switch (status) {
      case 'PASS':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'FAIL':
        return <XCircle className="h-5 w-5 text-red-600" />;
      case 'WARNING':
        return <AlertTriangle className="h-5 w-5 text-yellow-600" />;
    }
  };

  const getStatusColor = (status: 'PASS' | 'FAIL' | 'WARNING') => {
    switch (status) {
      case 'PASS':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'FAIL':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'WARNING':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    }
  };

  const componentIcons = {
    assessment: <FileCheck className="h-5 w-5" />,
    algorithm: <Cpu className="h-5 w-5" />,
    careerDatabase: <Database className="h-5 w-5" />,
    dataFlow: <Settings className="h-5 w-5" />,
    navigation: <Navigation className="h-5 w-5" />
  };

  const componentNames = {
    assessment: 'Assessment Component',
    algorithm: 'Career Matching Algorithm',
    careerDatabase: 'Career Database',
    dataFlow: 'Data Flow Integration',
    navigation: 'Navigation System'
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <Button 
            variant="ghost" 
            className="mb-4"
            onClick={() => navigate('/dashboard')}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
          
          <h1 className="text-3xl font-bold text-gray-900 mb-2">System Integrity Check</h1>
          <p className="text-gray-600">
            Comprehensive validation of all system components and data flow
          </p>
        </div>

        {/* Quick Health Status */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <span>Quick Health Status</span>
              {quickHealth !== null && getStatusIcon(quickHealth ? 'PASS' : 'FAIL')}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">
                Basic system functionality check
              </span>
              <Badge className={quickHealth ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                {quickHealth ? 'Healthy' : 'Issues Detected'}
              </Badge>
            </div>
          </CardContent>
        </Card>

        {/* Run Full Check */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Full System Check</CardTitle>
            <CardDescription>
              Run comprehensive validation of all system components
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button 
              onClick={runFullCheck} 
              disabled={isRunning}
              className="w-full"
            >
              {isRunning ? (
                <>
                  <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                  Running System Check...
                </>
              ) : (
                <>
                  <Settings className="h-4 w-4 mr-2" />
                  Run Full System Check
                </>
              )}
            </Button>
            
            {isRunning && (
              <div className="mt-4">
                <Progress value={75} className="h-2" />
                <p className="text-sm text-gray-600 mt-2">
                  Validating components and data flow...
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Results */}
        {results && (
          <>
            {/* Overall Status */}
            <Card className="mb-6">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <span>Overall System Status</span>
                  {getStatusIcon(results.overall)}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className={`p-4 rounded-lg border ${getStatusColor(results.overall)}`}>
                  <div className="flex items-center space-x-2">
                    {getStatusIcon(results.overall)}
                    <span className="font-semibold">
                      System Status: {results.overall}
                    </span>
                  </div>
                  <p className="text-sm mt-2">
                    {results.overall === 'PASS' && 'All systems operational'}
                    {results.overall === 'WARNING' && 'System operational with minor issues'}
                    {results.overall === 'FAIL' && 'Critical issues detected - immediate attention required'}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Component Status */}
            <Card className="mb-6">
              <CardHeader>
                <CardTitle>Component Status</CardTitle>
                <CardDescription>
                  Individual component validation results
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {Object.entries(results.components).map(([key, status]) => (
                    <div key={key} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center space-x-3">
                        {componentIcons[key as keyof typeof componentIcons]}
                        <span className="font-medium">
                          {componentNames[key as keyof typeof componentNames]}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(status)}
                        <Badge className={getStatusColor(status)}>
                          {status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Issues */}
            {results.issues.length > 0 && (
              <Card className="mb-6">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <AlertTriangle className="h-5 w-5 text-yellow-600" />
                    <span>Issues Detected</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {results.issues.map((issue, index) => (
                      <div key={index} className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                        <p className="text-sm text-yellow-800">{issue}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Recommendations */}
            {results.recommendations.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <CheckCircle className="h-5 w-5 text-blue-600" />
                    <span>Recommendations</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {results.recommendations.map((recommendation, index) => (
                      <div key={index} className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                        <p className="text-sm text-blue-800">{recommendation}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default SystemCheck;