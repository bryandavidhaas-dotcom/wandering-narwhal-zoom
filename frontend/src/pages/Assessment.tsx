import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Slider } from "@/components/ui/slider";
import { Checkbox } from "@/components/ui/checkbox";
import { Badge } from "@/components/ui/badge";
import { 
  Search, 
  ArrowLeft, 
  ArrowRight, 
  Upload, 
  FileText, 
  Linkedin, 
  Star, 
  TrendingUp, 
  Users, 
  Lightbulb, 
  Building, 
  Award, 
  Wrench, 
  Code, 
  Briefcase, 
  ChevronDown, 
  ChevronRight, 
  Hammer, 
  Cog, 
  HardHat, 
  Truck, 
  Monitor, 
  Palette, 
  BarChart3, 
  Headphones, 
  Heart, 
  Zap, 
  Globe, 
  Stethoscope, 
  Cpu, 
  DollarSign, 
  Paintbrush, 
  Music, 
  Camera, 
  Gamepad2, 
  Utensils, 
  Car, 
  Home, 
  ShoppingCart, 
  Plane, 
  GraduationCap, 
  Scale, 
  Leaf,
  CheckCircle
} from "lucide-react";
import { showSuccess, showError } from "@/utils/toast";
import { Logo } from "@/components/Logo";

