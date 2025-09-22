#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * Convert a career type string to a human-readable title
 * e.g., "data-analyst" becomes "Data Analyst"
 */
function careerTypeToTitle(careerType) {
  return careerType
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

/**
 * Generate a placeholder CareerTemplate for a given career type
 */
function generatePlaceholderTemplate(careerType) {
  const title = careerTypeToTitle(careerType);
  
  return {
    title,
    salaryRange: "$50,000 - $80,000",
    description: `${title} role with opportunities for professional growth and development. This position involves working with various stakeholders to achieve organizational objectives.`,
    requiredTechnicalSkills: ["Industry Knowledge", "Professional Tools", "Communication"],
    requiredSoftSkills: ["Problem Solving", "Communication", "Teamwork", "Adaptability"],
    preferredInterests: ["Professional Development", "Industry Trends"],
    preferredIndustries: ["Various Industries"],
    workDataWeight: 3,
    workPeopleWeight: 3,
    creativityWeight: 3,
    problemSolvingWeight: 3,
    leadershipWeight: 3,
    learningPath: `${title} Professional Development Program (3-6 months)`,
    stretchLevel: "safe",
    careerType,
    requiresTechnical: true,
    companies: ["Various Companies", "Growing Organizations", "Industry Leaders"],
    dayInLife: `Professional activities including planning, execution, collaboration, and continuous learning in the ${title.toLowerCase()} field.`,
    experienceLevel: "mid",
    minYearsExperience: 2,
    maxYearsExperience: 8,
    salaryMin: 50000,
    salaryMax: 80000,
    remoteOptions: "Hybrid available",
    workEnvironments: ["office", "hybrid"],
    
    // Enhanced fields
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["Professional Certification", "Industry Standards"],
    requiredCertifications: [],
    workLifeBalanceRating: 3,
    agePreference: "25-45",
    locationFlexibility: "flexible",
    transitionFriendly: true,
    resumeKeywords: [title.toLowerCase(), "professional", "experience"],
    relatedJobTitles: [`Senior ${title}`, `${title} Specialist`, `${title} Coordinator`],
    valuedCompanies: ["Industry Leaders", "Growing Companies"],
    preferredIndustryExperience: ["Relevant industry experience"],
    careerProgressionPatterns: [`Junior ${title} → ${title} → Senior ${title}`],
    alternativeQualifications: ["Relevant experience", "Professional skills", "Industry knowledge"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    
    // Trades-specific fields
    handsOnWorkWeight: 3,
    physicalWorkWeight: 3,
    outdoorWorkWeight: 3,
    mechanicalAptitudeWeight: 3
  };
}

/**
 * Main function to generate placeholder templates
 */
async function main() {
  try {
    console.log('🚀 Starting placeholder template generation...');
    
    // Read the missing career templates JSON file
    const missingTemplatesPath = path.join(process.cwd(), 'missing_career_templates.json');
    console.log(`📖 Reading missing career templates from: ${missingTemplatesPath}`);
    
    if (!fs.existsSync(missingTemplatesPath)) {
      throw new Error(`Missing career templates file not found at: ${missingTemplatesPath}`);
    }
    
    const missingTemplatesData = fs.readFileSync(missingTemplatesPath, 'utf8');
    const missingCareerTypes = JSON.parse(missingTemplatesData);
    
    console.log(`📊 Found ${missingCareerTypes.length} missing career types`);
    
    // Generate placeholder templates for each missing career type
    const placeholderTemplates = [];
    
    for (const careerType of missingCareerTypes) {
      console.log(`🔧 Generating placeholder for: ${careerType}`);
      const template = generatePlaceholderTemplate(careerType);
      placeholderTemplates.push(template);
    }
    
    console.log(`✅ Generated ${placeholderTemplates.length} placeholder templates`);
    
    // Create the TypeScript file content
    const fileContent = `import { CareerTemplate } from './careerMatching';

export const placeholderTemplates: CareerTemplate[] = ${JSON.stringify(placeholderTemplates, null, 2)};
`;
    
    // Write the placeholder templates to the frontend utils directory
    const outputPath = path.join(process.cwd(), 'frontend', 'src', 'utils', 'placeholder_templates.ts');
    const outputDir = path.dirname(outputPath);
    
    // Ensure the output directory exists
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    console.log(`💾 Writing placeholder templates to: ${outputPath}`);
    fs.writeFileSync(outputPath, fileContent, 'utf8');
    
    console.log('🎉 Successfully generated placeholder_templates.ts!');
    console.log(`📈 Summary:`);
    console.log(`   - Input: ${missingCareerTypes.length} missing career types`);
    console.log(`   - Output: ${placeholderTemplates.length} placeholder templates`);
    console.log(`   - File: ${outputPath}`);
    
  } catch (error) {
    console.error('❌ Error generating placeholder templates:', error);
    process.exit(1);
  }
}

// Run the script if called directly
if (require.main === module) {
  main();
}