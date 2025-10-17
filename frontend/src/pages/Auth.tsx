import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ArrowLeft, Eye, EyeOff } from "lucide-react";
import { showSuccess, showError } from "@/utils/toast";
import { Logo } from "@/components/Logo";

const Auth = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const defaultMode = searchParams.get('mode') || 'login';
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    resetToken: '',
    newPassword: '',
    confirmNewPassword: ''
  });

  const [authMode, setAuthMode] = useState<'login' | 'register' | 'forgot-password' | 'reset-password'>('login');
  const [resetToken, setResetToken] = useState<string>('');
  const [showPassword, setShowPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.email || !formData.password) {
      showError('Please fill in both email and password');
      return;
    }
    try {
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          username: formData.email,
          password: formData.password,
        }),
      });
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        showSuccess('Logged in successfully!');
        
        // Check if user has completed assessment and redirect appropriately
        if (data.assessment_completed === false) {
          showSuccess('Please complete your assessment to get personalized recommendations.');
          navigate('/assessment');
        } else {
          navigate('/dashboard');
        }
      } else {
        showError('Invalid email or password.');
      }
    } catch (error) {
      showError('An error occurred during login.');
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      showError('Passwords do not match');
      return;
    }
    try {
      const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
        }),
      });
      if (response.ok) {
        const data = await response.json();
        
        // Registration now returns JWT tokens directly
        if (data.access_token) {
          localStorage.setItem('token', data.access_token);
          showSuccess('Registration successful! Welcome! Redirecting to your assessment...');
          
          // New users always need to complete assessment (assessment_completed should be false)
          if (data.assessment_completed === false) {
            navigate('/assessment');
          } else {
            // This shouldn't happen for new registrations, but handle it gracefully
            navigate('/dashboard');
          }
        } else {
          showError('Registration successful, but no access token received. Please log in manually.');
        }
      } else {
        const errorData = await response.json();
        showError(errorData.detail || 'Registration failed.');
      }
    } catch (error) {
      showError('An error occurred during registration.');
    }
  };

  const handleForgotPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.email) {
      showError('Please enter your email address');
      return;
    }

    try {
      const response = await fetch('/api/v1/auth/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: formData.email,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        showSuccess('Password reset instructions sent! Check the token below.');
        
        // Store the reset token for testing (since no email service)
        if (data.reset_token) {
          setResetToken(data.reset_token);
          setAuthMode('reset-password');
        }
      } else {
        const errorData = await response.json();
        showError(errorData.detail || 'Failed to send reset instructions');
      }
    } catch (error) {
      showError('An error occurred while sending reset instructions');
    }
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.resetToken) {
      showError('Please enter the reset token');
      return;
    }
    
    if (!formData.newPassword) {
      showError('Please enter a new password');
      return;
    }
    
    if (formData.newPassword !== formData.confirmNewPassword) {
      showError('New passwords do not match');
      return;
    }

    if (formData.newPassword.length < 8) {
      showError('Password must be at least 8 characters long');
      return;
    }

    try {
      const response = await fetch('/api/v1/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token: formData.resetToken,
          new_password: formData.newPassword,
        }),
      });

      if (response.ok) {
        showSuccess('Password reset successfully! You can now log in with your new password.');
        setAuthMode('login');
        setFormData({
          email: formData.email, // Keep email for convenience
          password: '',
          confirmPassword: '',
          firstName: '',
          lastName: '',
          resetToken: '',
          newPassword: '',
          confirmNewPassword: ''
        });
        setResetToken('');
      } else {
        const errorData = await response.json();
        showError(errorData.detail || 'Failed to reset password');
      }
    } catch (error) {
      showError('An error occurred while resetting password');
    }
  };

  const renderLoginRegisterTabs = () => (
    <Tabs defaultValue={authMode === 'register' ? 'register' : 'login'} className="w-full">
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="login" onClick={() => setAuthMode('login')}>Sign In</TabsTrigger>
        <TabsTrigger value="register" onClick={() => setAuthMode('register')}>Sign Up</TabsTrigger>
      </TabsList>
      
      <TabsContent value="login">
        <Card>
          <CardHeader>
            <CardTitle>Welcome Back</CardTitle>
            <CardDescription>
              Sign in to continue your career discovery journey
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="Enter your email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Enter your password"
                    value={formData.password}
                    onChange={handleInputChange}
                    required
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </div>
              
              <Button type="submit" className="w-full">
                Sign In
              </Button>
            </form>
            
            <div className="mt-4 text-center">
              <Button
                variant="link"
                className="text-sm"
                onClick={() => setAuthMode('forgot-password')}
              >
                Forgot your password?
              </Button>
            </div>
          </CardContent>
        </Card>
      </TabsContent>
      
      <TabsContent value="register">
        <Card>
          <CardHeader>
            <CardTitle>Create Account</CardTitle>
            <CardDescription>
              Start your personalized career discovery journey
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleRegister} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="firstName">First Name</Label>
                  <Input
                    id="firstName"
                    name="firstName"
                    placeholder="First name"
                    value={formData.firstName}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="lastName">Last Name</Label>
                  <Input
                    id="lastName"
                    name="lastName"
                    placeholder="Last name"
                    value={formData.lastName}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="Enter your email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="At least 8 characters, mix of letters and numbers"
                    value={formData.password}
                    onChange={handleInputChange}
                    required
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Confirm Password</Label>
                <div className="relative">
                  <Input
                    id="confirmPassword"
                    name="confirmPassword"
                    type={showConfirmPassword ? "text" : "password"}
                    placeholder="Re-enter your password"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    required
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  >
                    {showConfirmPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </div>
              
              <Button type="submit" className="w-full">
                Create Account
              </Button>
            </form>
            
            <div className="mt-4 text-center text-sm text-gray-600">
              By creating an account, you agree to our privacy policy and terms of service.
            </div>
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>
  );

  const renderForgotPasswordForm = () => (
    <Card>
      <CardHeader>
        <CardTitle>Reset Password</CardTitle>
        <CardDescription>
          Enter your email address and we'll send you a reset token
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleForgotPassword} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="Enter your email address"
              value={formData.email}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <Button type="submit" className="w-full">
            Send Reset Token
          </Button>
        </form>
        
        <div className="mt-4 text-center">
          <Button
            variant="link"
            className="text-sm"
            onClick={() => setAuthMode('login')}
          >
            Back to Sign In
          </Button>
        </div>
      </CardContent>
    </Card>
  );

  const renderResetPasswordForm = () => (
    <Card>
      <CardHeader>
        <CardTitle>Set New Password</CardTitle>
        <CardDescription>
          Enter the reset token and your new password
        </CardDescription>
      </CardHeader>
      <CardContent>
        {resetToken && (
          <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
            <p className="text-sm font-medium text-blue-800 mb-1">Reset Token (for testing):</p>
            <p className="text-xs font-mono text-blue-600 break-all">{resetToken}</p>
            <p className="text-xs text-blue-600 mt-1">Copy this token to the field below</p>
          </div>
        )}
        
        <form onSubmit={handleResetPassword} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="resetToken">Reset Token</Label>
            <Input
              id="resetToken"
              name="resetToken"
              type="text"
              placeholder="Enter the reset token"
              value={formData.resetToken}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="newPassword">New Password</Label>
            <div className="relative">
              <Input
                id="newPassword"
                name="newPassword"
                type={showNewPassword ? "text" : "password"}
                placeholder="Enter your new password (min 8 characters)"
                value={formData.newPassword}
                onChange={handleInputChange}
                required
              />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                onClick={() => setShowNewPassword(!showNewPassword)}
              >
                {showNewPassword ? (
                  <EyeOff className="h-4 w-4" />
                ) : (
                  <Eye className="h-4 w-4" />
                )}
              </Button>
            </div>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="confirmNewPassword">Confirm New Password</Label>
            <div className="relative">
              <Input
                id="confirmNewPassword"
                name="confirmNewPassword"
                type={showConfirmPassword ? "text" : "password"}
                placeholder="Re-enter your new password"
                value={formData.confirmNewPassword}
                onChange={handleInputChange}
                required
              />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              >
                {showConfirmPassword ? (
                  <EyeOff className="h-4 w-4" />
                ) : (
                  <Eye className="h-4 w-4" />
                )}
              </Button>
            </div>
          </div>
          
          <Button type="submit" className="w-full">
            Reset Password
          </Button>
        </form>
        
        <div className="mt-4 text-center">
          <Button
            variant="link"
            className="text-sm"
            onClick={() => setAuthMode('login')}
          >
            Back to Sign In
          </Button>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Button 
            variant="ghost" 
            className="mb-4"
            onClick={() => navigate('/')}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Home
          </Button>
          
          <div className="flex justify-center mb-4">
            <button
              onClick={() => navigate('/')}
              className="transition-opacity hover:opacity-80 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-lg"
              aria-label="Go to home page"
            >
              <Logo size="lg" />
            </button>
          </div>
        </div>

        {(authMode === 'login' || authMode === 'register') && renderLoginRegisterTabs()}
        {authMode === 'forgot-password' && renderForgotPasswordForm()}
        {authMode === 'reset-password' && renderResetPasswordForm()}
      </div>
    </div>
  );
};

export default Auth;