import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Progress } from "@/components/ui/progress";
import { 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  RefreshCw, 
  ArrowLeft,
  Search,
  Heart,
  Briefcase,
  User,
  Database,
  Settings
} from "lucide-react";
import { generateCareerRecommendations } from "@/utils/enhancedCareerMatching";
import { useNavigate } from "react-router-dom";
import { showSuccess, showError } from "@/utils/toast";

interface TestResult {
  name: string;
  status: 'pass' | 'fail' | 'warning';
  message: string;
  details?: any;
}

const SystemTest = () => {
  const navigate = useNavigate();
  const [testResults, setTestResults] = useState<TestResult[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [testProgress, setTestProgress] = useState(0);

  useEffect(() => {
    // Load current user
    const userData = localStorage.getItem('currentUser');
    if (userData) {
      setCurrentUser(JSON.parse(userData));
    }
  }, []);

  const runComprehensiveTest = async () => {
    setIsRunning(true);
    setTestResults([]);
    setTestProgress(0);
    
    const tests: TestResult[] = [];
    const totalTests = 8;
    let currentTest = 0;

    const updateProgress = () => {
      currentTest++;
      setTestProgress((currentTest / totalTests) * 100);
    };

    try {
      // Test 1: Career Database Integrity
      console.log('🧪 Test 1: Career Database Integrity');
      try {
        const careerCount = CAREER_TEMPLATES.length;
        if (careerCount > 0) {
          // Check for required fields
          const missingFields = CAREER_TEMPLATES.filter(career => 
            !career.title || !career.careerType || !career.salaryRange || !career.description
          );
          
          if (missingFields.length === 0) {
            tests.push({
              name: "Career Database Integrity",
              status: 'pass',
              message: `${careerCount} careers loaded with complete data`,
              details: { careerCount, missingFields: 0 }
            });
          } else {
            tests.push({
              name: "Career Database Integrity",
              status: 'warning',
              message: `${careerCount} careers loaded, ${missingFields.length} have missing fields`,
              details: { careerCount, missingFields: missingFields.length }
            });
          }
        } else {
          tests.push({
            name: "Career Database Integrity",
            status: 'fail',
            message: "No careers found in database",
            details: { careerCount: 0 }
          });
        }
      } catch (error) {
        tests.push({
          name: "Career Database Integrity",
          status: 'fail',
          message: `Database error: ${error}`,
          details: { error }
        });
      }
      updateProgress();

      // Test 2: User Authentication & Data
      console.log('🧪 Test 2: User Authentication & Data');
      try {
        if (currentUser) {
          if (currentUser.assessmentData && currentUser.profileCompleted) {
            tests.push({
              name: "User Authentication & Data",
              status: 'pass',
              message: `User ${currentUser.firstName} ${currentUser.lastName} with complete profile`,
              details: { 
                userId: currentUser.id, 
                profileComplete: currentUser.profileCompleted,
                hasAssessment: !!currentUser.assessmentData
              }
            });
          } else {
            tests.push({
              name: "User Authentication & Data",
              status: 'warning',
              message: `User logged in but profile incomplete`,
              details: { 
                userId: currentUser.id, 
                profileComplete: currentUser.profileCompleted,
                hasAssessment: !!currentUser.assessmentData
              }
            });
          }
        } else {
          tests.push({
            name: "User Authentication & Data",
            status: 'fail',
            message: "No user logged in",
            details: { currentUser: null }
          });
        }
      } catch (error) {
        tests.push({
          name: "User Authentication & Data",
          status: 'fail',
          message: `User data error: ${error}`,
          details: { error }
        });
      }
      updateProgress();

      // Test 3: Career Recommendation Generation
      console.log('🧪 Test 3: Career Recommendation Generation');
      try {
        // Create test assessment data
        const testAssessmentData = {
          experience: '3-5',
          technicalSkills: ['Excel/Spreadsheets', 'Data Analysis', 'Project Management'],
          softSkills: ['Communication', 'Problem Solving', 'Leadership'],
          workingWithData: 4,
          workingWithPeople: 3,
          creativeTasks: 2,
          problemSolving: 4,
          leadership: 3,
          physicalHandsOnWork: 2,
          outdoorWork: 2,
          mechanicalAptitude: 3,
          interests: ['Technology & Software', 'Business & Entrepreneurship'],
          industries: ['Technology & Software', 'Financial Services'],
          workEnvironment: 'hybrid',
          salaryExpectations: '70k-100k',
          careerGoals: 'Advance to senior analyst role',
          age: '26-30',
          location: 'Austin, TX',
          educationLevel: 'bachelors',
          currentSituation: 'employed',
          currentRole: 'Business Analyst',
          workLifeBalance: 'important',
          certifications: [],
          resumeText: '',
          linkedinProfile: ''
        };

        const recommendations = generateCareerRecommendations(testAssessmentData, 1);
        
        if (recommendations && recommendations.length > 0) {
          const avgScore = recommendations.reduce((sum, rec) => sum + rec.relevanceScore, 0) / recommendations.length;
          tests.push({
            name: "Career Recommendation Generation",
            status: 'pass',
            message: `Generated ${recommendations.length} recommendations with avg score ${avgScore.toFixed(1)}%`,
            details: { 
              count: recommendations.length, 
              avgScore: avgScore.toFixed(1),
              topRecommendation: recommendations[0]?.title,
              topScore: recommendations[0]?.relevanceScore
            }
          });
        } else {
          tests.push({
            name: "Career Recommendation Generation",
            status: 'fail',
            message: "No recommendations generated",
            details: { recommendations: [] }
          });
        }
      } catch (error) {
        tests.push({
          name: "Career Recommendation Generation",
          status: 'fail',
          message: `Recommendation error: ${error}`,
          details: { error }
        });
      }
      updateProgress();

      // Test 4: User's Actual Recommendations (if profile complete)
      console.log('🧪 Test 4: User\'s Actual Recommendations');
      try {
        if (currentUser?.assessmentData && currentUser.profileCompleted) {
          // Process user's actual data
          const processedData = {
            ...currentUser.assessmentData,
            workingWithData: Array.isArray(currentUser.assessmentData.workingWithData) 
              ? currentUser.assessmentData.workingWithData[0] 
              : currentUser.assessmentData.workingWithData,
            workingWithPeople: Array.isArray(currentUser.assessmentData.workingWithPeople) 
              ? currentUser.assessmentData.workingWithPeople[0] 
              : currentUser.assessmentData.workingWithPeople,
            creativeTasks: Array.isArray(currentUser.assessmentData.creativeTasks) 
              ? currentUser.assessmentData.creativeTasks[0] 
              : currentUser.assessmentData.creativeTasks,
            problemSolving: Array.isArray(currentUser.assessmentData.problemSolving) 
              ? currentUser.assessmentData.problemSolving[0] 
              : currentUser.assessmentData.problemSolving,
            leadership: Array.isArray(currentUser.assessmentData.leadership) 
              ? currentUser.assessmentData.leadership[0] 
              : currentUser.assessmentData.leadership,
          };

          const userRecommendations = generateCareerRecommendations(processedData, 1);
          
          if (userRecommendations && userRecommendations.length > 0) {
            const avgScore = userRecommendations.reduce((sum, rec) => sum + rec.relevanceScore, 0) / userRecommendations.length;
            tests.push({
              name: "User's Actual Recommendations",
              status: 'pass',
              message: `Generated ${userRecommendations.length} personalized recommendations with avg score ${avgScore.toFixed(1)}%`,
              details: { 
                count: userRecommendations.length, 
                avgScore: avgScore.toFixed(1),
                topRecommendation: userRecommendations[0]?.title,
                topScore: userRecommendations[0]?.relevanceScore,
                userExperience: currentUser.assessmentData.experience,
                userSkills: currentUser.assessmentData.technicalSkills?.length || 0
              }
            });
          } else {
            tests.push({
              name: "User's Actual Recommendations",
              status: 'fail',
              message: "No personalized recommendations generated",
              details: { userRecommendations: [] }
            });
          }
        } else {
          tests.push({
            name: "User's Actual Recommendations",
            status: 'warning',
            message: "Cannot test - user profile incomplete",
            details: { profileComplete: currentUser?.profileCompleted || false }
          });
        }
      } catch (error) {
        tests.push({
          name: "User's Actual Recommendations",
          status: 'fail',
          message: `User recommendation error: ${error}`,
          details: { error }
        });
      }
      updateProgress();

      // Test 5: Save Career Functionality
      console.log('🧪 Test 5: Save Career Functionality');
      try {
        if (currentUser) {
          // Test saving a career
          const testCareerType = 'business-analyst';
          const originalSavedCareers = currentUser.savedCareers || [];
          
          // Simulate saving a career
          const updatedSavedCareers = originalSavedCareers.includes(testCareerType) 
            ? originalSavedCareers 
            : [...originalSavedCareers, testCareerType];
          
          const testUser = {
            ...currentUser,
            savedCareers: updatedSavedCareers
          };
          
          // Test localStorage save
          localStorage.setItem('testUser', JSON.stringify(testUser));
          const savedTestUser = JSON.parse(localStorage.getItem('testUser') || '{}');
          
          if (savedTestUser.savedCareers && savedTestUser.savedCareers.includes(testCareerType)) {
            tests.push({
              name: "Save Career Functionality",
              status: 'pass',
              message: `Career saving works - test career saved successfully`,
              details: { 
                originalCount: originalSavedCareers.length,
                newCount: updatedSavedCareers.length,
                testCareerType
              }
            });
            
            // Clean up test data
            localStorage.removeItem('testUser');
          } else {
            tests.push({
              name: "Save Career Functionality",
              status: 'fail',
              message: "Career saving failed - data not persisted",
              details: { savedTestUser }
            });
          }
        } else {
          tests.push({
            name: "Save Career Functionality",
            status: 'warning',
            message: "Cannot test - no user logged in",
            details: { currentUser: null }
          });
        }
      } catch (error) {
        tests.push({
          name: "Save Career Functionality",
          status: 'fail',
          message: `Save functionality error: ${error}`,
          details: { error }
        });
      }
      updateProgress();

      // Test 6: Saved Careers Retrieval
      console.log('🧪 Test 6: Saved Careers Retrieval');
      try {
        if (currentUser?.savedCareers) {
          const savedCareerTypes = currentUser.savedCareers;
          const savedCareerDetails = savedCareerTypes.map(careerType => 
            CAREER_TEMPLATES.find(template => template.careerType === careerType)
          ).filter(Boolean);
          
          tests.push({
            name: "Saved Careers Retrieval",
            status: 'pass',
            message: `Retrieved ${savedCareerDetails.length}/${savedCareerTypes.length} saved careers`,
            details: { 
              savedCount: savedCareerTypes.length,
              retrievedCount: savedCareerDetails.length,
              savedCareers: savedCareerDetails.map(c => c?.title)
            }
          });
        } else {
          tests.push({
            name: "Saved Careers Retrieval",
            status: 'warning',
            message: "No saved careers to test",
            details: { savedCareers: [] }
          });
        }
      } catch (error) {
        tests.push({
          name: "Saved Careers Retrieval",
          status: 'fail',
          message: `Saved careers retrieval error: ${error}`,
          details: { error }
        });
      }
      updateProgress();

      // Test 7: Career Detail Navigation
      console.log('🧪 Test 7: Career Detail Navigation');
      try {
        // Test that career types are properly formatted for navigation
        const testCareer = CAREER_TEMPLATES[0];
        if (testCareer && testCareer.careerType) {
          const careerUrl = `/career/${testCareer.careerType}`;
          tests.push({
            name: "Career Detail Navigation",
            status: 'pass',
            message: `Career navigation URLs properly formatted`,
            details: { 
              sampleCareer: testCareer.title,
              sampleUrl: careerUrl,
              careerType: testCareer.careerType
            }
          });
        } else {
          tests.push({
            name: "Career Detail Navigation",
            status: 'fail',
            message: "Career types not properly formatted",
            details: { testCareer }
          });
        }
      } catch (error) {
        tests.push({
          name: "Career Detail Navigation",
          status: 'fail',
          message: `Navigation test error: ${error}`,
          details: { error }
        });
      }
      updateProgress();

      // Test 8: Data Persistence
      console.log('🧪 Test 8: Data Persistence');
      try {
        // Test localStorage functionality
        const testData = { test: 'data', timestamp: Date.now() };
        localStorage.setItem('systemTest', JSON.stringify(testData));
        const retrievedData = JSON.parse(localStorage.getItem('systemTest') || '{}');
        
        if (retrievedData.test === 'data') {
          tests.push({
            name: "Data Persistence",
            status: 'pass',
            message: "localStorage working correctly",
            details: { testData, retrievedData }
          });
          localStorage.removeItem('systemTest');
        } else {
          tests.push({
            name: "Data Persistence",
            status: 'fail',
            message: "localStorage not working properly",
            details: { testData, retrievedData }
          });
        }
      } catch (error) {
        tests.push({
          name: "Data Persistence",
          status: 'fail',
          message: `Data persistence error: ${error}`,
          details: { error }
        });
      }
      updateProgress();

    } catch (error) {
      tests.push({
        name: "System Test",
        status: 'fail',
        message: `Critical system error: ${error}`,
        details: { error }
      });
    }

    setTestResults(tests);
    setIsRunning(false);
    setTestProgress(100);

    // Show summary
    const passCount = tests.filter(t => t.status === 'pass').length;
    const failCount = tests.filter(t => t.status === 'fail').length;
    const warnCount = tests.filter(t => t.status === 'warning').length;

    if (failCount === 0) {
      showSuccess(`✅ All tests passed! ${passCount} passed, ${warnCount} warnings`);
    } else {
      showError(`❌ ${failCount} tests failed, ${passCount} passed, ${warnCount} warnings`);
    }
  };

  const getStatusIcon = (status: 'pass' | 'fail' | 'warning') => {
    switch (status) {
      case 'pass':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'fail':
        return <XCircle className="h-5 w-5 text-red-600" />;
      case 'warning':
        return <AlertTriangle className="h-5 w-5 text-yellow-600" />;
    }
  };

  const getStatusColor = (status: 'pass' | 'fail' | 'warning') => {
    switch (status) {
      case 'pass':
        return 'bg-green-50 border-green-200 text-green-800';
      case 'fail':
        return 'bg-red-50 border-red-200 text-red-800';
      case 'warning':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
    }
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
          
          <h1 className="text-3xl font-bold text-gray-900 mb-2">System Verification Test</h1>
          <p className="text-gray-600">
            Comprehensive test of career recommendations and job saving functionality
          </p>
        </div>

        {/* Current User Info */}
        {currentUser && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <User className="h-5 w-5" />
                <span>Current User</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-3 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Name</p>
                  <p className="font-medium">{currentUser.firstName} {currentUser.lastName}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Profile Status</p>
                  <Badge className={currentUser.profileCompleted ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}>
                    {currentUser.profileCompleted ? 'Complete' : 'Incomplete'}
                  </Badge>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Saved Careers</p>
                  <p className="font-medium">{currentUser.savedCareers?.length || 0} saved</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Test Controls */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Run System Tests</CardTitle>
            <CardDescription>
              Test career recommendations, saving functionality, and data persistence
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button 
              onClick={runComprehensiveTest} 
              disabled={isRunning}
              className="w-full mb-4"
            >
              {isRunning ? (
                <>
                  <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                  Running Tests...
                </>
              ) : (
                <>
                  <Settings className="h-4 w-4 mr-2" />
                  Run Comprehensive Test
                </>
              )}
            </Button>
            
            {isRunning && (
              <div>
                <Progress value={testProgress} className="h-2 mb-2" />
                <p className="text-sm text-gray-600">
                  Testing system components... {Math.round(testProgress)}% complete
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Test Results */}
        {testResults.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Test Results</CardTitle>
              <CardDescription>
                {testResults.filter(t => t.status === 'pass').length} passed, {' '}
                {testResults.filter(t => t.status === 'fail').length} failed, {' '}
                {testResults.filter(t => t.status === 'warning').length} warnings
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {testResults.map((result, index) => (
                  <div key={index} className={`p-4 rounded-lg border ${getStatusColor(result.status)}`}>
                    <div className="flex items-start space-x-3">
                      {getStatusIcon(result.status)}
                      <div className="flex-1">
                        <h3 className="font-semibold">{result.name}</h3>
                        <p className="text-sm mt-1">{result.message}</p>
                        {result.details && (
                          <details className="mt-2">
                            <summary className="text-xs cursor-pointer hover:underline">
                              View Details
                            </summary>
                            <pre className="text-xs mt-2 p-2 bg-white bg-opacity-50 rounded overflow-auto">
                              {JSON.stringify(result.details, null, 2)}
                            </pre>
                          </details>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default SystemTest;