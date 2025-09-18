// ========================================
// ASSESSMENT DATA VALIDATOR
// ========================================
// Validates that assessment data is properly structured and compatible with the career matching algorithm

export interface AssessmentValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
  missingFields: string[];
  dataIntegrity: {
    hasRequiredFields: boolean;
    hasWorkPreferences: boolean;
    hasInterests: boolean;
    hasIndustries: boolean;
    hasSkills: boolean;
  };
}

/**
 * Validates assessment data structure and completeness
 */
export const validateAssessmentData = (assessmentData: any): AssessmentValidationResult => {
  const errors: string[] = [];
  const warnings: string[] = [];
  const missingFields: string[] = [];

  // Check if assessment data exists
  if (!assessmentData) {
    return {
      isValid: false,
      errors: ['Assessment data is null or undefined'],
      warnings: [],
      missingFields: ['All fields'],
      dataIntegrity: {
        hasRequiredFields: false,
        hasWorkPreferences: false,
        hasInterests: false,
        hasIndustries: false,
        hasSkills: false
      }
    };
  }

  // ========================================
  // REQUIRED FIELDS VALIDATION
  // ========================================
  const requiredFields = [
    'age', 'location', 'educationLevel', 'currentSituation', 'experience',
    'technicalSkills', 'softSkills', 'workingWithData', 'workingWithPeople',
    'creativeTasks', 'problemSolving', 'leadership', 'physicalHandsOnWork',
    'outdoorWork', 'mechanicalAptitude', 'interests', 'industries',
    'careerGoals', 'workLifeBalance', 'salaryExpectations'
  ];

  requiredFields.forEach(field => {
    if (assessmentData[field] === undefined || assessmentData[field] === null || assessmentData[field] === '') {
      missingFields.push(field);
    }
  });

  // ========================================
  // WORK PREFERENCES VALIDATION
  // ========================================
  const workPreferenceFields = [
    'workingWithData', 'workingWithPeople', 'creativeTasks', 
    'problemSolving', 'leadership', 'physicalHandsOnWork',
    'outdoorWork', 'mechanicalAptitude'
  ];

  let hasValidWorkPreferences = true;
  workPreferenceFields.forEach(field => {
    const value = assessmentData[field];
    if (typeof value !== 'number' || value < 1 || value > 5) {
      errors.push(`Work preference '${field}' must be a number between 1 and 5, got: ${value}`);
      hasValidWorkPreferences = false;
    }
  });

  // ========================================
  // SKILLS VALIDATION
  // ========================================
  const hasValidSkills = Array.isArray(assessmentData.technicalSkills) && 
                        Array.isArray(assessmentData.softSkills);
  
  if (!hasValidSkills) {
    errors.push('Technical skills and soft skills must be arrays');
  }

  if (assessmentData.technicalSkills?.length === 0 && assessmentData.softSkills?.length === 0) {
    warnings.push('No skills selected - this may result in less accurate recommendations');
  }

  // ========================================
  // INTERESTS AND INDUSTRIES VALIDATION
  // ========================================
  const hasValidInterests = Array.isArray(assessmentData.interests) && assessmentData.interests.length > 0;
  const hasValidIndustries = Array.isArray(assessmentData.industries) && assessmentData.industries.length > 0;

  if (!hasValidInterests) {
    errors.push('Interests must be a non-empty array');
  }

  if (!hasValidIndustries) {
    errors.push('Industries must be a non-empty array');
  }

  // Check for optimal selection counts
  if (assessmentData.interests?.length > 10) {
    warnings.push('Too many interests selected (>10) - consider focusing on top priorities');
  }

  if (assessmentData.industries?.length > 10) {
    warnings.push('Too many industries selected (>10) - consider focusing on top priorities');
  }

  // ========================================
  // ALGORITHM COMPATIBILITY CHECK
  // ========================================
  
  // Check for fields that the algorithm expects
  const algorithmFields = [
    'workingWithData', 'workingWithPeople', 'creativeTasks', 'problemSolving', 
    'leadership', 'handsOnWork', 'physicalWork', 'outdoorWork', 'mechanicalAptitude'
  ];

  // Ensure backward compatibility fields exist
  if (assessmentData.physicalHandsOnWork && !assessmentData.handsOnWork) {
    warnings.push('Missing handsOnWork field - using physicalHandsOnWork as fallback');
  }

  if (assessmentData.physicalHandsOnWork && !assessmentData.physicalWork) {
    warnings.push('Missing physicalWork field - using physicalHandsOnWork as fallback');
  }

  // ========================================
  // DATA INTEGRITY SUMMARY
  // ========================================
  const dataIntegrity = {
    hasRequiredFields: missingFields.length === 0,
    hasWorkPreferences: hasValidWorkPreferences,
    hasInterests: hasValidInterests,
    hasIndustries: hasValidIndustries,
    hasSkills: hasValidSkills
  };

  const isValid = errors.length === 0 && dataIntegrity.hasRequiredFields;

  return {
    isValid,
    errors,
    warnings,
    missingFields,
    dataIntegrity
  };
};

/**
 * Validates that assessment data is compatible with the career matching algorithm
 */
export const validateAlgorithmCompatibility = (assessmentData: any): boolean => {
  const validation = validateAssessmentData(assessmentData);
  
  // Algorithm needs at minimum:
  // - Work preferences (all 8 sliders)
  // - Some skills (technical or soft)
  // - Some interests
  // - Some industries
  // - Basic profile info (experience, education)
  
  return validation.isValid && 
         validation.dataIntegrity.hasWorkPreferences &&
         validation.dataIntegrity.hasInterests &&
         validation.dataIntegrity.hasIndustries &&
         (assessmentData.technicalSkills?.length > 0 || assessmentData.softSkills?.length > 0);
};

/**
 * Fixes common data structure issues for backward compatibility
 */
export const normalizeAssessmentData = (assessmentData: any): any => {
  if (!assessmentData) return assessmentData;

  const normalized = { ...assessmentData };

  // Ensure backward compatibility for work preferences
  if (normalized.physicalHandsOnWork && !normalized.handsOnWork) {
    normalized.handsOnWork = normalized.physicalHandsOnWork;
  }

  if (normalized.physicalHandsOnWork && !normalized.physicalWork) {
    normalized.physicalWork = normalized.physicalHandsOnWork;
  }

  // Ensure arrays are properly initialized
  if (!Array.isArray(normalized.technicalSkills)) {
    normalized.technicalSkills = [];
  }

  if (!Array.isArray(normalized.softSkills)) {
    normalized.softSkills = [];
  }

  if (!Array.isArray(normalized.interests)) {
    normalized.interests = [];
  }

  if (!Array.isArray(normalized.industries)) {
    normalized.industries = [];
  }

  if (!Array.isArray(normalized.certifications)) {
    normalized.certifications = [];
  }

  return normalized;
};