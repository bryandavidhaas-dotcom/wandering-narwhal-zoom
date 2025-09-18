// ========================================
// CAREER TEMPLATE VALIDATOR
// ========================================
// Validates that all career templates have complete data and consistent careerType values

import { CAREER_TEMPLATES } from './careerMatching';

export interface ValidationIssue {
  careerTitle: string;
  careerType: string;
  issue: string;
  severity: 'error' | 'warning';
}

export interface CareerTemplateValidationResult {
  isValid: boolean;
  issues: ValidationIssue[];
  missingFields: string[];
  duplicateCareerTypes: string[];
  totalCareers: number;
}

/**
 * Validates all career templates for completeness and consistency
 */
export const validateCareerTemplates = (): CareerTemplateValidationResult => {
  console.log('🔍 Validating career templates...');
  
  const issues: ValidationIssue[] = [];
  const missingFields: string[] = [];
  const careerTypeMap = new Map<string, string[]>();
  
  // Required fields for all career templates
  const requiredFields = [
    'title',
    'careerType',
    'salaryRange',
    'description',
    'requiredTechnicalSkills',
    'requiredSoftSkills',
    'preferredInterests',
    'preferredIndustries',
    'workDataWeight',
    'workPeopleWeight',
    'creativityWeight',
    'problemSolvingWeight',
    'leadershipWeight',
    'learningPath',
    'companies',
    'experienceLevel',
    'salaryMin',
    'salaryMax',
    'workEnvironments'
  ];

  CAREER_TEMPLATES.forEach((career, index) => {
    const careerTitle = career.title || `Career ${index}`;
    const careerType = career.careerType || 'unknown';
    
    // Check for missing required fields
    requiredFields.forEach(field => {
      if (career[field as keyof typeof career] === undefined || career[field as keyof typeof career] === null) {
        issues.push({
          careerTitle,
          careerType,
          issue: `Missing required field: ${field}`,
          severity: 'error'
        });
        if (!missingFields.includes(field)) {
          missingFields.push(field);
        }
      }
    });

    // Check for empty arrays that should have content
    const arrayFields = ['requiredTechnicalSkills', 'requiredSoftSkills', 'preferredInterests', 'preferredIndustries', 'companies', 'workEnvironments'];
    arrayFields.forEach(field => {
      const value = career[field as keyof typeof career];
      if (Array.isArray(value) && value.length === 0) {
        issues.push({
          careerTitle,
          careerType,
          issue: `Empty array for field: ${field}`,
          severity: 'warning'
        });
      }
    });

    // Check for invalid careerType format
    if (careerType && (careerType.includes(' ') || careerType !== careerType.toLowerCase())) {
      issues.push({
        careerTitle,
        careerType,
        issue: `Invalid careerType format: should be lowercase with hyphens, got "${careerType}"`,
        severity: 'error'
      });
    }

    // Track duplicate careerTypes
    if (!careerTypeMap.has(careerType)) {
      careerTypeMap.set(careerType, []);
    }
    careerTypeMap.get(careerType)!.push(careerTitle);

    // Check salary consistency
    if (career.salaryMin && career.salaryMax && career.salaryMin > career.salaryMax) {
      issues.push({
        careerTitle,
        careerType,
        issue: `Invalid salary range: min (${career.salaryMin}) > max (${career.salaryMax})`,
        severity: 'error'
      });
    }

    // Check experience level validity
    const validExperienceLevels = ['entry', 'junior', 'mid', 'senior', 'executive'];
    if (career.experienceLevel && !validExperienceLevels.includes(career.experienceLevel)) {
      issues.push({
        careerTitle,
        careerType,
        issue: `Invalid experience level: ${career.experienceLevel}`,
        severity: 'error'
      });
    }

    // Check work preference weights (should be 1-5)
    const weightFields = ['workDataWeight', 'workPeopleWeight', 'creativityWeight', 'problemSolvingWeight', 'leadershipWeight'];
    weightFields.forEach(field => {
      const value = career[field as keyof typeof career] as number;
      if (typeof value === 'number' && (value < 1 || value > 5)) {
        issues.push({
          careerTitle,
          careerType,
          issue: `Invalid weight for ${field}: ${value} (should be 1-5)`,
          severity: 'warning'
        });
      }
    });
  });

  // Find duplicate careerTypes
  const duplicateCareerTypes: string[] = [];
  careerTypeMap.forEach((titles, careerType) => {
    if (titles.length > 1) {
      duplicateCareerTypes.push(careerType);
      issues.push({
        careerTitle: titles.join(', '),
        careerType,
        issue: `Duplicate careerType "${careerType}" used by multiple careers`,
        severity: 'error'
      });
    }
  });

  const isValid = issues.filter(issue => issue.severity === 'error').length === 0;

  console.log(`✅ Career template validation complete: ${isValid ? 'VALID' : 'INVALID'}`);
  console.log(`📊 Total careers: ${CAREER_TEMPLATES.length}`);
  console.log(`⚠️ Issues found: ${issues.length} (${issues.filter(i => i.severity === 'error').length} errors, ${issues.filter(i => i.severity === 'warning').length} warnings)`);

  return {
    isValid,
    issues,
    missingFields,
    duplicateCareerTypes,
    totalCareers: CAREER_TEMPLATES.length
  };
};

/**
 * Validates that a specific careerType exists in the templates
 */
export const validateCareerTypeExists = (careerType: string): boolean => {
  return CAREER_TEMPLATES.some(career => career.careerType === careerType);
};

/**
 * Gets all available careerTypes
 */
export const getAllCareerTypes = (): string[] => {
  return CAREER_TEMPLATES.map(career => career.careerType);
};

/**
 * Finds careers with missing or invalid careerTypes
 */
export const findInvalidCareerTypes = (): Array<{ title: string; careerType: string; issue: string }> => {
  const invalid: Array<{ title: string; careerType: string; issue: string }> = [];
  
  CAREER_TEMPLATES.forEach(career => {
    if (!career.careerType) {
      invalid.push({
        title: career.title,
        careerType: 'undefined',
        issue: 'Missing careerType'
      });
    } else if (career.careerType.includes(' ')) {
      invalid.push({
        title: career.title,
        careerType: career.careerType,
        issue: 'careerType contains spaces'
      });
    } else if (career.careerType !== career.careerType.toLowerCase()) {
      invalid.push({
        title: career.title,
        careerType: career.careerType,
        issue: 'careerType not lowercase'
      });
    }
  });
  
  return invalid;
};

/**
 * Quick validation check for production use
 */
export const quickValidationCheck = (): { isValid: boolean; errorCount: number; warningCount: number } => {
  const result = validateCareerTemplates();
  const errorCount = result.issues.filter(issue => issue.severity === 'error').length;
  const warningCount = result.issues.filter(issue => issue.severity === 'warning').length;
  
  return {
    isValid: result.isValid,
    errorCount,
    warningCount
  };
};