// Simple test to verify API integration
const testApiIntegration = async () => {
  try {
    console.log('🧪 Testing API integration...');
    
    // Test data similar to what the frontend sends
    const testData = {
      age: "25-34",
      location: "United States",
      educationLevel: "Bachelor's degree",
      currentSituation: "Employed full-time",
      experience: "5-10",
      technicalSkills: ["Python", "Data Analysis", "SQL"],
      softSkills: ["Communication", "Problem Solving", "Leadership"],
      workingWithData: 4,
      workingWithPeople: 3,
      creativeTasks: 2,
      problemSolving: 5,
      leadership: 3,
      interests: ["Technology", "Analytics", "Innovation"],
      industries: ["Technology", "Healthcare"],
      workEnvironment: "Remote",
      careerGoals: "Career advancement",
      workLifeBalance: "Very important",
      salaryExpectations: "$80,000 - $120,000",
      explorationLevel: 1
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
    console.log('✅ API Response received:', recommendations.length, 'recommendations');
    
    recommendations.forEach((rec, index) => {
      console.log(`${index + 1}. ${rec.title} (${rec.relevanceScore}% match)`);
    });

    return recommendations;
  } catch (error) {
    console.error('❌ API test failed:', error);
    return null;
  }
};

// Run the test
testApiIntegration();