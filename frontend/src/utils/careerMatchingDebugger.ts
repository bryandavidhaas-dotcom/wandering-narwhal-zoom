// ========================================
// CAREER MATCHING DEBUGGER
// ========================================
// Utility to diagnose why users get zero recommendations

import { generateCareerRecommendations, CAREER_TEMPLATES, getExperienceLevel, getExperienceYears } from './careerMatching';

export interface DebugResult {
  issue: string;
  details: any;
  recommendation: string;
}

export const debugCareerMatching = (assessmentData: any, explorationLevel: number): DebugResult[] => {
  const issues: DebugResult[] = [];
  
  console.log('🔍 DEBUGGING: Career matching for exploration level', explorationLevel);
  console.log('📊 Assessment data:', assessmentData);
  
  // Check 1: Assessment data exists
  if (!assessmentData) {
    issues.push({
      issue: 'No assessment data provided',
      details: { assessmentData: null },
      recommendation: 'Complete your assessment first'
    });
    return issues;
  }
  
  // Check 2: Career templates loaded
  if (!CAREER_TEMPLATES || CAREER_TEMPLATES.length === 0) {
    issues.push({
      issue: 'No career templates loaded',
      details: { templateCount: CAREER_TEMPLATES?.length || 0 },
      recommendation: 'System error - career database not loaded'
    });
    return issues;
  }
  
  console.log('✅ Career templates loaded:', CAREER_TEMPLATES.length);
  
  // Check 3: Required fields present
  const requiredFields = [
    'experience', 'workingWithData', 'workingWithPeople', 'creativeTasks',
    'problemSolving', 'leadership', 'interests', 'industries'
  ];
  
  const missingFields = requiredFields.filter(field => {
    const value = assessmentData[field];
    if (field === 'interests' || field === 'industries') {
      return !Array.isArray(value) || value.length === 0;
    }
    return value === undefined || value === null;
  });
  
  if (missingFields.length > 0) {
    issues.push({
      issue: 'Missing required assessment fields',
      details: { missingFields, assessmentData },
      recommendation: 'Complete all sections of your assessment'
    });
  }
  
  // Check 4: Data types are correct
  const workPrefs = ['workingWithData', 'workingWithPeople', 'creativeTasks', 'problemSolving', 'leadership'];
  const invalidWorkPrefs = workPrefs.filter(field => {
    const value = assessmentData[field];
    // Handle both array format [3] and direct number 3
    const numValue = Array.isArray(value) ? value[0] : value;
    return typeof numValue !== 'number' || numValue < 1 || numValue > 5;
  });
  
  if (invalidWorkPrefs.length > 0) {
    issues.push({
      issue: 'Invalid work preference values',
      details: { 
        invalidFields: invalidWorkPrefs,
        values: invalidWorkPrefs.map(field => ({ field, value: assessmentData[field] }))
      },
      recommendation: 'Work preferences must be numbers between 1-5'
    });
  }
  
  // Check 5: Experience level processing
  const userExperienceLevel = getExperienceLevel(assessmentData.experience);
  const userExperienceYears = getExperienceYears(assessmentData.experience);
  
  console.log('👤 User experience:', {
    raw: assessmentData.experience,
    level: userExperienceLevel,
    years: userExperienceYears
  });
  
  // Check 6: Try to run the algorithm and catch errors
  try {
    console.log('🧪 Testing algorithm with user data...');
    const testRecommendations = generateCareerRecommendations(assessmentData, explorationLevel);
    console.log('📊 Algorithm returned:', testRecommendations.length, 'recommendations');
    
    if (testRecommendations.length === 0) {
      // Algorithm ran but returned zero - this is the main issue
      issues.push({
        issue: 'Algorithm returned zero recommendations',
        details: {
          explorationLevel,
          userExperienceLevel,
          userExperienceYears,
          templateCount: CAREER_TEMPLATES.length,
          assessmentSample: {
            experience: assessmentData.experience,
            workingWithData: assessmentData.workingWithData,
            interests: assessmentData.interests?.length || 0,
            industries: assessmentData.industries?.length || 0
          }
        },
        recommendation: 'Algorithm filtering too aggressively - needs adjustment'
      });
    }
  } catch (error) {
    issues.push({
      issue: 'Algorithm crashed during execution',
      details: { error: error.toString(), stack: error.stack },
      recommendation: 'Fix algorithm error'
    });
  }
  
  return issues;
};

export const fixAssessmentData = (assessmentData: any): any => {
  if (!assessmentData) return assessmentData;
  
  const fixed = { ...assessmentData };
  
  // Fix work preferences - convert arrays to numbers
  const workPrefs = ['workingWithData', 'workingWithPeople', 'creativeTasks', 'problemSolving', 'leadership'];
  workPrefs.forEach(field => {
    if (Array.isArray(fixed[field])) {
      fixed[field] = fixed[field][0] || 3;
    }
    if (typeof fixed[field] !== 'number') {
      fixed[field] = 3; // Default to middle value
    }
  });
  
  // Ensure arrays exist
  if (!Array.isArray(fixed.interests)) {
    fixed.interests = [];
  }
  if (!Array.isArray(fixed.industries)) {
    fixed.industries = [];
  }
  if (!Array.isArray(fixed.technicalSkills)) {
    fixed.technicalSkills = [];
  }
  if (!Array.isArray(fixed.softSkills)) {
    fixed.softSkills = [];
  }
  
  // Ensure experience exists
  if (!fixed.experience) {
    fixed.experience = '3-5'; // Default
  }
  
  return fixed;
};