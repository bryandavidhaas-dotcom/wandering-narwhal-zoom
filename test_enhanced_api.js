// Test the enhanced API with resume and LinkedIn data
const testEnhancedRecommendations = async () => {
  try {
    console.log('🧪 Testing enhanced API with resume and LinkedIn data...');
    
    // Test data with resume and LinkedIn information
    const testData = {
      age: "35-44",
      location: "San Francisco, CA",
      educationLevel: "Master's degree",
      currentSituation: "Employed full-time",
      experience: "10-15",
      
      // NEW: Resume text with technical skills and experience
      resumeText: `
        Senior Software Engineer with 12+ years of experience in Python, machine learning, and data analysis.
        Led a team of 8 engineers at Google, managed multiple projects using agile methodologies.
        Architected scalable microservices using AWS, Docker, and Kubernetes.
        Mentored junior developers and coordinated cross-functional initiatives.
        Experience in healthcare and fintech industries.
        Proficient in TensorFlow, pandas, SQL, React, and Node.js.
      `,
      
      // NEW: LinkedIn profile URL
      linkedinProfile: "https://linkedin.com/in/senior-engineer-profile",
      
      technicalSkills: ["Python", "Machine Learning", "SQL", "AWS"],
      softSkills: ["Leadership", "Communication", "Problem Solving"],
      workingWithData: 5,
      workingWithPeople: 4,
      creativeTasks: 3,
      problemSolving: 5,
      leadership: 5,
      interests: ["Technology", "AI", "Data Science"],
      industries: ["Technology", "Healthcare"],
      workEnvironment: "Hybrid",
      careerGoals: "Leadership role",
      workLifeBalance: "Important",
      salaryExpectations: "$150,000 - $200,000",
      explorationLevel: 2
    };

    const response = await fetch('http://localhost:8000/api/recommendations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(testData)
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }

    const recommendations = await response.json();
    console.log('✅ Enhanced API Response received:', recommendations.length, 'recommendations');
    
    recommendations.forEach((rec, index) => {
      console.log(`\n${index + 1}. ${rec.title} (${rec.relevanceScore}% match)`);
      console.log(`   Description: ${rec.description.substring(0, 100)}...`);
      console.log(`   Salary: ${rec.salaryRange}`);
      console.log(`   Match Reasons: ${rec.matchReasons.join(', ')}`);
      console.log(`   Companies: ${rec.companies.slice(0, 3).join(', ')}`);
    });

    return recommendations;
  } catch (error) {
    console.error('❌ Enhanced API test failed:', error);
    return null;
  }
};

// Test without resume/LinkedIn data for comparison
const testBasicRecommendations = async () => {
  try {
    console.log('\n🧪 Testing basic API without resume/LinkedIn data...');
    
    const basicData = {
      age: "35-44",
      location: "San Francisco, CA",
      educationLevel: "Master's degree",
      currentSituation: "Employed full-time",
      experience: "10-15",
      technicalSkills: ["Python", "Machine Learning", "SQL", "AWS"],
      softSkills: ["Leadership", "Communication", "Problem Solving"],
      workingWithData: 5,
      workingWithPeople: 4,
      creativeTasks: 3,
      problemSolving: 5,
      leadership: 5,
      interests: ["Technology", "AI", "Data Science"],
      industries: ["Technology", "Healthcare"],
      workEnvironment: "Hybrid",
      careerGoals: "Leadership role",
      workLifeBalance: "Important",
      salaryExpectations: "$150,000 - $200,000",
      explorationLevel: 2
    };

    const response = await fetch('http://localhost:8000/api/recommendations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(basicData)
    });

    const recommendations = await response.json();
    console.log('✅ Basic API Response received:', recommendations.length, 'recommendations');
    
    recommendations.forEach((rec, index) => {
      console.log(`\n${index + 1}. ${rec.title} (${rec.relevanceScore}% match)`);
      console.log(`   Match Reasons: ${rec.matchReasons.join(', ')}`);
    });

    return recommendations;
  } catch (error) {
    console.error('❌ Basic API test failed:', error);
    return null;
  }
};

// Run both tests
const runComparison = async () => {
  console.log('🔍 COMPARISON: Enhanced vs Basic Recommendations\n');
  console.log('=' .repeat(60));
  
  const enhanced = await testEnhancedRecommendations();
  console.log('\n' + '=' .repeat(60));
  const basic = await testBasicRecommendations();
  
  if (enhanced && basic) {
    console.log('\n📊 COMPARISON SUMMARY:');
    console.log('Enhanced recommendations should have:');
    console.log('- Higher relevance scores due to resume analysis');
    console.log('- More specific match reasons');
    console.log('- Better alignment with experience level');
    console.log('- Skills extracted from resume text');
  }
};

runComparison();