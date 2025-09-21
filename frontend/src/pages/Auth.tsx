import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ArrowLeft } from "lucide-react";
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
    lastName: ''
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate required fields
    if (!formData.email || !formData.password) {
      showError('Please fill in both email and password');
      return;
    }
    
    try {
      const usersData = localStorage.getItem('users');
      let users = [];
      
      if (usersData) {
        try {
          users = JSON.parse(usersData);
        } catch (parseError) {
          showError('Authentication data corrupted. Please register again.');
          return;
        }
      }

      if (!Array.isArray(users)) {
        users = [];
      }

      const user = users.find((u: any) =>
        u.email && u.email.toLowerCase() === formData.email.toLowerCase() &&
        u.password === formData.password
      );
      
      if (user) {
        localStorage.setItem('currentUser', JSON.stringify(user));
        showSuccess(`Welcome back, ${user.firstName}!`);
        
        if (user.profileCompleted) {
          navigate('/dashboard');
        } else {
          navigate('/assessment');
        }
      } else {
        showError('Invalid email or password. Please check your credentials and try again.');
      }
    } catch (error) {
      showError('An error occurred during login. Please try again.');
    }
  };

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      if (formData.password !== formData.confirmPassword) {
        showError('Passwords do not match');
        return;
      }

      if (formData.password.length < 8) {
        showError('Password must be at least 8 characters');
        return;
      }

      if (!formData.email || !formData.firstName || !formData.lastName) {
        showError('Please fill in all required fields');
        return;
      }

      const usersData = localStorage.getItem('users');
      let users = [];
      
      if (usersData) {
        try {
          users = JSON.parse(usersData);
        } catch (parseError) {
          users = [];
        }
      }

      if (!Array.isArray(users)) {
        users = [];
      }

      const existingUser = users.find((u: any) => 
        u.email && u.email.toLowerCase() === formData.email.toLowerCase()
      );

      if (existingUser) {
        showError('An account with this email already exists. Please sign in instead.');
        return;
      }

      const newUser = {
        id: Date.now().toString(),
        email: formData.email.toLowerCase(),
        password: formData.password,
        firstName: formData.firstName,
        lastName: formData.lastName,
        createdAt: new Date().toISOString(),
        profileCompleted: false
      };

      users.push(newUser);
      localStorage.setItem('users', JSON.stringify(users));
      localStorage.setItem('currentUser', JSON.stringify(newUser));
      
      showSuccess(`Account created successfully! Welcome, ${newUser.firstName}!`);
      navigate('/assessment');
    } catch (error) {
      showError('An error occurred during registration. Please try again.');
    }
  };

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
            <Logo size="lg" />
          </div>
        </div>

        <Tabs defaultValue={defaultMode} className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="login">Sign In</TabsTrigger>
            <TabsTrigger value="register">Sign Up</TabsTrigger>
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
                    <Input
                      id="password"
                      name="password"
                      type="password"
                      placeholder="Enter your password"
                      value={formData.password}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  
                  <Button type="submit" className="w-full">
                    Sign In
                  </Button>
                </form>
                
                <div className="mt-4 text-center">
                  <Button variant="link" className="text-sm">
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
                    <Input
                      id="password"
                      name="password"
                      type="password"
                      placeholder="At least 8 characters, mix of letters and numbers"
                      value={formData.password}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="confirmPassword">Confirm Password</Label>
                    <Input
                      id="confirmPassword"
                      name="confirmPassword"
                      type="password"
                      placeholder="Re-enter your password"
                      value={formData.confirmPassword}
                      onChange={handleInputChange}
                      required
                    />
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
      </div>
    </div>
  );
};

export default Auth;