import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowRight, Users, Target, TrendingUp, Network, FileText, CheckCircle, Compass, Briefcase, Brain, Zap, Star, User, Building2, GraduationCap, Award, Map, Search } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { Logo } from "@/components/Logo";

const Landing = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);
  const [isProfileComplete, setIsProfileComplete] = useState(false);
  const [isNavigating, setIsNavigating] = useState(false);

  // Check user state on component mount
  useEffect(() => {
    try {
      console.log('🏠 Landing page loading...');
      console.log('📍 Current URL:', window.location.href);
      
      const currentUser = localStorage.getItem('currentUser');
      console.log('👤 Raw user data from localStorage:', currentUser);
      
      if (currentUser) {
        try {
          const userData = JSON.parse(currentUser);
          console.log('✅ Parsed user data:', userData);
          setUser(userData);
          
          // Check if profile is complete
          if (userData.assessmentData && userData.profileCompleted) {
            console.log('✅ Profile is complete');
            setIsProfileComplete(true);
          } else {
            console.log('❌ Profile is incomplete');
            setIsProfileComplete(false);
          }
        } catch (parseError) {
          console.error('❌ Error parsing user data:', parseError);
          // Clear corrupted data
          localStorage.removeItem('currentUser');
        }
      } else {
        console.log('❌ No user data found');
      }
    } catch (error) {
      console.error('❌ Error in Landing useEffect:', error);
    }
  }, []);

  // Smart navigation based on user state
  const handleGetStarted = async () => {
    try {
      console.log('🚀 Get Started clicked');
      console.log('👤 User exists:', !!user);
      console.log('✅ Profile complete:', isProfileComplete);
      
      setIsNavigating(true);
      
      // Add small delay for visual feedback
      await new Promise(resolve => setTimeout(resolve, 200));
      
      if (user) {
        if (isProfileComplete) {
          console.log('➡️ Navigating to dashboard (profile complete)');
          navigate('/dashboard');
        } else {
          console.log('➡️ Navigating to assessment (profile incomplete)');
          navigate('/assessment');
        }
      } else {
        console.log('➡️ Navigating to registration (no user)');
        navigate('/auth?mode=register');
      }
    } catch (error) {
      console.error('❌ Error in handleGetStarted:', error);
      // Fallback navigation
      navigate('/auth');
    } finally {
      setIsNavigating(false);
    }
  };

  const handleAssessmentClick = async () => {
    try {
      console.log('📝 Assessment button clicked');
      console.log('👤 User exists:', !!user);
      
      setIsNavigating(true);
      
      // Add small delay for visual feedback
      await new Promise(resolve => setTimeout(resolve, 200));
      
      if (user) {
        console.log('➡️ Navigating to assessment (user logged in)');
        navigate('/assessment');
      } else {
        console.log('➡️ Navigating to registration (no user)');
        navigate('/auth?mode=register');
      }
    } catch (error) {
      console.error('❌ Error in handleAssessmentClick:', error);
      navigate('/auth');
    } finally {
      setIsNavigating(false);
    }
  };

  const handleDashboardClick = async () => {
    try {
      console.log('📊 Dashboard button clicked');
      console.log('👤 User exists:', !!user);
      console.log('✅ Profile complete:', isProfileComplete);
      console.log('➡️ Navigating to dashboard...');
      
      setIsNavigating(true);
      
      // Add small delay for visual feedback
      await new Promise(resolve => setTimeout(resolve, 200));
      
      navigate('/dashboard');
    } catch (error) {
      console.error('❌ Error in handleDashboardClick:', error);
      navigate('/dashboard');
    } finally {
      setIsNavigating(false);
    }
  };

  const handleSignInClick = async () => {
    try {
      console.log('🔐 Sign In button clicked');
      
      setIsNavigating(true);
      
      // Add small delay for visual feedback
      await new Promise(resolve => setTimeout(resolve, 200));
      
      navigate('/auth');
    } catch (error) {
      console.error('❌ Error in handleSignInClick:', error);
      navigate('/auth');
    } finally {
      setIsNavigating(false);
    }
  };

  // Dynamic button text based on user state
  const getMainButtonText = () => {
    try {
      if (user) {
        if (isProfileComplete) {
          return "View My Dashboard";
        } else {
          return "Complete My Assessment";
        }
      } else {
        return "Get AI Recommendations";
      }
    } catch (error) {
      console.error('❌ Error in getMainButtonText:', error);
      return "Get Started";
    }
  };

  const getAssessmentButtonText = () => {
    try {
      if (user) {
        if (isProfileComplete) {
          return "Retake Assessment";
        } else {
          return "Complete Assessment";
        }
      } else {
        return "Assessment";
      }
    } catch (error) {
      console.error('❌ Error in getAssessmentButtonText:', error);
      return "Assessment";
    }
  };

  const features = [
    {
      icon: <Brain className="h-6 w-6" />,
      title: "AI-Powered Assessment & Matching",
      description: "Our intelligent system analyzes your responses to uncover hidden strengths and discovers non-obvious career connections by analyzing thousands of skill-to-career patterns"
    },
    {
      icon: <CheckCircle className="h-6 w-6" />,
      title: "Intelligent Skills Analysis",
      description: "AI-driven gap analysis shows exactly which skills to develop for your target careers with personalized learning paths"
    },
    {
      icon: <Network className="h-6 w-6" />,
      title: "AI-Enhanced Networking",
      description: "Smart recommendations for professional connections and networking strategies tailored to your career goals"
    },
    {
      icon: <FileText className="h-6 w-6" />,
      title: "Personalized AI Reports",
      description: "Comprehensive career reports generated by AI analysis of your unique profile and market opportunities"
    }
  ];

  const testimonials = [
    {
      name: "Emily",
      role: "College Senior",
      quote: "The AI found 3 careers I never considered that perfectly match my psychology and statistics background - connections I never would have made myself!",
      rating: 5
    },
    {
      name: "Ravi",
      role: "Marketing Manager (8 years exp.)",
      quote: "The AI's skills gap analysis was incredibly precise - it showed me exactly what to learn for my UX transition with specific learning paths.",
      rating: 4.8
    },
    {
      name: "Marcus",
      role: "Recent Graduate",
      quote: "The AI discovered career paths for my CS degree that went way beyond 'software developer' - roles I didn't even know existed.",
      rating: 4.9
    },
    {
      name: "Sarah",
      role: "Operations Director (12 years exp.)",
      quote: "The AI identified how my operations experience translated to product management - patterns I couldn't see on my own.",
      rating: 5
    }
  ];

  const renderStars = (rating: number) => {
    try {
      const stars = [];
      const fullStars = Math.floor(rating);
      const hasHalfStar = rating % 1 !== 0;

      // Add full stars
      for (let i = 0; i < fullStars; i++) {
        stars.push(
          <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
        );
      }

      // Add half star if needed
      if (hasHalfStar) {
        stars.push(
          <div key="half" className="relative">
            <Star className="h-4 w-4 text-gray-300" />
            <div className="absolute inset-0 overflow-hidden w-1/2">
              <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
            </div>
          </div>
        );
      }

      // Add empty stars to make 5 total
      const remainingStars = 5 - Math.ceil(rating);
      for (let i = 0; i < remainingStars; i++) {
        stars.push(
          <Star key={`empty-${i}`} className="h-4 w-4 text-gray-300" />
        );
      }

      return stars;
    } catch (error) {
      console.error('❌ Error in renderStars:', error);
      return [<Star key="error" className="h-4 w-4 text-gray-300" />];
    }
  };

  console.log('🎨 Rendering Landing page...');
  console.log('👤 Current user state:', user ? `${user.firstName} ${user.lastName}` : 'No user');
  console.log('✅ Profile complete state:', isProfileComplete);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <div className="flex justify-between items-center">
          <Logo size="lg" />
          <div className="flex space-x-2">
            <Button
              variant="ghost"
              onClick={handleAssessmentClick}
              disabled={isNavigating}
            >
              {isNavigating ? "Loading..." : getAssessmentButtonText()}
            </Button>
            {user ? (
              <Button
                variant="outline"
                onClick={handleDashboardClick}
                disabled={isNavigating}
              >
                {isNavigating ? "Loading..." : "Dashboard"}
              </Button>
            ) : (
              <Button
                variant="outline"
                onClick={handleSignInClick}
                disabled={isNavigating}
              >
                {isNavigating ? "Loading..." : "Sign In"}
              </Button>
            )}
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16 text-center">
        <Badge className="mb-4" variant="secondary">
          <Brain className="h-4 w-4 mr-1" />
          AI-Powered Career Finder
        </Badge>
        
        {/* Dynamic welcome message for logged-in users */}
        {user && (
          <div className="mb-4">
            <p className="text-lg text-blue-600 font-medium">
              Welcome back, {user.firstName}! 
              {isProfileComplete ? ' Ready to explore more career options?' : ' Ready to complete your assessment?'}
            </p>
          </div>
        )}
        
        <h1 className="text-5xl font-bold text-gray-900 mb-6 max-w-4xl mx-auto">
          Find Your Next Career Opportunity
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Our advanced AI analyzes your unique profile to discover personalized recommendations 
          beyond your current role or obvious career options.
        </p>
        <div className="flex justify-center">
          <Button
            size="lg"
            className="text-lg px-8 py-3"
            onClick={handleGetStarted}
            disabled={isNavigating}
          >
            {isNavigating ? "Loading..." : getMainButtonText()}
            {!isNavigating && <ArrowRight className="ml-2 h-5 w-5" />}
          </Button>
        </div>
        <p className="text-sm text-gray-500 mt-4">
          {user ? (
            isProfileComplete ? 
              "Explore new career paths • Update your preferences anytime" :
              "Complete your 5-minute assessment • No credit card required"
          ) : (
            "5-minute AI assessment • No credit card required"
          )}
        </p>
      </section>

      {/* AI Differentiator Section */}
      <section className="container mx-auto px-4 py-12">
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 text-white text-center">
          <div className="flex items-center justify-center mb-4">
            <Zap className="h-8 w-8 mr-2" />
            <h2 className="text-2xl font-bold">Powered by Advanced AI</h2>
          </div>
          <p className="text-lg mb-6 max-w-3xl mx-auto opacity-90">
            Unlike generic career tests, our AI analyzes complex patterns across thousands of career paths,
            skills, and professional profiles to discover personalized recommendations beyond your current role or obvious career options.
          </p>
          <div className="grid md:grid-cols-3 gap-6 text-center">
            <div className="bg-white/20 rounded-xl p-6 backdrop-blur-sm border border-white/20">
              <div className="text-5xl font-bold mb-3 text-white drop-shadow-lg">
                361
              </div>
              <p className="text-base font-semibold mb-3 text-white">Careers in Database</p>
              <p className="text-sm text-white/90 leading-relaxed">
                Spanning 11 major job categories from technology to healthcare to skilled trades
              </p>
            </div>
            <div className="bg-white/20 rounded-xl p-6 backdrop-blur-sm border border-white/20">
              <div className="text-5xl font-bold mb-3 text-white drop-shadow-lg">
                25,270
              </div>
              <p className="text-base font-semibold mb-3 text-white">Data Points Analyzed</p>
              <p className="text-sm text-white/90 leading-relaxed">
                Every recommendation considers 70+ factors including skills, experience, salary, and growth potential
              </p>
            </div>
            <div className="bg-white/20 rounded-xl p-6 backdrop-blur-sm border border-white/20">
              <div className="text-5xl font-bold mb-3 text-white drop-shadow-lg">
                2,166
              </div>
              <p className="text-base font-semibold mb-3 text-white">Skill-Career Connections</p>
              <p className="text-sm text-white/90 leading-relaxed">
                Advanced AI maps thousands of skill combinations across 361 careers to find your perfect match
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            How Our AI Works
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Advanced artificial intelligence analyzes your profile and provides insights that human career counselors might miss
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-2 gap-6">
          {features.map((feature, index) => (
            <Card key={index} className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center text-blue-600 mb-4">
                  {feature.icon}
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Professional Personas Section */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-6">
              Designed for Every Career Stage
            </h2>
            <p className="text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
              Whether you're launching your career or pivoting after years of experience, 
              our AI provides strategic guidance tailored to your professional journey.
            </p>
          </div>
          
          <div className="max-w-7xl mx-auto">
            <div className="grid lg:grid-cols-2 gap-12 items-stretch">
              {/* Early Career Professionals */}
              <div className="bg-white border-2 border-blue-200 rounded-xl shadow-lg hover:shadow-xl hover:border-blue-300 transition-all duration-300 flex flex-col">
                <div className="p-8 flex-1 flex flex-col">
                  {/* Header */}
                  <div className="flex items-start mb-8">
                    <div className="w-16 h-16 bg-blue-600 rounded-xl flex items-center justify-center mr-6 shadow-sm">
                      <Compass className="h-8 w-8 text-white" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold text-gray-900 mb-2">Early Career Professionals</h3>
                      <div className="flex flex-wrap gap-2 mb-4">
                        <Badge variant="outline" className="text-xs font-medium">Students</Badge>
                        <Badge variant="outline" className="text-xs font-medium">Recent Graduates</Badge>
                        <Badge variant="outline" className="text-xs font-medium">Career Starters</Badge>
                        <Badge variant="outline" className="text-xs font-medium">Trade School</Badge>
                      </div>
                    </div>
                  </div>
                  
                  {/* Description */}
                  <div className="mb-8">
                    <p className="text-gray-700 text-lg leading-relaxed">
                      Starting your career or uncertain about direction? Our AI discovers opportunities that align with your 
                      education, interests, and natural strengths before you get locked into a narrow path.
                    </p>
                  </div>
                  
                  {/* Benefits */}
                  <div className="space-y-4 mb-8 flex-1">
                    {[
                      "AI explores careers beyond obvious major-related jobs",
                      "Understand what skills employers actually want",
                      "Build your network from day one",
                      "Make informed decisions about your first career moves"
                    ].map((benefit, index) => (
                      <div key={index} className="flex items-start space-x-3">
                        <div className="w-5 h-5 bg-blue-600 rounded-full flex items-center justify-center mt-0.5 flex-shrink-0">
                          <CheckCircle className="h-3 w-3 text-white" />
                        </div>
                        <p className="text-gray-700 font-medium">{benefit}</p>
                      </div>
                    ))}
                  </div>
                  
                  {/* Stats */}
                  <div className="bg-gray-50 rounded-lg p-6 border border-gray-100 mt-auto">
                    <div className="grid grid-cols-3 gap-4 text-center">
                      <div>
                        <div className="text-2xl font-bold text-blue-600 mb-1">0-2</div>
                        <p className="text-sm text-gray-600 font-medium">Years Experience</p>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-blue-600 mb-1">85%</div>
                        <p className="text-sm text-gray-600 font-medium">Find New Paths</p>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-blue-600 mb-1">3-6</div>
                        <p className="text-sm text-gray-600 font-medium">Months to Ready</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Experienced Professionals */}
              <div className="bg-white border-2 border-slate-300 rounded-xl shadow-lg hover:shadow-xl hover:border-slate-400 transition-all duration-300 flex flex-col">
                <div className="p-8 flex-1 flex flex-col">
                  {/* Header */}
                  <div className="flex items-start mb-8">
                    <div className="w-16 h-16 bg-slate-700 rounded-xl flex items-center justify-center mr-6 shadow-sm">
                      <Building2 className="h-8 w-8 text-white" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold text-gray-900 mb-2">Experienced Professionals</h3>
                      <div className="flex flex-wrap gap-2 mb-4">
                        <Badge variant="outline" className="text-xs font-medium">Mid-Career</Badge>
                        <Badge variant="outline" className="text-xs font-medium">Career Switchers</Badge>
                        <Badge variant="outline" className="text-xs font-medium">Senior Professionals</Badge>
                        <Badge variant="outline" className="text-xs font-medium">Leadership</Badge>
                      </div>
                    </div>
                  </div>
                  
                  {/* Description */}
                  <div className="mb-8">
                    <p className="text-gray-700 text-lg leading-relaxed">
                      Ready for change or feeling stuck? Our AI identifies how your years of experience translate 
                      to exciting new opportunities you may never have considered.
                    </p>
                  </div>
                  
                  {/* Benefits */}
                  <div className="space-y-4 mb-8 flex-1">
                    {[
                      "AI leverages your skills in new industries and functions",
                      "Find transition pathways that build on your experience",
                      "Connect with professionals in your target fields",
                      "Get AI-generated learning plans for skill gaps"
                    ].map((benefit, index) => (
                      <div key={index} className="flex items-start space-x-3">
                        <div className="w-5 h-5 bg-slate-700 rounded-full flex items-center justify-center mt-0.5 flex-shrink-0">
                          <CheckCircle className="h-3 w-3 text-white" />
                        </div>
                        <p className="text-gray-700 font-medium">{benefit}</p>
                      </div>
                    ))}
                  </div>
                  
                  {/* Stats */}
                  <div className="bg-gray-50 rounded-lg p-6 border border-gray-100 mt-auto">
                    <div className="grid grid-cols-3 gap-4 text-center">
                      <div>
                        <div className="text-2xl font-bold text-slate-700 mb-1">3+</div>
                        <p className="text-sm text-gray-600 font-medium">Years Experience</p>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-slate-700 mb-1">92%</div>
                        <p className="text-sm text-gray-600 font-medium">Discover Options</p>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-slate-700 mb-1">1-4</div>
                        <p className="text-sm text-gray-600 font-medium">Months to Pivot</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Job Families Coverage Section */}
      <section className="bg-gray-50 py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Comprehensive Career Coverage
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              Our AI-powered system covers <span className="font-semibold text-blue-600">361 careers</span> across major industries,
              with more being added regularly to ensure comprehensive career exploration.
            </p>
          </div>
          
          <div className="max-w-6xl mx-auto">
            {/* Currently Supported - Full Width */}
            <Card className="p-6 border-2 border-green-200 bg-green-50">
              <CardHeader className="pb-6">
                <div className="flex items-center justify-center space-x-2 mb-2">
                  <CheckCircle className="h-6 w-6 text-green-600" />
                  <CardTitle className="text-2xl text-green-800">Supported Career Categories and Careers</CardTitle>
                </div>
              </CardHeader>
              <CardContent className="pt-0">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="flex items-center space-x-3">
                    <Badge variant="outline" className="bg-white border-green-300 text-green-700 text-base px-3 py-1">
                      <Brain className="h-4 w-4 mr-1" />
                      Technology & Engineering
                    </Badge>
                    <span className="text-base text-green-600 font-semibold">57 careers</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Badge variant="outline" className="bg-white border-green-300 text-green-700 text-base px-3 py-1">
                      <User className="h-4 w-4 mr-1" />
                      Healthcare & Medical
                    </Badge>
                    <span className="text-base text-green-600 font-semibold">40 careers</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Badge variant="outline" className="bg-white border-green-300 text-green-700 text-base px-3 py-1">
                      <Building2 className="h-4 w-4 mr-1" />
                      Skilled Trades & Construction
                    </Badge>
                    <span className="text-base text-green-600 font-semibold">40 careers</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Badge variant="outline" className="bg-white border-green-300 text-green-700 text-base px-3 py-1">
                      <GraduationCap className="h-4 w-4 mr-1" />
                      Education & Training
                    </Badge>
                    <span className="text-base text-green-600 font-semibold">40 careers</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Badge variant="outline" className="bg-white border-green-300 text-green-700 text-base px-3 py-1">
                      <TrendingUp className="h-4 w-4 mr-1" />
                      Business & Finance
                    </Badge>
                    <span className="text-base text-green-600 font-semibold">44 careers</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Badge variant="outline" className="bg-white border-green-300 text-green-700 text-base px-3 py-1">
                      <Award className="h-4 w-4 mr-1" />
                      Legal & Law
                    </Badge>
                    <span className="text-base text-green-600 font-semibold">19 careers</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Badge variant="outline" className="bg-white border-green-300 text-green-700 text-base px-3 py-1">
                      <Briefcase className="h-4 w-4 mr-1" />
                      Creative & Arts
                    </Badge>
                    <span className="text-base text-green-600 font-semibold">26 careers</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Badge variant="outline" className="bg-white border-green-300 text-green-700 text-base px-3 py-1">
                      <Users className="h-4 w-4 mr-1" />
                      Public Service & Government
                    </Badge>
                    <span className="text-base text-green-600 font-semibold">30 careers</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Badge variant="outline" className="bg-white border-green-300 text-green-700 text-base px-3 py-1">
                      <Building2 className="h-4 w-4 mr-1" />
                      Hospitality & Service
                    </Badge>
                    <span className="text-base text-green-600 font-semibold">21 careers</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Badge variant="outline" className="bg-white border-green-300 text-green-700 text-base px-3 py-1">
                      <Zap className="h-4 w-4 mr-1" />
                      Manufacturing & Industrial
                    </Badge>
                    <span className="text-base text-green-600 font-semibold">22 careers</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Badge variant="outline" className="bg-white border-green-300 text-green-700 text-base px-3 py-1">
                      <Map className="h-4 w-4 mr-1" />
                      Agriculture & Environment
                    </Badge>
                    <span className="text-base text-green-600 font-semibold">22 careers</span>
                  </div>
                </div>
              </CardContent>
            </Card>
            
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Success Stories from Our AI-Powered Platform
          </h2>
        </div>
        
        <div className="grid md:grid-cols-2 gap-6 max-w-6xl mx-auto">
          {testimonials.map((testimonial, index) => (
            <Card key={index} className="p-6">
              <CardContent className="pt-0">
                <p className="text-lg text-gray-700 mb-4 italic">
                  "{testimonial.quote}"
                </p>
                
                {/* Star Rating */}
                <div className="flex items-center space-x-1 mb-4">
                  {renderStars(testimonial.rating)}
                  <span className="text-sm text-gray-600 ml-2">{testimonial.rating}/5</span>
                </div>
                
                <div className="flex items-center">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                    <span className="text-blue-600 font-semibold">
                      {testimonial.name[0]}
                    </span>
                  </div>
                  <div>
                    <p className="font-semibold">{testimonial.name}</p>
                    <p className="text-sm text-gray-600">{testimonial.role}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">
            Ready to Let AI Discover Your Next Career Move?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Join professionals at every career stage who have found their perfect next step with AI-powered insights
          </p>
          <Button
            size="lg"
            variant="secondary"
            className="text-lg px-8 py-3"
            onClick={handleGetStarted}
            disabled={isNavigating}
          >
            {isNavigating ? "Loading..." : getMainButtonText()}
            {!isNavigating && <ArrowRight className="ml-2 h-5 w-5" />}
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8">
        <div className="container mx-auto px-4 text-center">
          <div className="flex justify-center mb-4">
            <Logo size="md" variant="dark" />
          </div>
          <p className="text-gray-400">
            AI-powered career discovery for professionals at every stage
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;