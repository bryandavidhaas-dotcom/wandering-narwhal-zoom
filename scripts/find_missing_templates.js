#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * Script to find missing career templates by comparing all_career_types.json
 * with the careerType values in frontend/src/utils/careerMatching.ts
 */

function readAllCareerTypes() {
  try {
    const filePath = path.join(process.cwd(), 'all_career_types.json');
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    const careerTypes = JSON.parse(fileContent);
    
    if (!Array.isArray(careerTypes)) {
      throw new Error('all_career_types.json should contain an array of career types');
    }
    
    console.log(`📋 Found ${careerTypes.length} career types in all_career_types.json`);
    return careerTypes;
  } catch (error) {
    console.error('❌ Error reading all_career_types.json:', error);
    process.exit(1);
  }
}

function extractCareerTypesFromMatching() {
  try {
    const filePath = path.join(process.cwd(), 'frontend/src/utils/careerMatching.ts');
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    
    // Extract careerType values from the careerTemplates array
    const careerTypeRegex = /careerType:\s*["']([^"']+)["']/g;
    const careerTypes = [];
    let match;
    
    while ((match = careerTypeRegex.exec(fileContent)) !== null) {
      careerTypes.push(match[1]);
    }
    
    // Remove duplicates
    const uniqueCareerTypes = [...new Set(careerTypes)];
    
    console.log(`🔍 Found ${uniqueCareerTypes.length} unique career types in careerMatching.ts`);
    console.log('📝 Sample career types from careerMatching.ts:', uniqueCareerTypes.slice(0, 5));
    
    return uniqueCareerTypes;
  } catch (error) {
    console.error('❌ Error reading careerMatching.ts:', error);
    process.exit(1);
  }
}

function findMissingCareerTypes(allCareerTypes, existingCareerTypes) {
  const existingSet = new Set(existingCareerTypes.map(type => type.toLowerCase()));
  
  const missingCareerTypes = allCareerTypes.filter(careerType => {
    // Handle the case where careerType might be a string like "Legal & Law"
    // Convert to kebab-case for comparison
    const normalizedCareerType = careerType.toLowerCase()
      .replace(/\s+&\s+/g, '-')
      .replace(/\s+/g, '-')
      .replace(/[^a-z0-9-]/g, '');
    
    // Check both original and normalized versions
    return !existingSet.has(careerType.toLowerCase()) && 
           !existingSet.has(normalizedCareerType);
  });
  
  console.log(`❌ Found ${missingCareerTypes.length} missing career types`);
  
  if (missingCareerTypes.length > 0) {
    console.log('📋 Sample missing career types:', missingCareerTypes.slice(0, 10));
  }
  
  return missingCareerTypes;
}

function writeMissingCareerTypes(missingCareerTypes) {
  try {
    const outputPath = path.join(process.cwd(), 'missing_career_templates.json');
    const jsonContent = JSON.stringify(missingCareerTypes, null, 2);
    
    fs.writeFileSync(outputPath, jsonContent, 'utf-8');
    
    console.log(`✅ Successfully wrote ${missingCareerTypes.length} missing career types to missing_career_templates.json`);
  } catch (error) {
    console.error('❌ Error writing missing_career_templates.json:', error);
    process.exit(1);
  }
}

function main() {
  console.log('🚀 Starting missing career templates analysis...\n');
  
  // Step 1: Read all career types from all_career_types.json
  const allCareerTypes = readAllCareerTypes();
  
  // Step 2: Extract career types from careerMatching.ts
  const existingCareerTypes = extractCareerTypesFromMatching();
  
  // Step 3: Find missing career types
  const missingCareerTypes = findMissingCareerTypes(allCareerTypes, existingCareerTypes);
  
  // Step 4: Write missing career types to JSON file
  writeMissingCareerTypes(missingCareerTypes);
  
  console.log('\n📊 Summary:');
  console.log(`   Total career types: ${allCareerTypes.length}`);
  console.log(`   Existing templates: ${existingCareerTypes.length}`);
  console.log(`   Missing templates: ${missingCareerTypes.length}`);
  console.log(`   Coverage: ${((existingCareerTypes.length / allCareerTypes.length) * 100).toFixed(1)}%`);
  
  if (missingCareerTypes.length === 0) {
    console.log('\n🎉 All career types have templates! No missing templates found.');
  } else {
    console.log(`\n⚠️  ${missingCareerTypes.length} career types are missing templates.`);
    console.log('📄 Check missing_career_templates.json for the complete list.');
  }
}

// Run the script
if (require.main === module) {
  main();
}