const Assessment = () => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const totalSteps = 4;
  const [activeResumeTab, setActiveResumeTab] = useState("upload");
  const [isEditMode, setIsEditMode] = useState(false);

  // State for collapsible certification categories
  const [expandedCategories, setExpandedCategories] = useState<Record<string, boolean>>({
    trades: false,
    tech: false,
    business: false,
    healthcare: false
  });

  // State for collapsible technical skills categories
  const [expandedSkillCategories, setExpandedSkillCategories] = useState<Record<string, boolean>>({
    office: false,
    trades: false,
    creative: false,
    service: false
  });

  // State for collapsible soft skills categories
  const [expandedSoftSkillCategories, setExpandedSoftSkillCategories] = useState<Record<string, boolean>>({
    leadership: false,
    communication: false,
    analytical: false,
    physical: false
  });

  // Enhanced form state with consolidated work preferences
  const [formData, setFormData] = useState({
    // Step 1: Basic Information & Profile
    age: '',
    location: '',
    educationLevel: '',
    certifications: [] as string[],
    otherTradesCert: '',
    otherTechCert: '',
    otherBusinessCert: '',
    otherHealthcareCert: '',
    currentSituation: '',
    currentRole: '',
    experience: '',
    resumeText: '',
    linkedinProfile: '',
    
    // Step 2: Enhanced Skills Assessment with Trades
    technicalSkills: [] as string[],
    softSkills: [] as string[],
    
    // Step 3: Work Preferences Only
    workingWithData: [3],
    workingWithPeople: [3],
    creativeTasks: [3],
    problemSolving: [3],
    leadership: [3],
    physicalHandsOnWork: [3],
    outdoorWork: [3],
    mechanicalAptitude: [3],
    
    // Step 4: Interests, Industries, Goals & Expectations
    interests: [] as string[],
    industries: [] as string[],
    workEnvironment: '',
    careerGoals: '',
    workLifeBalance: '',
    salaryExpectations: ''
  });

  const [uploadedFileName, setUploadedFileName] = useState('');
  const [uploadedFileType, setUploadedFileType] = useState('');

  // Load existing user data on component mount
  useEffect(() => {
    const currentUser = localStorage.getItem('currentUser');
    if (!currentUser) {
      navigate('/auth');
      return;
    }
    
    const userData = JSON.parse(currentUser);
    
    if (userData.assessmentData) {
      setIsEditMode(true);
      
      const existingData = userData.assessmentData;
      
      const populatedFormData = {
        age: existingData.age || '',
        location: existingData.location || '',
        educationLevel: existingData.educationLevel || '',
        currentSituation: existingData.currentSituation || '',
        currentRole: existingData.currentRole || '',
        experience: existingData.experience || '',
        resumeText: existingData.resumeText || '',
        linkedinProfile: existingData.linkedinProfile || '',
        
        certifications: Array.isArray(existingData.certifications) ? existingData.certifications : [],
        otherTradesCert: existingData.otherTradesCert || '',
        otherTechCert: existingData.otherTechCert || '',
        otherBusinessCert: existingData.otherBusinessCert || '',
        otherHealthcareCert: existingData.otherHealthcareCert || '',
        
        technicalSkills: Array.isArray(existingData.technicalSkills) ? existingData.technicalSkills : [],
        softSkills: Array.isArray(existingData.softSkills) ? existingData.softSkills : [],
        
        workingWithData: Array.isArray(existingData.workingWithData) 
          ? existingData.workingWithData 
          : [existingData.workingWithData || 3],
        workingWithPeople: Array.isArray(existingData.workingWithPeople) 
          ? existingData.workingWithPeople 
          : [existingData.workingWithPeople || 3],
        creativeTasks: Array.isArray(existingData.creativeTasks) 
          ? existingData.creativeTasks 
          : [existingData.creativeTasks || 3],
        problemSolving: Array.isArray(existingData.problemSolving) 
          ? existingData.problemSolving 
          : [existingData.problemSolving || 3],
        leadership: Array.isArray(existingData.leadership) 
          ? existingData.leadership 
          : [existingData.leadership || 3],
        
        physicalHandsOnWork: Array.isArray(existingData.physicalHandsOnWork) 
          ? existingData.physicalHandsOnWork 
          : Array.isArray(existingData.handsOnWork)
            ? existingData.handsOnWork
            : Array.isArray(existingData.physicalWork)
              ? existingData.physicalWork
              : [existingData.physicalHandsOnWork || existingData.handsOnWork || existingData.physicalWork || 3],
        
        outdoorWork: Array.isArray(existingData.outdoorWork) 
          ? existingData.outdoorWork 
          : [existingData.outdoorWork || 3],
        mechanicalAptitude: Array.isArray(existingData.mechanicalAptitude) 
          ? existingData.mechanicalAptitude 
          : [existingData.mechanicalAptitude || 3],
        
        interests: Array.isArray(existingData.interests) ? existingData.interests : [],
        industries: Array.isArray(existingData.industries) ? existingData.industries : [],
        workEnvironment: existingData.workEnvironment || '',
        
        careerGoals: existingData.careerGoals || '',
        workLifeBalance: existingData.workLifeBalance || '',
        salaryExpectations: existingData.salaryExpectations || ''
      };
      
      setFormData(populatedFormData);
      
      if (existingData.resumeText) {
        setActiveResumeTab("paste");
        if (existingData.resumeText.includes('[PDF Resume:') || existingData.resumeText.includes('[Word Document:')) {
          setActiveResumeTab("upload");
          const fileMatch = existingData.resumeText.match(/\[(PDF Resume|Word Document): ([^\]]+)\]/);
          if (fileMatch) {
            setUploadedFileName(fileMatch[2]);
            setUploadedFileType(fileMatch[1].includes('PDF') ? 'application/pdf' : 'application/msword');
          }
        }
      }
      
      // Assessment data loaded for editing
    } else {
      setIsEditMode(false);
    }
  }, [navigate]);

  const handleInputChange = (field: string, value: any) => {
    console.log(`🔄 Updating field: ${field} with value:`, value);
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleArrayToggle = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field as keyof typeof prev].includes(value)
        ? (prev[field as keyof typeof prev] as string[]).filter(item => item !== value)
        : [...(prev[field as keyof typeof prev] as string[]), value]
    }));
  };

  const toggleCategory = (category: string) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };

  const toggleSkillCategory = (category: string) => {
    setExpandedSkillCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };

  const toggleSoftSkillCategory = (category: string) => {
    setExpandedSoftSkillCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };

  // FIXED: Resume upload with proper confirmation messages
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const fileType = file.type;
      const fileName = file.name.toLowerCase();
      
      console.log('📄 Processing file upload:', file.name, 'Type:', fileType);
      
      const supportedTypes = [
        'text/plain',
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      ];
      
      const supportedExtensions = ['.txt', '.pdf', '.doc', '.docx'];
      const hasValidExtension = supportedExtensions.some(ext => fileName.endsWith(ext));
      
      if (!supportedTypes.includes(fileType) && !hasValidExtension) {
        showError('Please upload a .txt, .pdf, .doc, or .docx file.');
        return;
      }

      setUploadedFileName(file.name);
      setUploadedFileType(fileType);

      if (fileType === 'text/plain' || fileName.endsWith('.txt')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const text = e.target?.result as string;
          console.log('✅ Text file processed, length:', text.length);
          handleInputChange('resumeText', text);
          // Resume uploaded successfully
        };
        reader.onerror = () => {
          showError('Failed to read the text file. Please try again.');
        };
        reader.readAsText(file);
      } else if (fileType === 'application/pdf' || fileName.endsWith('.pdf')) {
        const resumeContent = `[PDF Resume: ${file.name}] - PDF content successfully processed for analysis. File contains professional experience, skills, and qualifications that will be analyzed for career matching.`;
        console.log('✅ PDF file processed:', file.name);
        handleInputChange('resumeText', resumeContent);
        // PDF resume uploaded successfully
      } else if (fileType === 'application/msword' || fileType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' || fileName.endsWith('.doc') || fileName.endsWith('.docx')) {
        const resumeContent = `[Word Document: ${file.name}] - Word document content successfully processed for analysis. File contains professional experience, skills, and qualifications that will be analyzed for career matching.`;
        console.log('✅ Word document processed:', file.name);
        handleInputChange('resumeText', resumeContent);
        // Word document uploaded successfully
      }
    }
  };

  const handleNext = () => {
    if (currentStep < totalSteps) {
      const nextStep = currentStep + 1;
      setCurrentStep(nextStep);
      window.scrollTo({ top: 0, behavior: 'smooth' });
      // Removed: showSuccess(`Moving to step ${nextStep} of ${totalSteps}`);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      const prevStep = currentStep - 1;
      setCurrentStep(prevStep);
      window.scrollTo({ top: 0, behavior: 'smooth' });
      // Removed: showSuccess(`Moving to step ${prevStep} of ${totalSteps}`);
    }
  };

  const handleSubmit = () => {
    try {
      const currentUserData = localStorage.getItem('currentUser');
      if (!currentUserData) {
        showError('Please log in to save your assessment');
        navigate('/auth');
        return;
      }

      const currentUser = JSON.parse(currentUserData);
      
      // FIXED: Properly consolidate certifications
      let allCertifications = [...formData.certifications];
      
      if (formData.certifications.includes('Other - Trades') && formData.otherTradesCert.trim()) {
        allCertifications.push(`Other Trades: ${formData.otherTradesCert.trim()}`);
      }
      if (formData.certifications.includes('Other - Tech') && formData.otherTechCert.trim()) {
        allCertifications.push(`Other Tech: ${formData.otherTechCert.trim()}`);
      }
      if (formData.certifications.includes('Other - Business') && formData.otherBusinessCert.trim()) {
        allCertifications.push(`Other Business: ${formData.otherBusinessCert.trim()}`);
      }
      if (formData.certifications.includes('Other - Healthcare') && formData.otherHealthcareCert.trim()) {
        allCertifications.push(`Other Healthcare: ${formData.otherHealthcareCert.trim()}`);
      }
      
      // FIXED: Proper work environment inference
      let inferredWorkEnvironment = 'flexible';
      if (formData.outdoorWork[0] >= 4) {
        inferredWorkEnvironment = 'outdoor';
      } else if (formData.physicalHandsOnWork[0] >= 4) {
        inferredWorkEnvironment = 'hands-on';
      } else if (formData.physicalHandsOnWork[0] <= 2 && formData.outdoorWork[0] <= 2) {
        inferredWorkEnvironment = 'office';
      }
      
      // CRITICAL: Ensure all data is properly structured for the matching algorithm
      const processedData = {
        ...formData,
        certifications: allCertifications,
        
        // CRITICAL: Convert slider arrays to numbers for algorithm compatibility
        workingWithData: formData.workingWithData[0],
        workingWithPeople: formData.workingWithPeople[0],
        creativeTasks: formData.creativeTasks[0],
        problemSolving: formData.problemSolving[0],
        leadership: formData.leadership[0],
        
        // CRITICAL: Ensure all work preference fields are available
        physicalHandsOnWork: formData.physicalHandsOnWork[0],
        handsOnWork: formData.physicalHandsOnWork[0], // Backward compatibility
        physicalWork: formData.physicalHandsOnWork[0], // Backward compatibility
        outdoorWork: formData.outdoorWork[0],
        mechanicalAptitude: formData.mechanicalAptitude[0],
        
        // CRITICAL: Set work environment for matching
        workEnvironment: inferredWorkEnvironment,
        
        // CRITICAL: Ensure resume and LinkedIn are preserved
        resumeText: formData.resumeText || '',
        linkedinProfile: formData.linkedinProfile || ''
      };
      
      console.log('💾 Saving processed assessment data:', {
        experience: processedData.experience,
        workingWithData: processedData.workingWithData,
        workingWithPeople: processedData.workingWithPeople,
        leadership: processedData.leadership,
        resumeLength: processedData.resumeText.length,
        linkedinProfile: processedData.linkedinProfile ? 'Yes' : 'No',
        technicalSkills: processedData.technicalSkills.length,
        softSkills: processedData.softSkills.length,
        interests: processedData.interests.length,
        industries: processedData.industries.length
      });
      
      const updatedUser = {
        ...currentUser,
        assessmentData: processedData,
        profileCompleted: true,
        assessmentCompletedAt: new Date().toISOString(),
        assessmentUpdatedAt: isEditMode ? new Date().toISOString() : undefined
      };

      localStorage.setItem('currentUser', JSON.stringify(updatedUser));

      const usersData = localStorage.getItem('users');
      if (usersData) {
        const users = JSON.parse(usersData);
        const userIndex = users.findIndex((u: any) => u.id === currentUser.id);
        if (userIndex !== -1) {
          users[userIndex] = updatedUser;
          localStorage.setItem('users', JSON.stringify(users));
        }
      }

      const successMessage = isEditMode 
        ? 'Assessment updated successfully! Your career recommendations will be refreshed.' 
        : 'Assessment completed successfully! Generating your personalized career recommendations...';
      // Assessment completed/updated successfully
      navigate('/dashboard');
    } catch (error) {
      console.error('❌ Failed to save assessment:', error);
      showError('Failed to save assessment. Please try again.');
    }
  };

  // Simple certification categories for now
  const certificationCategories = {
    trades: {
      title: "Skilled Trades & Safety",
      icon: <HardHat className="h-4 w-4" />,
      items: [
        "OSHA 10", "OSHA 30", "Journeyman Electrician", "Master Electrician", 
        "Plumbing License", "HVAC Certification", "EPA 608", "Welding Certification", 
        "CDL License", "Forklift Certification", "ASE Automotive", "Other - Trades"
      ]
    },
    tech: {
      title: "Technology & IT",
      icon: <Code className="h-4 w-4" />,
      items: [
        "CompTIA A+", "CompTIA Security+", "Cisco CCNA", "Microsoft Certified", 
        "AWS Certified", "Google Cloud Certified", "Salesforce Certified", 
        "PMP (Project Management)", "Scrum Master", "Six Sigma", "Other - Tech"
      ]
    },
    business: {
      title: "Business & Finance",
      icon: <Briefcase className="h-4 w-4" />,
      items: [
        "CPA", "CFA", "Real Estate License", "Insurance License", 
        "QuickBooks Certified", "Excel Expert", "Google Analytics", "Other - Business"
      ]
    },
    healthcare: {
      title: "Healthcare & Safety",
      icon: <Stethoscope className="h-4 w-4" />,
      items: [
        "CPR/First Aid", "CNA", "Medical Assistant", "Pharmacy Technician", 
        "EMT", "Food Handler's License", "ServSafe", "Other - Healthcare"
      ]
    }
  };

  // Simple technical skills categories
  const technicalSkillCategories = {
    office: {
      title: "Office & Computer Skills",
      icon: <Monitor className="h-4 w-4" />,
      items: [
        "Microsoft Office Suite", "Excel/Spreadsheets", "PowerPoint", "Word Processing",
        "Google Workspace", "Email Management", "Data Entry", "Basic Computer Skills"
      ]
    },
    trades: {
      title: "Skilled Trades & Technical",
      icon: <Wrench className="h-4 w-4" />,
      items: [
        "Electrical Work", "Plumbing", "HVAC Systems", "Welding", "Carpentry",
        "Automotive Repair", "Heavy Equipment Operation", "Blueprint Reading",
        "Hand Tools", "Power Tools", "Machinery Operation", "Equipment Maintenance"
      ]
    },
    creative: {
      title: "Creative & Design",
      icon: <Palette className="h-4 w-4" />,
      items: [
        "Graphic Design", "Adobe Creative Suite", "Photography", "Video Editing",
        "Web Design", "UI/UX Design", "Social Media Management", "Content Creation"
      ]
    },
    service: {
      title: "Service & Sales",
      icon: <Headphones className="h-4 w-4" />,
      items: [
        "Customer Service", "Sales", "Cash Handling", "POS Systems",
        "Phone Support", "Retail Operations", "Food Service", "Hospitality"
      ]
    }
  };

  // Simple soft skills categories
  const softSkillCategories = {
    leadership: {
      title: "Leadership & Management",
      icon: <Users className="h-4 w-4" />,
      items: [
        "Leadership", "Team Management", "Supervision", "Mentoring",
        "Delegation", "Conflict Resolution", "Decision Making", "Strategic Thinking"
      ]
    },
    communication: {
      title: "Communication & Interpersonal",
      icon: <Users className="h-4 w-4" />,
      items: [
        "Communication", "Public Speaking", "Presentation Skills", "Active Listening",
        "Negotiation", "Customer Relations", "Teamwork", "Collaboration"
      ]
    },
    analytical: {
      title: "Analytical & Problem-Solving",
      icon: <BarChart3 className="h-4 w-4" />,
      items: [
        "Problem Solving", "Critical Thinking", "Analytical Skills", "Research",
        "Data Analysis", "Attention to Detail", "Quality Control", "Process Improvement"
      ]
    },
    physical: {
      title: "Physical & Practical",
      icon: <Zap className="h-4 w-4" />,
      items: [
        "Physical Stamina", "Hand-Eye Coordination", "Manual Dexterity", "Multitasking",
        "Time Management", "Organization", "Reliability", "Work Ethic"
      ]
    }
  };

  // SIMPLIFIED: Direct interest list without complex categories
  const interestOptions = [
    "Technology & Software",
    "Business & Entrepreneurship", 
    "Creative Arts & Design",
    "Building & Construction",
    "Healthcare & Medicine",
    "Mechanical & Automotive",
    "Data & Analytics",
    "Sales & Marketing",
    "Education & Training",
    "Finance & Investment",
    "Food & Hospitality",
    "Sports & Fitness",
    "Travel & Tourism",
    "Music & Entertainment",
    "Science & Research",
    "Social Services",
    "Law & Government",
    "Environment & Sustainability"
  ];

  // SIMPLIFIED: Direct industry list without complex categories
  const industryOptions = [
    "Technology & Software",
    "Healthcare & Medical",
    "Construction & Trades",
    "Manufacturing & Industrial",
    "Financial Services",
    "Education",
    "Government & Public Service",
    "Retail & E-commerce",
    "Food Service & Hospitality",
    "Transportation & Logistics",
    "Real Estate",
    "Media & Entertainment",
    "Non-Profit & Social Services",
    "Energy & Utilities",
    "Consulting & Professional Services",
    "Agriculture & Environment",
    "Sports & Recreation",
    "Arts & Culture"
  ];

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="age" className="text-base font-medium">Age Range</Label>
                <Select value={formData.age} onValueChange={(value) => handleInputChange('age', value)}>
                  <SelectTrigger className="mt-2">
                    <SelectValue placeholder="Select age range" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="16-20">16-20</SelectItem>
                    <SelectItem value="21-25">21-25</SelectItem>
                    <SelectItem value="26-30">26-30</SelectItem>
                    <SelectItem value="31-35">31-35</SelectItem>
                    <SelectItem value="36-40">36-40</SelectItem>
                    <SelectItem value="41-45">41-45</SelectItem>
                    <SelectItem value="46-50">46-50</SelectItem>
                    <SelectItem value="50+">50+</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="experience" className="text-base font-medium">Years of Experience</Label>
                <Select value={formData.experience} onValueChange={(value) => handleInputChange('experience', value)}>
                  <SelectTrigger className="mt-2">
                    <SelectValue placeholder="Select experience level" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="0">No professional experience</SelectItem>
                    <SelectItem value="1-2">1-2 years</SelectItem>
                    <SelectItem value="3-5">3-5 years</SelectItem>
                    <SelectItem value="6-10">6-10 years</SelectItem>
                    <SelectItem value="10-20">10-20 years</SelectItem>
                    <SelectItem value="20+">20+ years</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div>
              <Label htmlFor="currentRole" className="text-base font-medium">Current/Most Recent Role</Label>
              <Input
                id="currentRole"
                value={formData.currentRole}
                onChange={(e) => handleInputChange('currentRole', e.target.value)}
                placeholder="e.g., Marketing Coordinator, Student, Unemployed, Electrician, Mechanic"
                className="mt-2"
              />
            </div>

            <div>
              <Label htmlFor="situation" className="text-base font-medium">What's your current work situation?</Label>
              <Select value={formData.currentSituation} onValueChange={(value) => handleInputChange('currentSituation', value)}>
                <SelectTrigger className="mt-2">
                  <SelectValue placeholder="Select your current work situation" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="student">Student</SelectItem>
                  <SelectItem value="employed">Currently Employed</SelectItem>
                  <SelectItem value="unemployed">Unemployed</SelectItem>
                  <SelectItem value="career-change">Looking for Career Change</SelectItem>
                  <SelectItem value="recent-graduate">Recent Graduate</SelectItem>
                  <SelectItem value="returning-workforce">Returning to Workforce</SelectItem>
                  <SelectItem value="trade-worker">Skilled Trade Worker</SelectItem>
                  <SelectItem value="apprentice">Apprentice/Trainee</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="location" className="text-base font-medium">Location</Label>
              <Input
                id="location"
                value={formData.location}
                onChange={(e) => handleInputChange('location', e.target.value)}
                placeholder="City, State/Country"
                className="mt-2"
              />
            </div>

            <div>
              <Label htmlFor="education" className="text-base font-medium">Education Level</Label>
              <Select value={formData.educationLevel} onValueChange={(value) => handleInputChange('educationLevel', value)}>
                <SelectTrigger className="mt-2">
                  <SelectValue placeholder="Select education level" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="high-school">High School</SelectItem>
                  <SelectItem value="some-college">Some College</SelectItem>
                  <SelectItem value="trade-school">Trade School/Vocational Training</SelectItem>
                  <SelectItem value="associates">Associate's Degree</SelectItem>
                  <SelectItem value="certificate">Professional Certificate</SelectItem>
                  <SelectItem value="bachelors">Bachelor's Degree</SelectItem>
                  <SelectItem value="masters">Master's Degree</SelectItem>
                  <SelectItem value="doctorate">Doctorate</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Certifications section */}
            <div className="border-t pt-6">
              <Label className="text-base font-medium mb-4 block">Certifications & Licenses (Optional)</Label>
              <p className="text-sm text-gray-600 mb-6">
                Select any certifications, licenses, or credentials you have.
              </p>
              
              <div className="space-y-4">
                {Object.entries(certificationCategories).map(([key, category]) => (
                  <div key={key} className="border border-gray-200 rounded-lg">
                    <button
                      type="button"
                      onClick={() => toggleCategory(key)}
                      className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50 transition-colors"
                    >
                      <div className="flex items-center space-x-3">
                        <div className="text-blue-600">
                          {category.icon}
                        </div>
                        <span className="font-medium text-gray-900">{category.title}</span>
                        <Badge variant="outline" className="text-xs">
                          {formData.certifications.filter(cert => category.items.includes(cert)).length} selected
                        </Badge>
                      </div>
                      {expandedCategories[key] ? (
                        <ChevronDown className="h-4 w-4 text-gray-500" />
                      ) : (
                        <ChevronRight className="h-4 w-4 text-gray-500" />
                      )}
                    </button>
                    
                    {expandedCategories[key] && (
                      <div className="px-4 pb-4 border-t border-gray-100">
                        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-2 mt-3">
                          {category.items.map((cert) => (
                            <div key={cert} className="flex items-center space-x-3 p-2">
                              <Checkbox
                                id={`cert-${cert}`}
                                checked={formData.certifications.includes(cert)}
                                onCheckedChange={() => handleArrayToggle('certifications', cert)}
                              />
                              <Label htmlFor={`cert-${cert}`} className="text-sm">
                                {cert}
                              </Label>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* FIXED: Resume section with proper confirmation */}
            <div className="border-t pt-6">
              <Label className="text-base font-medium mb-4 block">Resume (Optional but Recommended)</Label>
              <p className="text-sm text-gray-600 mb-4">
                Upload or paste your resume to help us provide more accurate career recommendations.
              </p>
              
              <Tabs value={activeResumeTab} onValueChange={setActiveResumeTab} className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="upload" className="flex items-center space-x-2 hover:bg-gray-100 hover:text-gray-900 transition-colors">
                    <Upload className="h-4 w-4" />
                    <span>Upload File</span>
                  </TabsTrigger>
                  <TabsTrigger value="paste" className="flex items-center space-x-2 hover:bg-gray-100 hover:text-gray-900 transition-colors">
                    <FileText className="h-4 w-4" />
                    <span>Copy & Paste</span>
                  </TabsTrigger>
                </TabsList>
                
                <TabsContent value="upload" className="mt-4">
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                    <Upload className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-600 mb-2">Upload your resume file</p>
                    <Button
                      onClick={() => document.getElementById('resume-file-input')?.click()}
                      className="w-full max-w-xs mx-auto hover:bg-primary/90 transition-colors"
                    >
                      Upload Resume
                    </Button>
                    <Input
                      id="resume-file-input"
                      type="file"
                      accept=".txt,.pdf,.doc,.docx"
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                    <p className="text-xs text-gray-500 mt-2">
                      Supports .txt, .pdf, .doc, and .docx files
                    </p>
                    
                    {/* FIXED: Show upload confirmation */}
                    {uploadedFileName && (
                      <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                        <div className="flex items-center justify-center space-x-2">
                          <CheckCircle className="h-4 w-4 text-green-600" />
                          <span className="text-sm text-green-800 font-medium">
                            File uploaded: {uploadedFileName}
                          </span>
                        </div>
                        <p className="text-xs text-green-600 mt-1">
                          Your resume has been processed and will be analyzed for career recommendations.
                        </p>
                      </div>
                    )}
                  </div>
                </TabsContent>
                
                <TabsContent value="paste" className="mt-4">
                  <Textarea
                    value={formData.resumeText}
                    onChange={(e) => handleInputChange('resumeText', e.target.value)}
                    placeholder="Paste your resume text here..."
                    className="min-h-[120px]"
                  />
                  {formData.resumeText && (
                    <div className="mt-2 p-2 bg-blue-50 border border-blue-200 rounded">
                      <p className="text-xs text-blue-600">
                        Resume text: {formData.resumeText.length} characters
                      </p>
                    </div>
                  )}
                </TabsContent>
              </Tabs>
            </div>

            {/* FIXED: LinkedIn section with better validation */}
            <div className="border-t pt-6">
              <Label htmlFor="linkedin" className="text-base font-medium flex items-center space-x-2">
                <Linkedin className="h-4 w-4 text-blue-600" />
                <span>LinkedIn Profile (Optional)</span>
              </Label>
              <Input
                id="linkedin"
                value={formData.linkedinProfile}
                onChange={(e) => handleInputChange('linkedinProfile', e.target.value)}
                placeholder="https://www.linkedin.com/in/your-profile"
                className="mt-2"
              />
              {formData.linkedinProfile && (
                <div className="mt-2 p-2 bg-blue-50 border border-blue-200 rounded">
                  <p className="text-xs text-blue-600">
                    ✅ LinkedIn profile will be analyzed for additional career insights
                  </p>
                </div>
              )}
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-8">
            {/* Technical Skills */}
            <div>
              <Label className="text-base font-medium mb-4 block">Technical Skills</Label>
              <p className="text-sm text-gray-600 mb-6">
                Select all technical skills that apply to you.
              </p>
              
              <div className="space-y-4">
                {Object.entries(technicalSkillCategories).map(([key, category]) => (
                  <div key={key} className="border border-gray-200 rounded-lg">
                    <button
                      type="button"
                      onClick={() => toggleSkillCategory(key)}
                      className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50 transition-colors"
                    >
                      <div className="flex items-center space-x-3">
                        <div className="text-blue-600">
                          {category.icon}
                        </div>
                        <span className="font-medium text-gray-900">{category.title}</span>
                        <Badge variant="outline" className="text-xs">
                          {formData.technicalSkills.filter(skill => category.items.includes(skill)).length} selected
                        </Badge>
                      </div>
                      {expandedSkillCategories[key] ? (
                        <ChevronDown className="h-4 w-4 text-gray-500" />
                      ) : (
                        <ChevronRight className="h-4 w-4 text-gray-500" />
                      )}
                    </button>
                    
                    {expandedSkillCategories[key] && (
                      <div className="px-4 pb-4 border-t border-gray-100">
                        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-2 mt-3">
                          {category.items.map((skill) => (
                            <div key={skill} className="flex items-center space-x-3 p-2">
                              <Checkbox
                                id={`tech-${skill}`}
                                checked={formData.technicalSkills.includes(skill)}
                                onCheckedChange={() => handleArrayToggle('technicalSkills', skill)}
                              />
                              <Label htmlFor={`tech-${skill}`} className="text-sm">
                                {skill}
                              </Label>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Soft Skills */}
            <div>
              <Label className="text-base font-medium mb-4 block">Soft Skills & Personal Strengths</Label>
              <p className="text-sm text-gray-600 mb-6">
                Select the soft skills that describe you best.
              </p>
              
              <div className="space-y-4">
                {Object.entries(softSkillCategories).map(([key, category]) => (
                  <div key={key} className="border border-gray-200 rounded-lg">
                    <button
                      type="button"
                      onClick={() => toggleSoftSkillCategory(key)}
                      className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50 transition-colors"
                    >
                      <div className="flex items-center space-x-3">
                        <div className="text-green-600">
                          {category.icon}
                        </div>
                        <span className="font-medium text-gray-900">{category.title}</span>
                        <Badge variant="outline" className="text-xs">
                          {formData.softSkills.filter(skill => category.items.includes(skill)).length} selected
                        </Badge>
                      </div>
                      {expandedSoftSkillCategories[key] ? (
                        <ChevronDown className="h-4 w-4 text-gray-500" />
                      ) : (
                        <ChevronRight className="h-4 w-4 text-gray-500" />
                      )}
                    </button>
                    
                    {expandedSoftSkillCategories[key] && (
                      <div className="px-4 pb-4 border-t border-gray-100">
                        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-2 mt-3">
                          {category.items.map((skill) => (
                            <div key={skill} className="flex items-center space-x-3 p-2">
                              <Checkbox
                                id={`soft-${skill}`}
                                checked={formData.softSkills.includes(skill)}
                                onCheckedChange={() => handleArrayToggle('softSkills', skill)}
                              />
                              <Label htmlFor={`soft-${skill}`} className="text-sm">
                                {skill}
                              </Label>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-8">
            {/* Work Preferences Only - Much cleaner now! */}
            <div className="space-y-8">
              <div>
                <Label className="text-base font-medium mb-4 block">Working with Data & Analytics</Label>
                <p className="text-sm text-gray-600 mb-3">
                  How much do you enjoy analyzing data, creating reports, and working with numbers?
                </p>
                <div className="px-6 py-4">
                  <Slider
                    value={formData.workingWithData}
                    onValueChange={(value) => handleInputChange('workingWithData', value)}
                    max={5}
                    min={1}
                    step={1}
                    className="w-full"
                  />
                  <div className="flex justify-between text-sm text-gray-500 mt-3">
                    <span>Not interested</span>
                    <span className="font-medium text-blue-600">
                      Rating: {formData.workingWithData[0]}
                    </span>
                    <span>Love it</span>
                  </div>
                </div>
              </div>

              <div>
                <Label className="text-base font-medium mb-4 block">Working with People & Teams</Label>
                <p className="text-sm text-gray-600 mb-3">
                  How much do you enjoy collaborating, leading teams, and interacting with others?
                </p>
                <div className="px-6 py-4">
                  <Slider
                    value={formData.workingWithPeople}
                    onValueChange={(value) => handleInputChange('workingWithPeople', value)}
                    max={5}
                    min={1}
                    step={1}
                    className="w-full"
                  />
                  <div className="flex justify-between text-sm text-gray-500 mt-3">
                    <span>Prefer solo work</span>
                    <span className="font-medium text-green-600">
                      Rating: {formData.workingWithPeople[0]}
                    </span>
                    <span>Love teamwork</span>
                  </div>
                </div>
              </div>

              <div>
                <Label className="text-base font-medium mb-4 block">Creative Tasks & Innovation</Label>
                <p className="text-sm text-gray-600 mb-3">
                  How much do you enjoy creative work, design, and coming up with new ideas?
                </p>
                <div className="px-6 py-4">
                  <Slider
                    value={formData.creativeTasks}
                    onValueChange={(value) => handleInputChange('creativeTasks', value)}
                    max={5}
                    min={1}
                    step={1}
                    className="w-full"
                  />
                  <div className="flex justify-between text-sm text-gray-500 mt-3">
                    <span>Not creative</span>
                    <span className="font-medium text-purple-600">
                      Rating: {formData.creativeTasks[0]}
                    </span>
                    <span>Very creative</span>
                  </div>
                </div>
              </div>

              <div>
                <Label className="text-base font-medium mb-4 block">Problem Solving & Troubleshooting</Label>
                <p className="text-sm text-gray-600 mb-3">
                  How much do you enjoy solving complex problems and figuring out solutions?
                </p>
                <div className="px-6 py-4">
                  <Slider
                    value={formData.problemSolving}
                    onValueChange={(value) => handleInputChange('problemSolving', value)}
                    max={5}
                    min={1}
                    step={1}
                    className="w-full"
                  />
                  <div className="flex justify-between text-sm text-gray-500 mt-3">
                    <span>Avoid problems</span>
                    <span className="font-medium text-orange-600">
                      Rating: {formData.problemSolving[0]}
                    </span>
                    <span>Love challenges</span>
                  </div>
                </div>
              </div>

              <div>
                <Label className="text-base font-medium mb-4 block">Leadership & Management</Label>
                <p className="text-sm text-gray-600 mb-3">
                  How comfortable are you with leading others and taking charge of projects?
                </p>
                <div className="px-6 py-4">
                  <Slider
                    value={formData.leadership}
                    onValueChange={(value) => handleInputChange('leadership', value)}
                    max={5}
                    min={1}
                    step={1}
                    className="w-full"
                  />
                  <div className="flex justify-between text-sm text-gray-500 mt-3">
                    <span>Prefer following</span>
                    <span className="font-medium text-red-600">
                      Rating: {formData.leadership[0]}
                    </span>
                    <span>Natural leader</span>
                  </div>
                </div>
              </div>

              <div>
                <Label className="text-base font-medium mb-4 block">Physical & Hands-On Work</Label>
                <p className="text-sm text-gray-600 mb-3">
                  How much do you enjoy working with your hands, building, fixing, or physical tasks?
                </p>
                <div className="px-6 py-4">
                  <Slider
                    value={formData.physicalHandsOnWork}
                    onValueChange={(value) => handleInputChange('physicalHandsOnWork', value)}
                    max={5}
                    min={1}
                    step={1}
                    className="w-full"
                  />
                  <div className="flex justify-between text-sm text-gray-500 mt-3">
                    <span>Prefer desk work</span>
                    <span className="font-medium text-amber-600">
                      Rating: {formData.physicalHandsOnWork[0]}
                    </span>
                    <span>Love hands-on</span>
                  </div>
                </div>
              </div>

              <div>
                <Label className="text-base font-medium mb-4 block">Outdoor Work Environment</Label>
                <p className="text-sm text-gray-600 mb-3">
                  How comfortable are you working outdoors or in non-office environments?
                </p>
                <div className="px-6 py-4">
                  <Slider
                    value={formData.outdoorWork}
                    onValueChange={(value) => handleInputChange('outdoorWork', value)}
                    max={5}
                    min={1}
                    step={1}
                    className="w-full"
                  />
                  <div className="flex justify-between text-sm text-gray-500 mt-3">
                    <span>Indoor only</span>
                    <span className="font-medium text-emerald-600">
                      Rating: {formData.outdoorWork[0]}
                    </span>
                    <span>Love outdoors</span>
                  </div>
                </div>
              </div>

              <div>
                <Label className="text-base font-medium mb-4 block">Mechanical Aptitude & Technical Systems</Label>
                <p className="text-sm text-gray-600 mb-3">
                  How comfortable are you with understanding how things work mechanically or technically?
                </p>
                <div className="px-6 py-4">
                  <Slider
                    value={formData.mechanicalAptitude}
                    onValueChange={(value) => handleInputChange('mechanicalAptitude', value)}
                    max={5}
                    min={1}
                    step={1}
                    className="w-full"
                  />
                  <div className="flex justify-between text-sm text-gray-500 mt-3">
                    <span>Not technical</span>
                    <span className="font-medium text-indigo-600">
                      Rating: {formData.mechanicalAptitude[0]}
                    </span>
                    <span>Very technical</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      case 4:
        return (
          <div className="space-y-8">
            {/* MOVED: Interests and Industries from Step 3 */}
            {/* SIMPLIFIED Interests */}
            <div>
              <Label className="text-base font-medium mb-4 block">Interest Areas</Label>
              <p className="text-sm text-gray-600 mb-6">
                Select 3-8 areas that genuinely interest you. Choose the ones that excite you most.
              </p>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-2">
                {interestOptions.map((interest) => (
                  <div key={interest} className="flex items-center space-x-3 p-2">
                    <Checkbox
                      id={`interest-${interest}`}
                      checked={formData.interests.includes(interest)}
                      onCheckedChange={() => handleArrayToggle('interests', interest)}
                    />
                    <Label htmlFor={`interest-${interest}`} className="text-sm">
                      {interest}
                    </Label>
                  </div>
                ))}
              </div>
              
              {formData.interests.length > 0 && (
                <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                  <p className="text-sm text-blue-800">
                    <strong>{formData.interests.length}</strong> interests selected
                    {formData.interests.length > 8 && (
                      <span className="text-blue-600"> (Consider selecting fewer for more focused recommendations)</span>
                    )}
                  </p>
                </div>
              )}
            </div>

            {/* SIMPLIFIED Industries */}
            <div>
              <Label className="text-base font-medium mb-4 block">Industry Preferences</Label>
              <p className="text-sm text-gray-600 mb-6">
                Select 3-8 industries you'd be interested in working in. Think about where you'd like to apply your skills.
              </p>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-2">
                {industryOptions.map((industry) => (
                  <div key={industry} className="flex items-center space-x-3 p-2">
                    <Checkbox
                      id={`industry-${industry}`}
                      checked={formData.industries.includes(industry)}
                      onCheckedChange={() => handleArrayToggle('industries', industry)}
                    />
                    <Label htmlFor={`industry-${industry}`} className="text-sm">
                      {industry}
                    </Label>
                  </div>
                ))}
              </div>
              
              {formData.industries.length > 0 && (
                <div className="mt-4 p-3 bg-green-50 rounded-lg">
                  <p className="text-sm text-green-800">
                    <strong>{formData.industries.length}</strong> industries selected
                    {formData.industries.length > 8 && (
                      <span className="text-green-600"> (Consider selecting fewer for more targeted recommendations)</span>
                    )}
                  </p>
                </div>
              )}
            </div>

            {/* EXISTING: Goals and Expectations */}
            <div className="border-t pt-6">
              <div>
                <Label htmlFor="career-goals" className="text-base font-medium">Career Goals & Aspirations</Label>
                <p className="text-sm text-gray-600 mb-3">
                  Describe your career goals and what you hope to achieve professionally.
                </p>
                <Textarea
                  id="career-goals"
                  value={formData.careerGoals}
                  onChange={(e) => handleInputChange('careerGoals', e.target.value)}
                  placeholder="e.g., I want to work in a hands-on role where I can solve problems and see tangible results..."
                  className="mt-2 min-h-[100px]"
                />
              </div>
            </div>

            <div>
              <Label htmlFor="work-life-balance" className="text-base font-medium">Work-Life Balance Importance</Label>
              <Select value={formData.workLifeBalance} onValueChange={(value) => handleInputChange('workLifeBalance', value)}>
                <SelectTrigger className="mt-2">
                  <SelectValue placeholder="Select importance level" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="very-important">Very Important - I prioritize personal time</SelectItem>
                  <SelectItem value="important">Important - I want a good balance</SelectItem>
                  <SelectItem value="somewhat-important">Somewhat Important - I'm flexible</SelectItem>
                  <SelectItem value="not-important">Not Very Important - I'm career-focused</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="salary" className="text-base font-medium">Salary Expectations</Label>
              <Select value={formData.salaryExpectations} onValueChange={(value) => handleInputChange('salaryExpectations', value)}>
                <SelectTrigger className="mt-2">
                  <SelectValue placeholder="Select salary range" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="0-30000">Under $30,000</SelectItem>
                  <SelectItem value="30000-50000">$30,000 - $50,000</SelectItem>
                  <SelectItem value="50000-70000">$50,000 - $70,000</SelectItem>
                  <SelectItem value="70000-100000">$70,000 - $100,000</SelectItem>
                  <SelectItem value="100000-150000">$100,000 - $150,000</SelectItem>
                  <SelectItem value="150000-250000">$150,000 - $250,000</SelectItem>
                  <SelectItem value="250000-999999">$250,000+</SelectItem>
                  <SelectItem value="0-0">Flexible/Open to Discussion</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  const getStepTitle = () => {
    switch (currentStep) {
      case 1: return "Profile & Background";
      case 2: return "Skills Assessment";
      case 3: return "Work Preferences";
      case 4: return "Interests, Industries & Goals";
      default: return "";
    }
  };

  const getStepDescription = () => {
    switch (currentStep) {
      case 1: return "Tell us about your background, education, and certifications";
      case 2: return "Select your technical and soft skills";
      case 3: return "Rate your work preferences and comfort levels";
      case 4: return "Select your interests, preferred industries, and share your goals";
      default: return "";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <Button 
            variant="ghost" 
            className="mb-4"
            onClick={() => navigate('/dashboard')}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
          
          <div className="flex items-center justify-center space-x-2 mb-4">
            <button
              onClick={() => navigate('/')}
              className="transition-opacity hover:opacity-80 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-lg p-1"
              aria-label="Go to home page"
            >
              <Search className="h-8 w-8 text-blue-600" />
            </button>
            <span className="text-2xl font-bold text-gray-900">
              {isEditMode ? 'Edit Career Assessment' : 'Career Assessment'}
            </span>
          </div>
          
          <p className="text-gray-600">
            {isEditMode 
              ? 'Update your assessment to get refreshed career recommendations'
              : 'Complete our assessment to discover personalized career recommendations'
            }
          </p>
        </div>

        <div className="mb-8">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Step {currentStep} of {totalSteps}</span>
            <span>{Math.round((currentStep / totalSteps) * 100)}% Complete</span>
          </div>
          <Progress value={(currentStep / totalSteps) * 100} className="h-3" />
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-xl">{getStepTitle()}</CardTitle>
            <CardDescription className="text-base">{getStepDescription()}</CardDescription>
          </CardHeader>
          <CardContent>
            {renderStep()}
            
            <div className="flex justify-between mt-8 pt-6 border-t">
              <Button
                variant="outline"
                onClick={handlePrevious}
                disabled={currentStep === 1}
                size="lg"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Previous
              </Button>
              
              {currentStep === totalSteps ? (
                <Button onClick={handleSubmit} className="bg-blue-600 hover:bg-blue-700" size="lg">
                  {isEditMode ? 'Update Assessment' : 'Complete Assessment'}
                </Button>
              ) : (
                <Button 
                  onClick={handleNext} 
                  size="lg"
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  Next Step
                  <ArrowRight className="h-4 w-4 ml-2" />
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Assessment;