// ========================================
// PROFILE VALIDATION UTILITY
// ========================================
// Ensures that career matching only runs when user has complete assessment data

export interface UserAssessmentData {
  // Step 1: Basic Information
  age: string;
  location: string;
  educationLevel: string;
  currentSituation: string;
  experience: string;
  currentRole?: string;
  resumeText?: string;
  linkedinProfile?: string;
  certifications?: string[];
  
  // Step 2: Skills
  technicalSkills: string[];
  softSkills: string[];
  
  // Step 3: Preferences & Interests
  workingWithData: number;
  workingWithPeople: number;
  creativeTasks: number;
  problemSolving: number;
  leadership: number;
  interests: string[];
  industries: string[];
  workEnvironment: string;
  
  // Step 4: Goals
  careerGoals: string;
  workLifeBalance: string;
  salaryExpectations: string;
  additionalInfo?: string;
  
  [key: string]: any;
}

export const validateProfileCompleteness = (assessmentData: UserAssessmentData | undefined): boolean => {
  if (!assessmentData) {
    console.log('No assessment data found');
    return false;
  }
  
  // Required fields for complete profile
  const requiredFields = [
    // Step 1: Basic Information
    'age',
    'location', 
    'educationLevel',
    'currentSituation',
    'experience',
    
    // Step 2: Skills (arrays should have at least some items)
    'technicalSkills',
    'softSkills',
    
    // Step 3: Preferences (should have values)
    'workingWithData',
    'workingWithPeople', 
    'creativeTasks',
    'problemSolving',
    'leadership',
    'interests',
    'industries',
    'workEnvironment',
    
    // Step 4: Goals
    'careerGoals',
    'workLifeBalance',
    'salaryExpectations'
  ];
  
  // Check that all required fields exist and have meaningful values
  for (const field of requiredFields) {
    const value = assessmentData[field];
    
    if (value === undefined || value === null || value === '') {
      console.log(`Missing required field: ${field}`);
      return false;
    }
    
    // For arrays, check they have at least one item
    if (Array.isArray(value) && value.length === 0) {
      console.log(`Empty array field: ${field}`);
      return false;
    }
    
    // For slider values, check they're valid numbers
    if (field.includes('working') || field === 'leadership' || field === 'creativeTasks' || field === 'problemSolving') {
      if (typeof value !== 'number' || value < 1 || value > 5) {
        console.log(`Invalid slider value for ${field}: ${value}`);
        return false;
      }
    }
  }
  
  return true;
};

export const getProfileCompletionStatus = (assessmentData: UserAssessmentData | undefined): {
  isComplete: boolean;
  completionPercentage: number;
  missingFields: string[];
} => {
  if (!assessmentData) {
    return {
      isComplete: false,
      completionPercentage: 0,
      missingFields: ['Complete assessment required']
    };
  }

  const requiredFields = [
    'age', 'location', 'educationLevel', 'currentSituation', 'experience',
    'technicalSkills', 'softSkills', 'workingWithData', 'workingWithPeople',
    'creativeTasks', 'problemSolving', 'leadership', 'interests', 'industries',
    'workEnvironment', 'careerGoals', 'workLifeBalance', 'salaryExpectations'
  ];

  const missingFields: string[] = [];
  let completedFields = 0;

  for (const field of requiredFields) {
    const value = assessmentData[field];
    
    if (value === undefined || value === null || value === '') {
      missingFields.push(field);
    } else if (Array.isArray(value) && value.length === 0) {
      missingFields.push(field);
    } else if (field.includes('working') || field === 'leadership' || field === 'creativeTasks' || field === 'problemSolving') {
      if (typeof value !== 'number' || value < 1 || value > 5) {
        missingFields.push(field);
      } else {
        completedFields++;
      }
    } else {
      completedFields++;
    }
  }

  const completionPercentage = Math.round((completedFields / requiredFields.length) * 100);
  const isComplete = missingFields.length === 0;

  return {
    isComplete,
    completionPercentage,
    missingFields
  };
};