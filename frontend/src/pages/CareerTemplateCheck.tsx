import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  RefreshCw, 
  ArrowLeft,
  Database,
  Search,
  FileCheck
} from "lucide-react";
import { 
  validateCareerTemplates, 
  validateCareerTypeExists, 
  getAllCareerTypes, 
  findInvalidCareerTypes,
  ValidationIssue,
  CareerTemplateValidationResult 
} from "@/utils/careerTemplateValidator";
import { CAREER_TEMPLATES } from "@/utils/careerMatching";
import { useNavigate } from "react-router-dom";

const CareerTemplateCheck = () => {
  const navigate = useNavigate();
  const [validationResult, setValidationResult] = useState<CareerTemplateValidationResult | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [selectedCareerType, setSelectedCareerType] = useState('');

  useEffect(() => {
    runValidation();
  }, []);

  const runValidation = async () => {
    setIsRunning(true);
    
    // Simulate some delay for better UX
    await new Promise(resolve => setTimeout(resolve, 500));
    
    try {
      const result = validateCareerTemplates();
      setValidationResult(result);
    } catch (error) {
      console.error('Validation failed:', error);
    } finally {
      setIsRunning(false);
    }
  };

  const checkSpecificCareerType = () => {
    if (!selectedCareerType) return;
    
    const exists = validateCareerTypeExists(selectedCareerType);
    if (exists) {
      alert(`✅ Career type "${selectedCareerType}" exists in templates`);
    } else {
      alert(`❌ Career type "${selectedCareerType}" NOT FOUND in templates`);
    }
  };

  const getIssueIcon = (severity: 'error' | 'warning') => {
    return severity === 'error' ? 
      <XCircle className="h-4 w-4 text-red-600" /> : 
      <AlertTriangle className="h-4 w-4 text-yellow-600" />;
  };

  const getIssueColor = (severity: 'error' | 'warning') => {
    return severity === 'error' ? 
      'bg-red-50 border-red-200 text-red-800' : 
      'bg-yellow-50 border-yellow-200 text-yellow-800';
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <Button 
            variant="ghost" 
            className="mb-4"
            onClick={() => navigate('/dashboard')}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
          
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Career Template Validation</h1>
          <p className="text-gray-600">
            Check for missing job descriptions and careerType inconsistencies
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid md:grid-cols-4 gap-4 mb-6">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center space-x-2">
                <Database className="h-5 w-5 text-blue-600" />
                <div>
                  <p className="text-sm text-gray-600">Total Careers</p>
                  <p className="text-2xl font-bold">{CAREER_TEMPLATES.length}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center space-x-2">
                {validationResult?.isValid ? 
                  <CheckCircle className="h-5 w-5 text-green-600" /> : 
                  <XCircle className="h-5 w-5 text-red-600" />
                }
                <div>
                  <p className="text-sm text-gray-600">Validation Status</p>
                  <p className="text-lg font-bold">
                    {validationResult?.isValid ? 'Valid' : 'Issues Found'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center space-x-2">
                <XCircle className="h-5 w-5 text-red-600" />
                <div>
                  <p className="text-sm text-gray-600">Errors</p>
                  <p className="text-2xl font-bold text-red-600">
                    {validationResult?.issues.filter(i => i.severity === 'error').length || 0}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center space-x-2">
                <AlertTriangle className="h-5 w-5 text-yellow-600" />
                <div>
                  <p className="text-sm text-gray-600">Warnings</p>
                  <p className="text-2xl font-bold text-yellow-600">
                    {validationResult?.issues.filter(i => i.severity === 'warning').length || 0}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Validation Controls */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Validation Controls</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex space-x-4 mb-4">
              <Button 
                onClick={runValidation} 
                disabled={isRunning}
              >
                {isRunning ? (
                  <>
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                    Validating...
                  </>
                ) : (
                  <>
                    <FileCheck className="h-4 w-4 mr-2" />
                    Run Full Validation
                  </>
                )}
              </Button>
            </div>
            
            {/* Career Type Checker */}
            <div className="flex space-x-2">
              <input
                type="text"
                placeholder="Enter careerType to check (e.g., vp-product-management)"
                value={selectedCareerType}
                onChange={(e) => setSelectedCareerType(e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md"
              />
              <Button onClick={checkSpecificCareerType} variant="outline">
                <Search className="h-4 w-4 mr-2" />
                Check
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Validation Results */}
        {validationResult && (
          <>
            {/* Overall Status */}
            <Alert className={`mb-6 ${validationResult.isValid ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
              <div className="flex items-center space-x-2">
                {validationResult.isValid ? 
                  <CheckCircle className="h-5 w-5 text-green-600" /> : 
                  <XCircle className="h-5 w-5 text-red-600" />
                }
                <AlertDescription className={validationResult.isValid ? 'text-green-800' : 'text-red-800'}>
                  {validationResult.isValid ? 
                    'All career templates are valid and complete!' : 
                    `Found ${validationResult.issues.length} issues that need attention`
                  }
                </AlertDescription>
              </div>
            </Alert>

            {/* Issues List */}
            {validationResult.issues.length > 0 && (
              <Card className="mb-6">
                <CardHeader>
                  <CardTitle>Issues Found</CardTitle>
                  <CardDescription>
                    {validationResult.issues.filter(i => i.severity === 'error').length} errors and {validationResult.issues.filter(i => i.severity === 'warning').length} warnings
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {validationResult.issues.map((issue, index) => (
                      <div key={index} className={`p-3 rounded-lg border ${getIssueColor(issue.severity)}`}>
                        <div className="flex items-start space-x-2">
                          {getIssueIcon(issue.severity)}
                          <div className="flex-1">
                            <p className="font-medium">{issue.careerTitle}</p>
                            <p className="text-sm opacity-90">careerType: {issue.careerType}</p>
                            <p className="text-sm mt-1">{issue.issue}</p>
                          </div>
                          <Badge variant={issue.severity === 'error' ? 'destructive' : 'secondary'}>
                            {issue.severity}
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Duplicate Career Types */}
            {validationResult.duplicateCareerTypes.length > 0 && (
              <Card className="mb-6">
                <CardHeader>
                  <CardTitle className="text-red-600">Duplicate Career Types</CardTitle>
                  <CardDescription>
                    These careerType values are used by multiple careers
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {validationResult.duplicateCareerTypes.map((careerType, index) => (
                      <div key={index} className="p-2 bg-red-50 border border-red-200 rounded">
                        <code className="text-red-800">{careerType}</code>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* All Career Types */}
            <Card>
              <CardHeader>
                <CardTitle>All Career Types</CardTitle>
                <CardDescription>
                  Complete list of careerType values in the system
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-3 gap-2 max-h-64 overflow-y-auto">
                  {getAllCareerTypes().map((careerType, index) => (
                    <div key={index} className="p-2 bg-gray-50 border border-gray-200 rounded">
                      <code className="text-sm">{careerType}</code>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </>
        )}
      </div>
    </div>
  );
};

export default CareerTemplateCheck;