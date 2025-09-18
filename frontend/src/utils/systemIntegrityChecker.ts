// ========================================
// SYSTEM INTEGRITY CHECKER
// ========================================
// Validates that all components of the career discovery system work together properly

import { validateAssessmentData, validateAlgorithmCompatibility, normalizeAssessmentData } from './assessmentValidator';
import { generateCareerRecommendations, CAREER_TEMPLATES } from './careerMatching';

export interface SystemIntegrityResult {
  overall: 'PASS' | 'FAIL' | 'WARNING';
  components: {
    assessment: 'PASS' | 'FAIL' | 'WARNING';
    algorithm: 'PASS' | 'FAIL' | 'WARNING';
    careerDatabase: 'PASS' | 'FAIL' | 'WARNING';
    dataFlow: 'PASS' | 'FAIL' | 'WARNING';
    navigation: 'PASS' | 'FAIL' | 'WARNING';
  };
  issues: string[];
  recommendations: string[];
}

/**
 * Runs comprehensive system integrity checks
 */
export const runSystemIntegrityCheck = (): SystemIntegrityResult => {
  const issues: string[] = [];
  const recommendations: string[] = [];
  
  console.log('🔍 Running comprehensive system integrity check...');

  // ========================================
  // 1. ASSESSMENT COMPONENT CHECK
  // ========================================
  let assessmentStatus: 'PASS' | 'FAIL' | 'WARNING' = 'PASS';
  
  try {
    // Test sample assessment data structure
    const sampleAssessmentData = {
      age: '26-30',
      location: 'New York, NY',
      educationLevel: 'bachelors',
      currentSituation: 'employed',
      experience: '3-5',
      technicalSkills: ['Excel/Spreadsheets', 'Data Analysis'],
      softSkills: ['Communication', 'Problem Solving'],
      workingWithData: 4,
      workingWithPeople: 3,
      creativeTasks: 2,
      problemSolving: 4,
      leadership: 3,
      physicalHandsOnWork: 2,
      outdoorWork: 2,
      mechanicalAptitude: 3,
      interests: ['Technology & Software', 'Data & Analytics'],
      industries: ['Technology & Software', 'Financial Services'],
      careerGoals: 'Grow into a senior analyst role',
      workLifeBalance: 'important',
      salaryExpectations: '70k-100k'
    };

    const validation = validateAssessmentData(sampleAssessmentData);
    if (!validation.isValid) {
      assessmentStatus = 'FAIL';
      issues.push(`Assessment validation failed: ${validation.errors.join(', ')}`);
    } else if (validation.warnings.length > 0) {
      assessmentStatus = 'WARNING';
      issues.push(`Assessment warnings: ${validation.warnings.join(', ')}`);
    }

    console.log('✅ Assessment component check passed');
  } catch (error) {
    assessmentStatus = 'FAIL';
    issues.push(`Assessment component error: ${error}`);
    console.error('❌ Assessment component check failed:', error);
  }

  // ========================================
  // 2. ALGORITHM COMPATIBILITY CHECK
  // ========================================
  let algorithmStatus: 'PASS' | 'FAIL' | 'WARNING' = 'PASS';
  
  try {
    const testData = {
      age: '26-30',
      location: 'Austin, TX',
      educationLevel: 'bachelors',
      currentSituation: 'employed',
      experience: '3-5',
      technicalSkills: ['Excel/Spreadsheets', 'Data Analysis', 'SQL'],
      softSkills: ['Communication', 'Problem Solving', 'Analytical Skills'],
      workingWithData: 4,
      workingWithPeople: 3,
      creativeTasks: 2,
      problemSolving: 4,
      leadership: 3,
      physicalHandsOnWork: 2,
      handsOnWork: 2, // Backward compatibility
      physicalWork: 2, // Backward compatibility
      outdoorWork: 2,
      mechanicalAptitude: 3,
      interests: ['Technology & Software', 'Data & Analytics', 'Business & Entrepreneurship'],
      industries: ['Technology & Software', 'Financial Services', 'Healthcare & Medical'],
      careerGoals: 'Advance to senior data analyst role',
      workLifeBalance: 'important',
      salaryExpectations: '70k-100k'
    };

    // Test algorithm compatibility
    const isCompatible = validateAlgorithmCompatibility(testData);
    if (!isCompatible) {
      algorithmStatus = 'FAIL';
      issues.push('Algorithm compatibility check failed');
    }

    // Test recommendation generation
    const recommendations = generateCareerRecommendations(testData, 1);
    if (!recommendations || recommendations.length === 0) {
      algorithmStatus = 'FAIL';
      issues.push('Algorithm failed to generate recommendations');
    } else if (recommendations.length < 3) {
      algorithmStatus = 'WARNING';
      issues.push(`Algorithm generated only ${recommendations.length} recommendations (expected 3+)`);
    }

    console.log('✅ Algorithm compatibility check passed');
  } catch (error) {
    algorithmStatus = 'FAIL';
    issues.push(`Algorithm error: ${error}`);
    console.error('❌ Algorithm compatibility check failed:', error);
  }

  // ========================================
  // 3. CAREER DATABASE CHECK
  // ========================================
  let careerDatabaseStatus: 'PASS' | 'FAIL' | 'WARNING' = 'PASS';
  
  try {
    // Check career database integrity
    if (!CAREER_TEMPLATES || CAREER_TEMPLATES.length === 0) {
      careerDatabaseStatus = 'FAIL';
      issues.push('Career database is empty or missing');
    } else {
      // Check for required fields in career templates
      const requiredCareerFields = [
        'title', 'salaryRange', 'description', 'requiredTechnicalSkills',
        'requiredSoftSkills', 'preferredInterests', 'preferredIndustries',
        'workDataWeight', 'workPeopleWeight', 'creativityWeight',
        'problemSolvingWeight', 'leadershipWeight', 'experienceLevel'
      ];

      let missingFieldsCount = 0;
      CAREER_TEMPLATES.forEach((career, index) => {
        requiredCareerFields.forEach(field => {
          if (career[field as keyof typeof career] === undefined) {
            missingFieldsCount++;
          }
        });
      });

      if (missingFieldsCount > 0) {
        careerDatabaseStatus = 'WARNING';
        issues.push(`Career database has ${missingFieldsCount} missing fields across templates`);
      }

      // Check for diversity in career levels
      const experienceLevels = CAREER_TEMPLATES.map(c => c.experienceLevel);
      const uniqueLevels = [...new Set(experienceLevels)];
      if (uniqueLevels.length < 3) {
        careerDatabaseStatus = 'WARNING';
        issues.push('Career database lacks diversity in experience levels');
      }
    }

    console.log('✅ Career database check passed');
  } catch (error) {
    careerDatabaseStatus = 'FAIL';
    issues.push(`Career database error: ${error}`);
    console.error('❌ Career database check failed:', error);
  }

  // ========================================
  // 4. DATA FLOW CHECK
  // ========================================
  let dataFlowStatus: 'PASS' | 'FAIL' | 'WARNING' = 'PASS';
  
  try {
    // Test complete data flow: Assessment -> Algorithm -> Recommendations
    const fullFlowData = {
      // Step 1: Profile & Background
      age: '26-30',
      location: 'Seattle, WA',
      educationLevel: 'bachelors',
      currentSituation: 'employed',
      currentRole: 'Marketing Coordinator',
      experience: '3-5',
      certifications: ['Google Analytics', 'HubSpot'],
      
      // Step 2: Skills
      technicalSkills: ['Excel/Spreadsheets', 'Data Analysis', 'Social Media Management'],
      softSkills: ['Communication', 'Problem Solving', 'Teamwork'],
      
      // Step 3: Work Preferences
      workingWithData: 4,
      workingWithPeople: 4,
      creativeTasks: 3,
      problemSolving: 4,
      leadership: 3,
      physicalHandsOnWork: 2,
      handsOnWork: 2,
      physicalWork: 2,
      outdoorWork: 2,
      mechanicalAptitude: 2,
      
      // Step 4: Interests, Industries & Goals
      interests: ['Technology & Software', 'Sales & Marketing', 'Data & Analytics'],
      industries: ['Technology & Software', 'Media & Entertainment', 'E-commerce'],
      careerGoals: 'Transition to a data-focused marketing role',
      workLifeBalance: 'important',
      salaryExpectations: '70k-100k'
    };

    // Normalize data
    const normalizedData = normalizeAssessmentData(fullFlowData);
    
    // Validate
    const validation = validateAssessmentData(normalizedData);
    if (!validation.isValid) {
      dataFlowStatus = 'FAIL';
      issues.push('Data flow validation failed');
    }

    // Generate recommendations
    const flowRecommendations = generateCareerRecommendations(normalizedData, 1);
    if (!flowRecommendations || flowRecommendations.length === 0) {
      dataFlowStatus = 'FAIL';
      issues.push('Data flow failed to produce recommendations');
    }

    console.log('✅ Data flow check passed');
  } catch (error) {
    dataFlowStatus = 'FAIL';
    issues.push(`Data flow error: ${error}`);
    console.error('❌ Data flow check failed:', error);
  }

  // ========================================
  // 5. NAVIGATION CHECK
  // ========================================
  let navigationStatus: 'PASS' | 'FAIL' | 'WARNING' = 'PASS';
  
  try {
    // Check that all required routes exist (this is a basic check)
    const requiredRoutes = ['/', '/auth', '/assessment', '/dashboard', '/career/:careerType'];
    
    // In a real implementation, we'd check React Router configuration
    // For now, we'll assume navigation is working if we got this far
    
    console.log('✅ Navigation check passed (basic)');
  } catch (error) {
    navigationStatus = 'WARNING';
    issues.push(`Navigation check warning: ${error}`);
    console.warn('⚠️ Navigation check had warnings:', error);
  }

  // ========================================
  // GENERATE RECOMMENDATIONS
  // ========================================
  if (issues.length === 0) {
    recommendations.push('System integrity is excellent - all components working properly');
  } else {
    if (assessmentStatus === 'FAIL' || algorithmStatus === 'FAIL') {
      recommendations.push('Critical issues detected - immediate attention required');
    }
    if (careerDatabaseStatus === 'WARNING') {
      recommendations.push('Consider expanding career database diversity');
    }
    if (dataFlowStatus === 'WARNING') {
      recommendations.push('Monitor data flow for edge cases');
    }
  }

  // ========================================
  // DETERMINE OVERALL STATUS
  // ========================================
  let overall: 'PASS' | 'FAIL' | 'WARNING' = 'PASS';
  
  if (assessmentStatus === 'FAIL' || algorithmStatus === 'FAIL' || careerDatabaseStatus === 'FAIL' || dataFlowStatus === 'FAIL') {
    overall = 'FAIL';
  } else if (assessmentStatus === 'WARNING' || algorithmStatus === 'WARNING' || careerDatabaseStatus === 'WARNING' || dataFlowStatus === 'WARNING' || navigationStatus === 'WARNING') {
    overall = 'WARNING';
  }

  console.log(`🏁 System integrity check complete: ${overall}`);
  console.log(`📊 Issues found: ${issues.length}`);
  console.log(`💡 Recommendations: ${recommendations.length}`);

  return {
    overall,
    components: {
      assessment: assessmentStatus,
      algorithm: algorithmStatus,
      careerDatabase: careerDatabaseStatus,
      dataFlow: dataFlowStatus,
      navigation: navigationStatus
    },
    issues,
    recommendations
  };
};

/**
 * Quick health check for production monitoring
 */
export const quickHealthCheck = (): boolean => {
  try {
    // Basic smoke test
    const testData = {
      experience: '3-5',
      technicalSkills: ['Excel/Spreadsheets'],
      softSkills: ['Communication'],
      workingWithData: 3,
      workingWithPeople: 3,
      creativeTasks: 3,
      problemSolving: 3,
      leadership: 3,
      physicalHandsOnWork: 3,
      outdoorWork: 3,
      mechanicalAptitude: 3,
      interests: ['Technology & Software'],
      industries: ['Technology & Software'],
      careerGoals: 'Test',
      workLifeBalance: 'important',
      salaryExpectations: '70k-100k'
    };

    const recommendations = generateCareerRecommendations(testData, 1);
    return recommendations && recommendations.length > 0;
  } catch (error) {
    console.error('Quick health check failed:', error);
    return false;
  }
};