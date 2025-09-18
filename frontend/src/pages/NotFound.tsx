import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Logo } from '@/components/Logo';
import { useNavigate } from 'react-router-dom';
import { Home, ArrowLeft, Search, AlertCircle } from 'lucide-react';

const NotFound = () => {
  const navigate = useNavigate();

  const handleGoHome = () => {
    navigate('/');
  };

  const handleGoBack = () => {
    navigate(-1);
  };

  const handleGoToDashboard = () => {
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <Logo size="lg" />
            <div className="space-x-4">
              <Button variant="ghost" onClick={handleGoBack}>
                <ArrowLeft className="h-4 w-4 mr-2" />
                Go Back
              </Button>
              <Button onClick={handleGoHome}>
                <Home className="h-4 w-4 mr-2" />
                Home
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex items-center justify-center min-h-[calc(100vh-80px)] p-4">
        <div className="max-w-2xl mx-auto text-center">
          {/* 404 Icon */}
          <div className="mb-8">
            <div className="mx-auto w-24 h-24 bg-red-100 rounded-full flex items-center justify-center mb-6">
              <AlertCircle className="h-12 w-12 text-red-600" />
            </div>
            <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
            <h2 className="text-3xl font-semibold text-gray-700 mb-4">Page Not Found</h2>
            <p className="text-xl text-gray-600 mb-8">
              Oops! The page you're looking for doesn't exist or has been moved.
            </p>
          </div>

          {/* Action Cards */}
          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer" onClick={handleGoHome}>
              <CardHeader>
                <CardTitle className="flex items-center justify-center">
                  <Home className="h-5 w-5 mr-2 text-blue-600" />
                  Go to Homepage
                </CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Return to our main page and explore career discovery features
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow cursor-pointer" onClick={handleGoToDashboard}>
              <CardHeader>
                <CardTitle className="flex items-center justify-center">
                  <Search className="h-5 w-5 mr-2 text-green-600" />
                  Career Dashboard
                </CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Access your personalized career recommendations and insights
                </CardDescription>
              </CardContent>
            </Card>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Quick Links</h3>
            <div className="flex flex-wrap justify-center gap-4">
              <Button variant="outline" onClick={() => navigate('/auth')}>
                Sign In
              </Button>
              <Button variant="outline" onClick={() => navigate('/assessment')}>
                Take Assessment
              </Button>
              <Button variant="outline" onClick={() => navigate('/system-check')}>
                System Check
              </Button>
            </div>
          </div>

          {/* Help Text */}
          <div className="mt-12 p-6 bg-white rounded-lg shadow-sm">
            <h4 className="font-semibold text-gray-900 mb-2">Need Help?</h4>
            <p className="text-gray-600 text-sm">
              If you believe this is an error or you were expecting to find something here, 
              please try going back to the previous page or return to our homepage.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFound;