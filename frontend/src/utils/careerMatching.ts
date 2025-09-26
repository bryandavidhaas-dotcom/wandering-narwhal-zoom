// ========================================
// CRITICAL SAFETY GUARDRAILS - DO NOT REMOVE OR MODIFY WITHOUT REVIEW
// ========================================
//
// ⚠️  IMPORTANT SAFETY NOTICE ⚠️
//
// This file contains CRITICAL SAFETY GUARDRAILS that prevent the recommendation
// of dangerous career paths to users without proper qualifications.
//
// BEFORE MODIFYING ANY SAFETY-RELATED CODE, YOU MUST:
// 1. Understand that removing these guardrails could recommend life-threatening careers
//    (e.g., recommending Product Managers become Brain Surgeons or Nurse Anesthetists)
// 2. Get explicit approval from system architects and safety reviewers
// 3. Ensure any changes maintain or strengthen safety protections
// 4. Test thoroughly with safety-critical career scenarios
//
// KEY SAFETY FUNCTIONS (DO NOT REMOVE):
// - isSafetyCriticalCareer(): Identifies careers requiring specialized licensing
// - hasRelevantBackground(): Verifies users have appropriate experience
// - Safety filtering in Adventure Zone (lines ~1477-1482)
// - Stricter scoring for safety-critical careers (lines ~1778-1784)
//
// RATIONALE: Adventure Zone previously recommended a Product Manager become a
// Nurse Anesthetist (CRNA) - a role requiring 7+ years medical training and
// responsible for administering life-saving/life-threatening anesthesia.
//
// ========================================
// FIXED ADVENTURE ZONE FILTERING - ENSURES RELATED RECOMMENDATIONS
// ========================================

export interface CareerTemplate {
  title: string;
  salaryRange: string;
  description: string;
  requiredTechnicalSkills: string[];
  requiredSoftSkills: string[];
  preferredInterests: string[];
  preferredIndustries: string[];
  workDataWeight: number;
  workPeopleWeight: number;
  creativityWeight: number;
  problemSolvingWeight: number;
  leadershipWeight: number;
  learningPath: string;
  stretchLevel: string;
  careerType: string;
  requiresTechnical: boolean;
  companies: string[];
  dayInLife: string;
  experienceLevel: string;
  minYearsExperience: number;
  maxYearsExperience: number;
  salaryMin: number;
  salaryMax: number;
  remoteOptions: string;
  workEnvironments: string[];
  
  // Enhanced fields
  requiredEducation: string;
  preferredEducation: string;
  valuedCertifications: string[];
  requiredCertifications: string[];
  workLifeBalanceRating: number;
  agePreference: string;
  locationFlexibility: string;
  transitionFriendly: boolean;
  resumeKeywords: string[];
  relatedJobTitles: string[];
  valuedCompanies: string[];
  preferredIndustryExperience: string[];
  careerProgressionPatterns: string[];
  alternativeQualifications: string[];
  skillBasedEntry: boolean;
  experienceCanSubstitute: boolean;
  
  // Trades-specific fields
  handsOnWorkWeight: number;
  physicalWorkWeight: number;
  outdoorWorkWeight: number;
  mechanicalAptitudeWeight: number;
}

export interface CareerMatch extends CareerTemplate {
  relevanceScore: number;
  confidenceLevel: number;
  matchReasons: string[];
}

export interface UserAssessmentData {
  experience: string;
  technicalSkills: string[];
  softSkills: string[];
  workingWithData: number;
  workingWithPeople: number;
  creativeTasks: number;
  problemSolving: number;
  leadership: number;
  interests: string[];
  industries: string[];
  workEnvironment: string;
  salaryExpectations: string;
  careerGoals: string;
  age: string;
  location: string;
  educationLevel: string;
  certifications: string[];
  currentSituation: string;
  currentRole: string;
  resumeText: string;
  linkedinProfile: string;
  workLifeBalance: string;
  physicalHandsOnWork?: number;
  handsOnWork?: number;
  physicalWork?: number;
  outdoorWork?: number;
  mechanicalAptitude?: number;
  [key: string]: any;
}

// Import existing trades templates
import { TRADES_CAREER_TEMPLATES } from './tradesCareerTemplates';
import { placeholderTemplates } from './placeholder_templates';

// ========================================
// COMPREHENSIVE CAREER TEMPLATES - ALL EXPERIENCE LEVELS
// ========================================

const COMPREHENSIVE_CAREER_TEMPLATES: CareerTemplate[] = [
  // ========================================
  // EXECUTIVE LEVEL (15+ years) - C-Suite and VP Roles
  // ========================================
  {
    title: "Chief Executive Officer (CEO)",
    salaryRange: "$300,000 - $1,000,000+",
    description: "Lead entire organization, set strategic vision, manage board relationships, and drive company growth and performance",
    requiredTechnicalSkills: ["Strategic Planning", "Financial Management", "Business Development", "Market Analysis"],
    requiredSoftSkills: ["Executive Leadership", "Vision Setting", "Decision Making", "Communication"],
    preferredInterests: ["Business & Entrepreneurship", "Leadership", "Strategy"],
    preferredIndustries: ["Technology & Software", "Financial Services", "Healthcare & Medical"],
    workDataWeight: 4,
    workPeopleWeight: 5,
    creativityWeight: 4,
    problemSolvingWeight: 5,
    leadershipWeight: 5,
    learningPath: "Executive Leadership Development (12+ months)",
    stretchLevel: "safe",
    careerType: "chief-executive-officer",
    requiresTechnical: true,
    companies: ["Fortune 500 Companies", "High-Growth Startups", "Private Equity Portfolio Companies"],
    dayInLife: "Board meetings, strategic planning, investor relations, organizational leadership",
    experienceLevel: "executive",
    minYearsExperience: 20,
    maxYearsExperience: 40,
    salaryMin: 300000,
    salaryMax: 1000000,
    remoteOptions: "Limited - Executive presence required",
    workEnvironments: ["office", "hybrid"],
    requiredEducation: "masters",
    preferredEducation: "masters",
    valuedCertifications: ["MBA", "Executive Leadership"],
    requiredCertifications: [],
    workLifeBalanceRating: 1,
    agePreference: "40-60",
    locationFlexibility: "major-cities",
    transitionFriendly: false,
    resumeKeywords: ["CEO", "executive", "leadership", "strategy", "P&L"],
    relatedJobTitles: ["President", "Managing Director", "General Manager"],
    valuedCompanies: ["Fortune 500", "High-growth companies"],
    preferredIndustryExperience: ["Executive leadership", "P&L responsibility"],
    careerProgressionPatterns: ["VP → SVP → President → CEO"],
    alternativeQualifications: ["20+ years leadership", "P&L responsibility", "Board experience"],
    skillBasedEntry: false,
    experienceCanSubstitute: false,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 1
  },

  {
    title: "Chief Technology Officer (CTO)",
    salaryRange: "$250,000 - $500,000",
    description: "Lead technology strategy, oversee engineering teams, drive technical innovation and architecture decisions",
    requiredTechnicalSkills: ["Technology Strategy", "Software Architecture", "Engineering Management", "Cloud Platforms"],
    requiredSoftSkills: ["Technical Leadership", "Strategic Thinking", "Team Building", "Innovation"],
    preferredInterests: ["Technology & Software", "Innovation", "Engineering"],
    preferredIndustries: ["Technology & Software", "Financial Services", "E-commerce"],
    workDataWeight: 4,
    workPeopleWeight: 5,
    creativityWeight: 5,
    problemSolvingWeight: 5,
    leadershipWeight: 5,
    learningPath: "Executive Technology Leadership (8-12 months)",
    stretchLevel: "safe",
    careerType: "chief-technology-officer",
    requiresTechnical: true,
    companies: ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Uber"],
    dayInLife: "Technology strategy, engineering leadership, architecture decisions, innovation planning",
    experienceLevel: "executive",
    minYearsExperience: 18,
    maxYearsExperience: 30,
    salaryMin: 250000,
    salaryMax: 500000,
    remoteOptions: "Hybrid available",
    workEnvironments: ["office", "hybrid"],
    requiredEducation: "bachelors",
    preferredEducation: "masters",
    valuedCertifications: ["AWS", "Cloud Architecture", "Executive Leadership"],
    requiredCertifications: [],
    workLifeBalanceRating: 2,
    agePreference: "35-55",
    locationFlexibility: "major-cities",
    transitionFriendly: false,
    resumeKeywords: ["CTO", "technology strategy", "engineering leadership", "architecture"],
    relatedJobTitles: ["VP Engineering", "Head of Technology", "Chief Architect"],
    valuedCompanies: ["Google", "Microsoft", "Amazon", "Tech Companies"],
    preferredIndustryExperience: ["Technology leadership", "Engineering management"],
    careerProgressionPatterns: ["Senior Engineer → Engineering Manager → VP Engineering → CTO"],
    alternativeQualifications: ["18+ years tech experience", "Engineering leadership", "Architecture expertise"],
    skillBasedEntry: false,
    experienceCanSubstitute: false,
    handsOnWorkWeight: 2,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 3
  },

  {
    title: "VP of Product Management",
    salaryRange: "$200,000 - $350,000",
    description: "Lead product strategy across multiple product lines, manage senior product managers, drive product vision",
    requiredTechnicalSkills: ["Product Strategy", "Data Analysis", "User Research", "Product Management"],
    requiredSoftSkills: ["Leadership", "Strategic Thinking", "Communication", "Mentoring"],
    preferredInterests: ["Technology & Software", "Business & Entrepreneurship", "Innovation"],
    preferredIndustries: ["Technology & Software", "Financial Services", "E-commerce"],
    workDataWeight: 4,
    workPeopleWeight: 5,
    creativityWeight: 4,
    problemSolvingWeight: 5,
    leadershipWeight: 5,
    learningPath: "Executive Product Leadership (6-8 months)",
    stretchLevel: "safe",
    careerType: "vp-product-management",
    requiresTechnical: true,
    companies: ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Spotify"],
    dayInLife: "Product strategy, team leadership, stakeholder management, roadmap planning",
    experienceLevel: "executive",
    minYearsExperience: 15,
    maxYearsExperience: 25,
    salaryMin: 200000,
    salaryMax: 350000,
    remoteOptions: "Hybrid available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "masters",
    valuedCertifications: ["Product Management", "MBA", "Agile/Scrum"],
    requiredCertifications: [],
    workLifeBalanceRating: 2,
    agePreference: "35-50",
    locationFlexibility: "flexible",
    transitionFriendly: false,
    resumeKeywords: ["VP product", "product strategy", "product leadership", "roadmap"],
    relatedJobTitles: ["Director of Product", "Head of Product", "Senior Product Manager"],
    valuedCompanies: ["Google", "Microsoft", "Amazon", "Meta"],
    preferredIndustryExperience: ["Product management", "Technology"],
    careerProgressionPatterns: ["PM → Senior PM → Director → VP"],
    alternativeQualifications: ["15+ years product experience", "Team leadership", "Strategic thinking"],
    skillBasedEntry: false,
    experienceCanSubstitute: false,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 1
  },

  {
    title: "VP of Sales",
    salaryRange: "$180,000 - $300,000",
    description: "Lead sales organization, develop sales strategy, manage enterprise accounts and sales teams",
    requiredTechnicalSkills: ["Sales Strategy", "CRM Systems", "Sales Analytics", "Revenue Operations"],
    requiredSoftSkills: ["Leadership", "Negotiation", "Communication", "Strategic Thinking"],
    preferredInterests: ["Sales & Marketing", "Business & Entrepreneurship", "Leadership"],
    preferredIndustries: ["Technology & Software", "Financial Services", "Manufacturing"],
    workDataWeight: 3,
    workPeopleWeight: 5,
    creativityWeight: 3,
    problemSolvingWeight: 4,
    leadershipWeight: 5,
    learningPath: "Executive Sales Leadership (4-6 months)",
    stretchLevel: "safe",
    careerType: "vp-sales",
    requiresTechnical: true,
    companies: ["Salesforce", "Oracle", "Microsoft", "IBM", "Enterprise Software Companies"],
    dayInLife: "Sales strategy, team leadership, enterprise deals, revenue planning",
    experienceLevel: "executive",
    minYearsExperience: 15,
    maxYearsExperience: 25,
    salaryMin: 180000,
    salaryMax: 300000,
    remoteOptions: "Hybrid available",
    workEnvironments: ["office", "hybrid", "travel"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["Sales Leadership", "CRM", "Negotiation"],
    requiredCertifications: [],
    workLifeBalanceRating: 2,
    agePreference: "35-55",
    locationFlexibility: "flexible",
    transitionFriendly: true,
    resumeKeywords: ["VP sales", "sales leadership", "revenue", "enterprise sales"],
    relatedJobTitles: ["Sales Director", "Head of Sales", "Chief Revenue Officer"],
    valuedCompanies: ["Salesforce", "Oracle", "Microsoft", "Enterprise Companies"],
    preferredIndustryExperience: ["Sales leadership", "Enterprise sales"],
    careerProgressionPatterns: ["Sales Rep → Sales Manager → Sales Director → VP Sales"],
    alternativeQualifications: ["15+ years sales experience", "Team leadership", "Revenue responsibility"],
    skillBasedEntry: false,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 2,
    mechanicalAptitudeWeight: 1
  },

  // ========================================
  // SENIOR LEVEL (10-15 years) - Director and Senior Manager Roles
  // ========================================
  {
    title: "Director of Engineering",
    salaryRange: "$160,000 - $220,000",
    description: "Lead engineering teams, set technical direction, manage software development lifecycle and engineering culture",
    requiredTechnicalSkills: ["Software Engineering", "System Architecture", "Team Management", "Agile/Scrum"],
    requiredSoftSkills: ["Technical Leadership", "Team Building", "Communication", "Strategic Thinking"],
    preferredInterests: ["Technology & Software", "Engineering", "Leadership"],
    preferredIndustries: ["Technology & Software", "Financial Services", "E-commerce"],
    workDataWeight: 3,
    workPeopleWeight: 5,
    creativityWeight: 4,
    problemSolvingWeight: 5,
    leadershipWeight: 5,
    learningPath: "Engineering Leadership Program (4-6 months)",
    stretchLevel: "safe",
    careerType: "director-engineering",
    requiresTechnical: true,
    companies: ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Uber"],
    dayInLife: "Team leadership, technical strategy, architecture decisions, hiring and mentoring",
    experienceLevel: "senior",
    minYearsExperience: 10,
    maxYearsExperience: 18,
    salaryMin: 160000,
    salaryMax: 220000,
    remoteOptions: "Hybrid available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["AWS", "Leadership", "Agile/Scrum"],
    requiredCertifications: [],
    workLifeBalanceRating: 3,
    agePreference: "32-50",
    locationFlexibility: "flexible",
    transitionFriendly: true,
    resumeKeywords: ["director engineering", "engineering manager", "technical leadership"],
    relatedJobTitles: ["Engineering Manager", "Head of Engineering", "VP Engineering"],
    valuedCompanies: ["Google", "Microsoft", "Amazon", "Tech Companies"],
    preferredIndustryExperience: ["Software engineering", "Technical leadership"],
    careerProgressionPatterns: ["Senior Engineer → Engineering Manager → Director"],
    alternativeQualifications: ["10+ years engineering", "Team leadership", "Technical expertise"],
    skillBasedEntry: false,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 2,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 3
  },

  {
    title: "Director of Product Management",
    salaryRange: "$150,000 - $200,000",
    description: "Lead product management organization, drive product strategy, manage multiple product lines",
    requiredTechnicalSkills: ["Product Strategy", "Data Analysis", "User Research", "Product Management"],
    requiredSoftSkills: ["Leadership", "Strategic Thinking", "Communication", "Team Management"],
    preferredInterests: ["Technology & Software", "Business & Entrepreneurship", "Innovation"],
    preferredIndustries: ["Technology & Software", "Financial Services", "E-commerce"],
    workDataWeight: 4,
    workPeopleWeight: 5,
    creativityWeight: 4,
    problemSolvingWeight: 5,
    leadershipWeight: 5,
    learningPath: "Product Leadership Program (4-6 months)",
    stretchLevel: "safe",
    careerType: "director-product-management",
    requiresTechnical: true,
    companies: ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Spotify"],
    dayInLife: "Product strategy, team leadership, roadmap planning, stakeholder management",
    experienceLevel: "senior",
    minYearsExperience: 10,
    maxYearsExperience: 18,
    salaryMin: 150000,
    salaryMax: 200000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "masters",
    valuedCertifications: ["Product Management", "Agile/Scrum", "MBA"],
    requiredCertifications: [],
    workLifeBalanceRating: 3,
    agePreference: "32-48",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["director product", "product strategy", "product leadership"],
    relatedJobTitles: ["Senior Product Manager", "Head of Product", "VP Product"],
    valuedCompanies: ["Google", "Microsoft", "Amazon", "Meta"],
    preferredIndustryExperience: ["Product management", "Technology"],
    careerProgressionPatterns: ["PM → Senior PM → Director → VP"],
    alternativeQualifications: ["10+ years product experience", "Team leadership", "Strategic thinking"],
    skillBasedEntry: false,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 1
  },

  {
    title: "Head of Product",
    salaryRange: "$180,000 - $250,000",
    description: "Lead product organization, set product vision and strategy, manage senior product managers across multiple product lines",
    requiredTechnicalSkills: ["Product Strategy", "Data Analysis", "User Research", "Product Management", "Roadmap Planning"],
    requiredSoftSkills: ["Executive Leadership", "Strategic Thinking", "Communication", "Team Building", "Vision Setting"],
    preferredInterests: ["Technology & Software", "Business & Entrepreneurship", "Innovation", "Leadership"],
    preferredIndustries: ["Technology & Software", "Financial Services", "E-commerce", "SaaS"],
    workDataWeight: 4,
    workPeopleWeight: 5,
    creativityWeight: 4,
    problemSolvingWeight: 5,
    leadershipWeight: 5,
    learningPath: "Head of Product Program (4-8 months)",
    stretchLevel: "safe",
    careerType: "head-of-product",
    requiresTechnical: true,
    companies: ["Airbnb", "Uber", "Stripe", "Slack", "Zoom", "Dropbox", "Google", "Microsoft", "Amazon", "Meta"],
    dayInLife: "Strategic product planning, team leadership, stakeholder management, product vision development",
    experienceLevel: "senior",
    minYearsExperience: 12,
    maxYearsExperience: 20,
    salaryMin: 180000,
    salaryMax: 250000,
    remoteOptions: "Hybrid available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "masters",
    valuedCertifications: ["Product Management", "MBA", "Agile/Scrum", "Leadership"],
    requiredCertifications: [],
    workLifeBalanceRating: 2,
    agePreference: "35-50",
    locationFlexibility: "flexible",
    transitionFriendly: false,
    resumeKeywords: ["head of product", "product leadership", "product strategy", "product vision", "team leadership"],
    relatedJobTitles: ["VP Product", "Director of Product", "Chief Product Officer", "Senior Product Manager"],
    valuedCompanies: ["Airbnb", "Uber", "Stripe", "Slack", "Zoom", "Dropbox"],
    preferredIndustryExperience: ["Product management", "Technology", "SaaS"],
    careerProgressionPatterns: ["Senior PM → Principal PM → Director → Head of Product → VP Product"],
    alternativeQualifications: ["12+ years product experience", "Team leadership", "Strategic product thinking"],
    skillBasedEntry: false,
    experienceCanSubstitute: false,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 1
  },

  {
    title: "Senior Data Science Manager",
    salaryRange: "$140,000 - $190,000",
    description: "Lead data science teams, drive analytics strategy, manage machine learning initiatives",
    requiredTechnicalSkills: ["Machine Learning", "Python", "SQL", "Data Strategy", "Team Management"],
    requiredSoftSkills: ["Leadership", "Communication", "Strategic Thinking", "Mentoring"],
    preferredInterests: ["Data & Analytics", "Technology & Software", "Research"],
    preferredIndustries: ["Technology & Software", "Financial Services", "Healthcare & Medical"],
    workDataWeight: 5,
    workPeopleWeight: 4,
    creativityWeight: 4,
    problemSolvingWeight: 5,
    leadershipWeight: 4,
    learningPath: "Data Science Leadership (4-6 months)",
    stretchLevel: "safe",
    careerType: "senior-data-science-manager",
    requiresTechnical: true,
    companies: ["Google", "Microsoft", "Netflix", "Uber", "Airbnb", "Meta"],
    dayInLife: "Team leadership, data strategy, model review, stakeholder management",
    experienceLevel: "senior",
    minYearsExperience: 10,
    maxYearsExperience: 18,
    salaryMin: 140000,
    salaryMax: 190000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "masters",
    preferredEducation: "masters",
    valuedCertifications: ["Machine Learning", "AWS", "Leadership"],
    requiredCertifications: [],
    workLifeBalanceRating: 4,
    agePreference: "30-45",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["data science manager", "machine learning", "analytics leadership"],
    relatedJobTitles: ["Data Science Lead", "Principal Data Scientist", "Head of Analytics"],
    valuedCompanies: ["Google", "Microsoft", "Netflix", "Tech Companies"],
    preferredIndustryExperience: ["Data science", "Analytics", "Machine learning"],
    careerProgressionPatterns: ["Data Scientist → Senior DS → DS Manager → Director"],
    alternativeQualifications: ["10+ years data science", "Team leadership", "ML expertise"],
    skillBasedEntry: false,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 2
  },

  {
    title: "Sales Director",
    salaryRange: "$120,000 - $180,000",
    description: "Lead regional sales teams, manage enterprise accounts, drive revenue growth and sales strategy",
    requiredTechnicalSkills: ["Sales Management", "CRM Systems", "Sales Analytics", "Territory Management"],
    requiredSoftSkills: ["Leadership", "Negotiation", "Communication", "Strategic Thinking"],
    preferredInterests: ["Sales & Marketing", "Business & Entrepreneurship", "Leadership"],
    preferredIndustries: ["Technology & Software", "Financial Services", "Manufacturing"],
    workDataWeight: 3,
    workPeopleWeight: 5,
    creativityWeight: 3,
    problemSolvingWeight: 4,
    leadershipWeight: 5,
    learningPath: "Sales Leadership Development (3-4 months)",
    stretchLevel: "safe",
    careerType: "sales-director",
    requiresTechnical: true,
    companies: ["Salesforce", "Oracle", "Microsoft", "IBM", "Enterprise Companies"],
    dayInLife: "Team leadership, enterprise sales, strategy development, performance management",
    experienceLevel: "senior",
    minYearsExperience: 10,
    maxYearsExperience: 18,
    salaryMin: 120000,
    salaryMax: 180000,
    remoteOptions: "Hybrid available",
    workEnvironments: ["office", "hybrid", "travel"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["Sales Leadership", "CRM", "Negotiation"],
    requiredCertifications: [],
    workLifeBalanceRating: 3,
    agePreference: "32-50",
    locationFlexibility: "flexible",
    transitionFriendly: true,
    resumeKeywords: ["sales director", "sales management", "enterprise sales", "revenue"],
    relatedJobTitles: ["Sales Manager", "Regional Sales Manager", "VP Sales"],
    valuedCompanies: ["Salesforce", "Oracle", "Microsoft", "Enterprise Companies"],
    preferredIndustryExperience: ["Sales", "Account management", "Business development"],
    careerProgressionPatterns: ["Sales Rep → Sales Manager → Sales Director → VP Sales"],
    alternativeQualifications: ["10+ years sales", "Team leadership", "Revenue responsibility"],
    skillBasedEntry: false,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 2,
    mechanicalAptitudeWeight: 1
  },

  // ========================================
  // MID-LEVEL (5-10 years) - Senior Individual Contributors and Managers
  // ========================================
  {
    title: "Senior Product Manager",
    salaryRange: "$120,000 - $160,000",
    description: "Lead complex product initiatives, mentor junior PMs, drive product strategy for major features",
    requiredTechnicalSkills: ["Product Management", "Data Analysis", "User Research", "Agile/Scrum"],
    requiredSoftSkills: ["Leadership", "Communication", "Strategic Thinking", "Problem Solving"],
    preferredInterests: ["Technology & Software", "Business & Entrepreneurship", "Innovation"],
    preferredIndustries: ["Technology & Software", "Financial Services", "E-commerce"],
    workDataWeight: 4,
    workPeopleWeight: 5,
    creativityWeight: 4,
    problemSolvingWeight: 5,
    leadershipWeight: 4,
    learningPath: "Advanced Product Management (3-4 months)",
    stretchLevel: "safe",
    careerType: "senior-product-manager",
    requiresTechnical: true,
    companies: ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Spotify"],
    dayInLife: "Product strategy, stakeholder management, data analysis, team collaboration",
    experienceLevel: "mid",
    minYearsExperience: 5,
    maxYearsExperience: 12,
    salaryMin: 120000,
    salaryMax: 160000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["Product Management", "Agile/Scrum", "Google Analytics"],
    requiredCertifications: [],
    workLifeBalanceRating: 3,
    agePreference: "28-42",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["senior product manager", "product strategy", "roadmap", "leadership"],
    relatedJobTitles: ["Product Manager", "Principal Product Manager", "Director Product"],
    valuedCompanies: ["Google", "Microsoft", "Amazon", "Meta"],
    preferredIndustryExperience: ["Product management", "Technology", "Business analysis"],
    careerProgressionPatterns: ["PM → Senior PM → Principal PM → Director"],
    alternativeQualifications: ["5+ years product experience", "Leadership skills", "Strategic thinking"],
    skillBasedEntry: false,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 1
  },

  {
    title: "Senior Software Engineer",
    salaryRange: "$110,000 - $150,000",
    description: "Design and build complex software systems, mentor junior engineers, lead technical initiatives",
    requiredTechnicalSkills: ["Software Development", "System Design", "Programming Languages", "Architecture"],
    requiredSoftSkills: ["Problem Solving", "Communication", "Mentoring", "Technical Leadership"],
    preferredInterests: ["Technology & Software", "Engineering", "Problem Solving"],
    preferredIndustries: ["Technology & Software", "Financial Services", "E-commerce"],
    workDataWeight: 3,
    workPeopleWeight: 3,
    creativityWeight: 4,
    problemSolvingWeight: 5,
    leadershipWeight: 3,
    learningPath: "Advanced Software Engineering (4-6 months)",
    stretchLevel: "safe",
    careerType: "senior-software-engineer",
    requiresTechnical: true,
    companies: ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Uber"],
    dayInLife: "Software development, system design, code review, mentoring junior engineers",
    experienceLevel: "mid",
    minYearsExperience: 5,
    maxYearsExperience: 12,
    salaryMin: 110000,
    salaryMax: 150000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["AWS", "Cloud Platforms", "Programming Languages"],
    requiredCertifications: [],
    workLifeBalanceRating: 4,
    agePreference: "26-40",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["senior software engineer", "software development", "programming", "architecture"],
    relatedJobTitles: ["Software Engineer", "Principal Engineer", "Staff Engineer"],
    valuedCompanies: ["Google", "Microsoft", "Amazon", "Tech Companies"],
    preferredIndustryExperience: ["Software engineering", "Technology"],
    careerProgressionPatterns: ["Engineer → Senior Engineer → Staff Engineer → Principal"],
    alternativeQualifications: ["5+ years engineering", "Technical expertise", "System design skills"],
    skillBasedEntry: false,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 2,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 3
  },

  {
    title: "Senior Data Scientist",
    salaryRange: "$115,000 - $155,000",
    description: "Build advanced machine learning models, lead analytics projects, mentor junior data scientists",
    requiredTechnicalSkills: ["Machine Learning", "Python", "SQL", "Statistical Analysis", "Data Visualization"],
    requiredSoftSkills: ["Problem Solving", "Communication", "Mentoring", "Critical Thinking"],
    preferredInterests: ["Data & Analytics", "Technology & Software", "Research"],
    preferredIndustries: ["Technology & Software", "Financial Services", "Healthcare & Medical"],
    workDataWeight: 5,
    workPeopleWeight: 3,
    creativityWeight: 4,
    problemSolvingWeight: 5,
    leadershipWeight: 3,
    learningPath: "Advanced Data Science (4-6 months)",
    stretchLevel: "safe",
    careerType: "senior-data-scientist",
    requiresTechnical: true,
    companies: ["Google", "Microsoft", "Netflix", "Uber", "Airbnb", "Meta"],
    dayInLife: "Advanced modeling, research, mentoring, stakeholder presentations",
    experienceLevel: "mid",
    minYearsExperience: 5,
    maxYearsExperience: 12,
    salaryMin: 115000,
    salaryMax: 155000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "masters",
    preferredEducation: "masters",
    valuedCertifications: ["Machine Learning", "Python", "AWS", "Google Cloud"],
    requiredCertifications: [],
    workLifeBalanceRating: 4,
    agePreference: "28-42",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["senior data scientist", "machine learning", "python", "analytics"],
    relatedJobTitles: ["Data Scientist", "Principal Data Scientist", "ML Engineer"],
    valuedCompanies: ["Google", "Microsoft", "Netflix", "Tech Companies"],
    preferredIndustryExperience: ["Data science", "Analytics", "Research"],
    careerProgressionPatterns: ["Data Scientist → Senior DS → Principal DS → DS Manager"],
    alternativeQualifications: ["5+ years data science", "ML expertise", "Python proficiency"],
    skillBasedEntry: false,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 2
  },

  {
    title: "Engineering Manager",
    salaryRange: "$130,000 - $170,000",
    description: "Lead engineering teams, manage software development processes, drive technical and people management",
    requiredTechnicalSkills: ["Software Engineering", "Team Management", "Agile/Scrum", "System Architecture"],
    requiredSoftSkills: ["Leadership", "Communication", "Team Building", "Strategic Thinking"],
    preferredInterests: ["Technology & Software", "Leadership", "Team Management"],
    preferredIndustries: ["Technology & Software", "Financial Services", "E-commerce"],
    workDataWeight: 3,
    workPeopleWeight: 5,
    creativityWeight: 3,
    problemSolvingWeight: 4,
    leadershipWeight: 5,
    learningPath: "Engineering Management Program (3-4 months)",
    stretchLevel: "safe",
    careerType: "engineering-manager",
    requiresTechnical: true,
    companies: ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Uber"],
    dayInLife: "Team leadership, 1-on-1s, technical planning, hiring and performance management",
    experienceLevel: "mid",
    minYearsExperience: 6,
    maxYearsExperience: 12,
    salaryMin: 130000,
    salaryMax: 170000,
    remoteOptions: "Hybrid available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["Leadership", "Agile/Scrum", "AWS"],
    requiredCertifications: [],
    workLifeBalanceRating: 3,
    agePreference: "30-45",
    locationFlexibility: "flexible",
    transitionFriendly: true,
    resumeKeywords: ["engineering manager", "team leadership", "software engineering", "management"],
    relatedJobTitles: ["Senior Software Engineer", "Director of Engineering", "Technical Lead"],
    valuedCompanies: ["Google", "Microsoft", "Amazon", "Tech Companies"],
    preferredIndustryExperience: ["Software engineering", "Technical leadership"],
    careerProgressionPatterns: ["Senior Engineer → Engineering Manager → Director"],
    alternativeQualifications: ["6+ years engineering", "Leadership experience", "Team management"],
    skillBasedEntry: false,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 2,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 3
  },

  // ========================================
  // MID-LEVEL CONTINUED (3-8 years) - Core Professional Roles
  // ========================================
  {
    title: "Product Manager",
    salaryRange: "$90,000 - $130,000",
    description: "Own product roadmap and strategy, work with engineering teams, drive product success through data-driven decisions",
    requiredTechnicalSkills: ["Product Management", "Data Analysis", "User Research", "Agile/Scrum"],
    requiredSoftSkills: ["Communication", "Strategic Thinking", "Problem Solving", "Leadership"],
    preferredInterests: ["Technology & Software", "Business & Entrepreneurship", "Innovation"],
    preferredIndustries: ["Technology & Software", "Financial Services", "E-commerce"],
    workDataWeight: 4,
    workPeopleWeight: 4,
    creativityWeight: 4,
    problemSolvingWeight: 5,
    leadershipWeight: 3,
    learningPath: "Product Management Certification (3-4 months)",
    stretchLevel: "safe",
    careerType: "product-manager",
    requiresTechnical: true,
    companies: ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Spotify"],
    dayInLife: "Product strategy, stakeholder meetings, data analysis, roadmap planning",
    experienceLevel: "mid",
    minYearsExperience: 3,
    maxYearsExperience: 8,
    salaryMin: 90000,
    salaryMax: 130000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["Product Management", "Agile/Scrum", "Google Analytics"],
    requiredCertifications: [],
    workLifeBalanceRating: 3,
    agePreference: "25-38",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["product manager", "product strategy", "roadmap", "user research"],
    relatedJobTitles: ["Associate Product Manager", "Business Analyst", "Senior Product Manager"],
    valuedCompanies: ["Google", "Microsoft", "Amazon", "Meta"],
    preferredIndustryExperience: ["Product management", "Business analysis", "Technology"],
    careerProgressionPatterns: ["Business Analyst → PM → Senior PM → Director"],
    alternativeQualifications: ["3+ years relevant experience", "Analytical skills", "Strategic thinking"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 1
  },

  {
    title: "Data Scientist",
    salaryRange: "$95,000 - $135,000",
    description: "Build machine learning models, analyze complex datasets, provide data-driven insights for business decisions",
    requiredTechnicalSkills: ["Python", "SQL", "Machine Learning", "Statistical Analysis", "Data Visualization"],
    requiredSoftSkills: ["Problem Solving", "Communication", "Critical Thinking", "Collaboration"],
    preferredInterests: ["Data & Analytics", "Technology & Software", "Research"],
    preferredIndustries: ["Technology & Software", "Financial Services", "Healthcare & Medical"],
    workDataWeight: 5,
    workPeopleWeight: 3,
    creativityWeight: 3,
    problemSolvingWeight: 5,
    leadershipWeight: 2,
    learningPath: "Data Science Bootcamp (4-6 months)",
    stretchLevel: "safe",
    careerType: "data-scientist",
    requiresTechnical: true,
    companies: ["Google", "Microsoft", "Netflix", "Uber", "Airbnb", "Meta"],
    dayInLife: "Model building, data analysis, stakeholder presentations, research",
    experienceLevel: "mid",
    minYearsExperience: 3,
    maxYearsExperience: 8,
    salaryMin: 95000,
    salaryMax: 135000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "masters",
    valuedCertifications: ["Machine Learning", "Python", "AWS", "Google Cloud"],
    requiredCertifications: [],
    workLifeBalanceRating: 4,
    agePreference: "25-38",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["data scientist", "machine learning", "python", "analytics", "sql"],
    relatedJobTitles: ["Data Analyst", "ML Engineer", "Research Scientist"],
    valuedCompanies: ["Google", "Microsoft", "Netflix", "Tech Companies"],
    preferredIndustryExperience: ["Data analysis", "Research", "Analytics"],
    careerProgressionPatterns: ["Data Analyst → Data Scientist → Senior DS → Principal DS"],
    alternativeQualifications: ["3+ years data experience", "ML skills", "Python proficiency"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 2
  },

  {
    title: "Software Engineer",
    salaryRange: "$85,000 - $120,000",
    description: "Design, develop, and maintain software applications, collaborate with cross-functional teams",
    requiredTechnicalSkills: ["Programming Languages", "Software Development", "Version Control", "Testing"],
    requiredSoftSkills: ["Problem Solving", "Communication", "Collaboration", "Learning Agility"],
    preferredInterests: ["Technology & Software", "Engineering", "Problem Solving"],
    preferredIndustries: ["Technology & Software", "Financial Services", "E-commerce"],
    workDataWeight: 3,
    workPeopleWeight: 3,
    creativityWeight: 4,
    problemSolvingWeight: 5,
    leadershipWeight: 2,
    learningPath: "Software Engineering Bootcamp (3-6 months)",
    stretchLevel: "safe",
    careerType: "software-engineer",
    requiresTechnical: true,
    companies: ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Uber"],
    dayInLife: "Software development, code review, debugging, feature implementation",
    experienceLevel: "mid",
    minYearsExperience: 2,
    maxYearsExperience: 8,
    salaryMin: 85000,
    salaryMax: 120000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["AWS", "Programming Languages", "Cloud Platforms"],
    requiredCertifications: [],
    workLifeBalanceRating: 4,
    agePreference: "22-35",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["software engineer", "programming", "development", "coding"],
    relatedJobTitles: ["Junior Software Engineer", "Senior Software Engineer", "Full Stack Developer"],
    valuedCompanies: ["Google", "Microsoft", "Amazon", "Tech Companies"],
    preferredIndustryExperience: ["Software development", "Technology"],
    careerProgressionPatterns: ["Junior Engineer → Software Engineer → Senior Engineer"],
    alternativeQualifications: ["2+ years programming", "CS degree or bootcamp", "Technical skills"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 2,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 3
  },

  {
    title: "Business Analyst",
    salaryRange: "$65,000 - $95,000",
    description: "Bridge business needs and technical solutions, analyze processes, recommend improvements",
    requiredTechnicalSkills: ["Excel/Spreadsheets", "Data Analysis", "Business Intelligence (BI)", "SQL"],
    requiredSoftSkills: ["Problem Solving", "Critical Thinking", "Communication", "Strategic Thinking"],
    preferredInterests: ["Business & Entrepreneurship", "Data & Analytics", "Consulting"],
    preferredIndustries: ["Technology & Software", "Financial Services", "Healthcare & Medical", "Consulting & Professional Services"],
    workDataWeight: 4,
    workPeopleWeight: 4,
    creativityWeight: 2,
    problemSolvingWeight: 5,
    leadershipWeight: 3,
    learningPath: "Business Analysis Certification (2-3 months)",
    stretchLevel: "safe",
    careerType: "business-analyst",
    requiresTechnical: true,
    companies: ["Deloitte", "Accenture", "PwC", "IBM", "Microsoft", "Oracle"],
    dayInLife: "Requirements gathering, data analysis, stakeholder meetings, process improvement",
    experienceLevel: "mid",
    minYearsExperience: 2,
    maxYearsExperience: 8,
    salaryMin: 65000,
    salaryMax: 95000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["Business Analysis", "Six Sigma", "Agile/Scrum"],
    requiredCertifications: [],
    workLifeBalanceRating: 4,
    agePreference: "24-38",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["business analyst", "requirements", "process improvement", "data analysis"],
    relatedJobTitles: ["Data Analyst", "Systems Analyst", "Product Manager"],
    valuedCompanies: ["Deloitte", "Accenture", "PwC", "Consulting Firms"],
    preferredIndustryExperience: ["Business analysis", "Consulting", "Process improvement"],
    careerProgressionPatterns: ["Analyst → Business Analyst → Senior BA → Manager"],
    alternativeQualifications: ["2+ years analytical experience", "Process improvement skills", "Business acumen"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 1
  },

  {
    title: "UX Designer",
    salaryRange: "$70,000 - $105,000",
    description: "Design user experiences, conduct user research, create wireframes and prototypes",
    requiredTechnicalSkills: ["Figma", "Adobe Creative Suite", "User Research", "Prototyping"],
    requiredSoftSkills: ["Creativity", "Communication", "Problem Solving", "Empathy"],
    preferredInterests: ["Creative Arts & Design", "Technology & Software", "User Experience"],
    preferredIndustries: ["Technology & Software", "Design Agencies", "E-commerce"],
    workDataWeight: 2,
    workPeopleWeight: 4,
    creativityWeight: 5,
    problemSolvingWeight: 4,
    leadershipWeight: 2,
    learningPath: "UX Design Bootcamp (3-6 months)",
    stretchLevel: "safe",
    careerType: "ux-designer",
    requiresTechnical: true,
    companies: ["Google", "Microsoft", "Amazon", "Meta", "Design Agencies", "Startups"],
    dayInLife: "User research, wireframing, prototyping, design reviews, stakeholder collaboration",
    experienceLevel: "mid",
    minYearsExperience: 2,
    maxYearsExperience: 8,
    salaryMin: 70000,
    salaryMax: 105000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["UX Design", "Figma", "Adobe Certified", "Google UX"],
    requiredCertifications: [],
    workLifeBalanceRating: 4,
    agePreference: "24-38",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["ux designer", "user experience", "figma", "user research", "prototyping"],
    relatedJobTitles: ["UI Designer", "Product Designer", "Visual Designer"],
    valuedCompanies: ["Google", "Microsoft", "Design Agencies", "Tech Companies"],
    preferredIndustryExperience: ["Design", "Creative", "Technology"],
    careerProgressionPatterns: ["Junior Designer → UX Designer → Senior Designer → Design Lead"],
    alternativeQualifications: ["2+ years design experience", "Strong portfolio", "Design tool proficiency"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 2,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 2
  },

  // ========================================
  // JUNIOR LEVEL (1-4 years) - Early Career Professional Roles
  // ========================================
  {
    title: "Junior Data Analyst",
    salaryRange: "$50,000 - $70,000",
    description: "Support data analysis projects, create reports and visualizations, learn advanced analytics techniques",
    requiredTechnicalSkills: ["Excel/Spreadsheets", "SQL", "Data Visualization", "Basic Statistics"],
    requiredSoftSkills: ["Problem Solving", "Attention to Detail", "Communication", "Learning Agility"],
    preferredInterests: ["Data & Analytics", "Technology & Software", "Research"],
    preferredIndustries: ["Technology & Software", "Financial Services", "Healthcare & Medical"],
    workDataWeight: 5,
    workPeopleWeight: 2,
    creativityWeight: 2,
    problemSolvingWeight: 4,
    leadershipWeight: 2,
    learningPath: "Data Analytics Fundamentals (3-4 months)",
    stretchLevel: "safe",
    careerType: "junior-data-analyst",
    requiresTechnical: true,
    companies: ["Tech Startups", "Mid-size Companies", "Consulting Firms", "Healthcare Organizations"],
    dayInLife: "Data extraction, report creation, basic analysis, learning new tools",
    experienceLevel: "junior",
    minYearsExperience: 1,
    maxYearsExperience: 4,
    salaryMin: 50000,
    salaryMax: 70000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["Google Analytics", "Excel", "SQL", "Tableau"],
    requiredCertifications: [],
    workLifeBalanceRating: 4,
    agePreference: "22-30",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["junior data analyst", "data analysis", "excel", "sql", "reporting"],
    relatedJobTitles: ["Data Analyst", "Reporting Analyst", "Business Intelligence Analyst"],
    valuedCompanies: ["Growing Companies", "Tech Startups", "Consulting Firms"],
    preferredIndustryExperience: ["Any analytical work", "Internships", "Academic projects"],
    careerProgressionPatterns: ["Junior Analyst → Data Analyst → Senior Analyst → Manager"],
    alternativeQualifications: ["1+ years analytical experience", "Strong Excel skills", "SQL knowledge"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 2
  },

  {
    title: "Junior Software Engineer",
    salaryRange: "$65,000 - $85,000",
    description: "Develop software applications under guidance, learn best practices, contribute to team projects",
    requiredTechnicalSkills: ["Programming Languages", "Version Control", "Basic Software Development", "Testing"],
    requiredSoftSkills: ["Problem Solving", "Learning Agility", "Communication", "Collaboration"],
    preferredInterests: ["Technology & Software", "Engineering", "Problem Solving"],
    preferredIndustries: ["Technology & Software", "Financial Services", "E-commerce"],
    workDataWeight: 3,
    workPeopleWeight: 3,
    creativityWeight: 4,
    problemSolvingWeight: 5,
    leadershipWeight: 2,
    learningPath: "Software Engineering Fundamentals (3-6 months)",
    stretchLevel: "safe",
    careerType: "junior-software-engineer",
    requiresTechnical: true,
    companies: ["Tech Startups", "Mid-size Tech Companies", "Consulting Firms"],
    dayInLife: "Code development, bug fixes, learning new technologies, code reviews",
    experienceLevel: "junior",
    minYearsExperience: 1,
    maxYearsExperience: 4,
    salaryMin: 65000,
    salaryMax: 85000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["Programming Languages", "AWS", "Cloud Platforms"],
    requiredCertifications: [],
    workLifeBalanceRating: 4,
    agePreference: "22-28",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["junior software engineer", "programming", "development", "coding"],
    relatedJobTitles: ["Software Engineer", "Developer", "Full Stack Developer"],
    valuedCompanies: ["Tech Companies", "Startups", "Growing Companies"],
    preferredIndustryExperience: ["Software development", "Programming", "Technology"],
    careerProgressionPatterns: ["Junior Engineer → Software Engineer → Senior Engineer"],
    alternativeQualifications: ["1+ years programming", "CS degree or bootcamp", "Technical projects"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 2,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 3
  },

  {
    title: "Junior UX Designer",
    salaryRange: "$50,000 - $70,000",
    description: "Create wireframes and prototypes, support design projects, learn user research methods",
    requiredTechnicalSkills: ["Figma", "Adobe Creative Suite", "Wireframing", "Prototyping"],
    requiredSoftSkills: ["Creativity", "Communication", "Problem Solving", "Attention to Detail"],
    preferredInterests: ["Creative Arts & Design", "Technology & Software", "User Experience"],
    preferredIndustries: ["Technology & Software", "Design Agencies", "E-commerce"],
    workDataWeight: 2,
    workPeopleWeight: 4,
    creativityWeight: 5,
    problemSolvingWeight: 4,
    leadershipWeight: 2,
    learningPath: "UX Design Fundamentals (3-4 months)",
    stretchLevel: "safe",
    careerType: "junior-ux-designer",
    requiresTechnical: true,
    companies: ["Design Agencies", "Tech Startups", "E-commerce Companies"],
    dayInLife: "Wireframe creation, design system work, user research support, design iteration",
    experienceLevel: "junior",
    minYearsExperience: 1,
    maxYearsExperience: 4,
    salaryMin: 50000,
    salaryMax: 70000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["UX Design", "Figma", "Adobe Certified", "Google UX"],
    requiredCertifications: [],
    workLifeBalanceRating: 4,
    agePreference: "22-30",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["junior ux designer", "ux design", "figma", "wireframes", "prototypes"],
    relatedJobTitles: ["UX Designer", "UI Designer", "Product Designer"],
    valuedCompanies: ["Design Agencies", "Tech Companies", "Startups"],
    preferredIndustryExperience: ["Design", "Creative", "Technology"],
    careerProgressionPatterns: ["Junior Designer → UX Designer → Senior Designer"],
    alternativeQualifications: ["1+ years design experience", "Strong portfolio", "Design tool proficiency"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 2,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 2
  },

  // ========================================
  // ENTRY LEVEL (0-2 years) - New Graduate Roles
  // ========================================
  {
    title: "Associate Product Manager",
    salaryRange: "$70,000 - $95,000",
    description: "Support product management activities, learn product strategy, assist with roadmap planning and user research",
    requiredTechnicalSkills: ["Product Management Basics", "Data Analysis", "User Research", "Agile/Scrum"],
    requiredSoftSkills: ["Communication", "Problem Solving", "Learning Agility", "Collaboration"],
    preferredInterests: ["Technology & Software", "Business & Entrepreneurship", "Innovation"],
    preferredIndustries: ["Technology & Software", "Financial Services", "E-commerce"],
    workDataWeight: 4,
    workPeopleWeight: 4,
    creativityWeight: 3,
    problemSolvingWeight: 4,
    leadershipWeight: 3,
    learningPath: "Associate Product Manager Program (6 months)",
    stretchLevel: "safe",
    careerType: "associate-product-manager",
    requiresTechnical: true,
    companies: ["Google", "Microsoft", "Amazon", "Meta", "Tech Startups"],
    dayInLife: "Product research, data analysis, stakeholder support, learning product strategy",
    experienceLevel: "entry",
    minYearsExperience: 0,
    maxYearsExperience: 2,
    salaryMin: 70000,
    salaryMax: 95000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["Product Management", "Google Analytics", "Agile/Scrum"],
    requiredCertifications: [],
    workLifeBalanceRating: 4,
    agePreference: "22-28",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["associate product manager", "product management", "analytics", "user research"],
    relatedJobTitles: ["Product Analyst", "Business Analyst", "Program Manager"],
    valuedCompanies: ["Google", "Microsoft", "Amazon", "Tech Companies"],
    preferredIndustryExperience: ["Technology", "Business analysis", "Consulting"],
    careerProgressionPatterns: ["APM → Product Manager → Senior PM"],
    alternativeQualifications: ["Recent graduate", "Analytical skills", "Technology interest"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 1
  },

  {
    title: "Data Analyst",
    salaryRange: "$55,000 - $75,000",
    description: "Analyze data to support business decisions, create reports and dashboards, learn advanced analytics",
    requiredTechnicalSkills: ["Excel/Spreadsheets", "SQL", "Data Visualization", "Basic Statistics"],
    requiredSoftSkills: ["Problem Solving", "Communication", "Attention to Detail", "Critical Thinking"],
    preferredInterests: ["Data & Analytics", "Technology & Software", "Research"],
    preferredIndustries: ["Technology & Software", "Financial Services", "Healthcare & Medical"],
    workDataWeight: 5,
    workPeopleWeight: 3,
    creativityWeight: 2,
    problemSolvingWeight: 4,
    leadershipWeight: 2,
    learningPath: "Data Analytics Certification (2-4 months)",
    stretchLevel: "safe",
    careerType: "data-analyst",
    requiresTechnical: true,
    companies: ["Various Industries", "Tech Companies", "Consulting Firms", "Healthcare"],
    dayInLife: "Data analysis, report creation, dashboard building, stakeholder presentations",
    experienceLevel: "entry",
    minYearsExperience: 0,
    maxYearsExperience: 3,
    salaryMin: 55000,
    salaryMax: 75000,
    remoteOptions: "Remote available",
    workEnvironments: ["office", "hybrid", "remote"],
    requiredEducation: "bachelors",
    preferredEducation: "bachelors",
    valuedCertifications: ["Google Analytics", "Excel", "SQL", "Tableau"],
    requiredCertifications: [],
    workLifeBalanceRating: 4,
    agePreference: "22-30",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["data analyst", "data analysis", "excel", "sql", "reporting", "analytics"],
    relatedJobTitles: ["Business Analyst", "Reporting Analyst", "Data Scientist"],
    valuedCompanies: ["All Industries", "Tech Companies", "Consulting Firms"],
    preferredIndustryExperience: ["Any analytical work", "Research", "Academic projects"],
    careerProgressionPatterns: ["Data Analyst → Senior Analyst → Data Scientist → Manager"],
    alternativeQualifications: ["Recent graduate", "Strong analytical skills", "Excel/SQL knowledge"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    handsOnWorkWeight: 1,
    physicalWorkWeight: 1,
    outdoorWorkWeight: 1,
    mechanicalAptitudeWeight: 2
  }
];

// ========================================
// CRITICAL FIX: VALIDATE AND SANITIZE TRADES TEMPLATES
// ========================================

const sanitizeCareerTemplate = (career: any): CareerTemplate => {
  return {
    ...career,
    // CRITICAL: Ensure all required arrays exist and are arrays
    requiredTechnicalSkills: Array.isArray(career.requiredTechnicalSkills) ? career.requiredTechnicalSkills : [],
    requiredSoftSkills: Array.isArray(career.requiredSoftSkills) ? career.requiredSoftSkills : [],
    preferredInterests: Array.isArray(career.preferredInterests) ? career.preferredInterests : [],
    preferredIndustries: Array.isArray(career.preferredIndustries) ? career.preferredIndustries : [],
    companies: Array.isArray(career.companies) ? career.companies : [],
    workEnvironments: Array.isArray(career.workEnvironments) ? career.workEnvironments : ["office"],
    valuedCertifications: Array.isArray(career.valuedCertifications) ? career.valuedCertifications : [],
    requiredCertifications: Array.isArray(career.requiredCertifications) ? career.requiredCertifications : [],
    resumeKeywords: Array.isArray(career.resumeKeywords) ? career.resumeKeywords : [],
    relatedJobTitles: Array.isArray(career.relatedJobTitles) ? career.relatedJobTitles : [],
    valuedCompanies: Array.isArray(career.valuedCompanies) ? career.valuedCompanies : [],
    preferredIndustryExperience: Array.isArray(career.preferredIndustryExperience) ? career.preferredIndustryExperience : [],
    careerProgressionPatterns: Array.isArray(career.careerProgressionPatterns) ? career.careerProgressionPatterns : [],
    alternativeQualifications: Array.isArray(career.alternativeQualifications) ? career.alternativeQualifications : [],
    
    // Ensure numeric fields have defaults
    workDataWeight: typeof career.workDataWeight === 'number' ? career.workDataWeight : 3,
    workPeopleWeight: typeof career.workPeopleWeight === 'number' ? career.workPeopleWeight : 3,
    creativityWeight: typeof career.creativityWeight === 'number' ? career.creativityWeight : 3,
    problemSolvingWeight: typeof career.problemSolvingWeight === 'number' ? career.problemSolvingWeight : 3,
    leadershipWeight: typeof career.leadershipWeight === 'number' ? career.leadershipWeight : 3,
    handsOnWorkWeight: typeof career.handsOnWorkWeight === 'number' ? career.handsOnWorkWeight : 3,
    physicalWorkWeight: typeof career.physicalWorkWeight === 'number' ? career.physicalWorkWeight : 3,
    outdoorWorkWeight: typeof career.outdoorWorkWeight === 'number' ? career.outdoorWorkWeight : 3,
    mechanicalAptitudeWeight: typeof career.mechanicalAptitudeWeight === 'number' ? career.mechanicalAptitudeWeight : 3,
    workLifeBalanceRating: typeof career.workLifeBalanceRating === 'number' ? career.workLifeBalanceRating : 3,
    minYearsExperience: typeof career.minYearsExperience === 'number' ? career.minYearsExperience : 0,
    maxYearsExperience: typeof career.maxYearsExperience === 'number' ? career.maxYearsExperience : 10,
    salaryMin: typeof career.salaryMin === 'number' ? career.salaryMin : 50000,
    salaryMax: typeof career.salaryMax === 'number' ? career.salaryMax : 100000,
    
    // Ensure string fields have defaults
    title: career.title || 'Unknown Career',
    salaryRange: career.salaryRange || '$50,000 - $100,000',
    description: career.description || 'Career description not available',
    learningPath: career.learningPath || 'Professional development program',
    stretchLevel: career.stretchLevel || 'safe',
    careerType: career.careerType || 'unknown-career',
    dayInLife: career.dayInLife || 'Professional work activities',
    experienceLevel: career.experienceLevel || 'mid',
    remoteOptions: career.remoteOptions || 'Available',
    requiredEducation: career.requiredEducation || 'high-school',
    preferredEducation: career.preferredEducation || 'bachelors',
    agePreference: career.agePreference || '25-45',
    locationFlexibility: career.locationFlexibility || 'flexible',
    
    // Ensure boolean fields have defaults
    requiresTechnical: typeof career.requiresTechnical === 'boolean' ? career.requiresTechnical : true,
    transitionFriendly: typeof career.transitionFriendly === 'boolean' ? career.transitionFriendly : true,
    skillBasedEntry: typeof career.skillBasedEntry === 'boolean' ? career.skillBasedEntry : true,
    experienceCanSubstitute: typeof career.experienceCanSubstitute === 'boolean' ? career.experienceCanSubstitute : true
  };
};

// CRITICAL FIX: Sanitize trades templates before combining
const SANITIZED_TRADES_TEMPLATES = TRADES_CAREER_TEMPLATES.map(sanitizeCareerTemplate);

// Combined career templates with sanitized data
// Combine all templates and remove duplicates
const combinedTemplates = [
  ...COMPREHENSIVE_CAREER_TEMPLATES,
  ...SANITIZED_TRADES_TEMPLATES,
  ...placeholderTemplates,
];

const uniqueCareerTemplates = Array.from(
  combinedTemplates
    .reduce((map, career) => {
      if (!map.has(career.careerType)) {
        map.set(career.careerType, career);
      }
      return map;
    }, new Map<string, CareerTemplate>())
    .values()
);

export const CAREER_TEMPLATES: CareerTemplate[] = uniqueCareerTemplates;

console.log(`🔧 FIXED: Career templates loaded and sanitized: ${CAREER_TEMPLATES.length} total careers`);

// ========================================
// HELPER FUNCTIONS
// ========================================

export const getExperienceLevel = (exp: string): string => {
  if (exp === '0') return 'entry';
  if (exp === '1-2') return 'junior';
  if (exp === '3-5') return 'mid';
  if (exp === '6-10') return 'senior';
  if (exp === '10-20') return 'senior';
  if (exp === '20+') return 'executive';
  return 'entry';
};

export const getExperienceYears = (experience: string): number => {
  switch (experience) {
    case '0': return 0;
    case '1-2': return 1.5;
    case '3-5': return 4;
    case '6-10': return 8;
    case '10-20': return 15;
    case '20+': return 25;
    default: return 0;
  }
};

// ========================================
// NEW: ADVENTURE ZONE FILTERING HELPERS WITH SAFETY GUARDRAILS
// ========================================

/**
 * Check if a career requires specialized licensing or training that makes it inappropriate
 * for cross-industry recommendations without proper qualifications
 */
const isSafetyCriticalCareer = (career: CareerTemplate): boolean => {
  // CRITICAL SAFETY UPDATE: Only block truly life-threatening careers requiring specialized medical/emergency training
  // This matches the backend logic exactly to prevent inconsistencies
  
  const titleLower = career.title.toLowerCase();
  const descriptionLower = career.description.toLowerCase();
  
  // LIFE-CRITICAL MEDICAL ROLES - Direct patient care with life/death decisions
  const medicalLifeCritical = [
    'physician', 'doctor', 'surgeon', 'anesthesiologist', 'anesthetist', 'crna',
    'nurse anesthetist', 'emergency physician', 'trauma surgeon', 'cardiologist',
    'oncologist', 'neurologist', 'psychiatrist', 'pharmacist', 'dentist'
  ];
  
  // EMERGENCY RESPONSE ROLES - Life/death emergency situations
  const emergencyLifeCritical = [
    'paramedic', 'emt', 'emergency medical technician', 'firefighter',
    'police officer', 'sheriff', 'detective', '911 dispatcher', 'emergency dispatcher'
  ];
  
  // AVIATION SAFETY ROLES - Passenger safety responsibility
  const aviationLifeCritical = [
    'airline pilot', 'commercial pilot', 'air traffic controller', 'flight engineer'
  ];
  
  // NUCLEAR/HAZARDOUS MATERIALS - Public safety with catastrophic risk
  const hazmatLifeCritical = [
    'nuclear engineer', 'nuclear technician', 'radiation safety', 'hazmat specialist'
  ];
  
  const allLifeCritical = [
    ...medicalLifeCritical,
    ...emergencyLifeCritical,
    ...aviationLifeCritical,
    ...hazmatLifeCritical
  ];
  
  // Check for exact matches or very specific containment
  const isLifeCritical = allLifeCritical.some(keyword => {
    // More precise matching to avoid false positives
    if (keyword.includes(' ')) {
      // Multi-word terms need exact phrase matching
      return titleLower.includes(keyword) || descriptionLower.includes(keyword);
    } else {
      // Single words need word boundary checking to avoid partial matches
      const wordBoundaryRegex = new RegExp(`\\b${keyword}\\b`, 'i');
      return wordBoundaryRegex.test(career.title) || wordBoundaryRegex.test(career.description);
    }
  });
  
  if (isLifeCritical) {
    console.log(`🚨 FRONTEND SAFETY: Identified life-critical career: ${career.title}`);
    return true;
  }
  
  return false;
};

/**
 * Check if user has relevant background for safety-critical careers
 */
const hasRelevantBackground = (userAssessment: UserAssessmentData, career: CareerTemplate): boolean => {
  if (!isSafetyCriticalCareer(career)) return true; // Not safety-critical, allow
  
  const userSkills = [...(userAssessment.technicalSkills || []), ...(userAssessment.softSkills || [])];
  const userIndustries = userAssessment.industries || [];
  const userResume = (userAssessment.resumeText || '').toLowerCase();
  const userRole = (userAssessment.currentRole || '').toLowerCase();
  
  // Check for relevant medical background
  if (career.title.toLowerCase().includes('nurse') || career.title.toLowerCase().includes('medical')) {
    const medicalKeywords = ['nurse', 'medical', 'healthcare', 'hospital', 'clinical', 'patient care'];
    const hasmedicalBackground =
      userIndustries.some(ind => ind.toLowerCase().includes('healthcare')) ||
      userSkills.some(skill => medicalKeywords.some(keyword => skill.toLowerCase().includes(keyword))) ||
      medicalKeywords.some(keyword => userResume.includes(keyword) || userRole.includes(keyword));
    
    if (!hasmedicalBackground) return false;
  }
  
  // Check for relevant legal background
  if (career.title.toLowerCase().includes('attorney') || career.title.toLowerCase().includes('lawyer')) {
    const legalKeywords = ['legal', 'law', 'attorney', 'lawyer', 'paralegal', 'compliance'];
    const hasLegalBackground =
      userIndustries.some(ind => ind.toLowerCase().includes('legal')) ||
      userSkills.some(skill => legalKeywords.some(keyword => skill.toLowerCase().includes(keyword))) ||
      legalKeywords.some(keyword => userResume.includes(keyword) || userRole.includes(keyword));
    
    if (!hasLegalBackground) return false;
  }
  
  // Check for relevant engineering background
  if (career.title.toLowerCase().includes('engineer')) {
    const engineeringKeywords = ['engineer', 'engineering', 'technical', 'systems', 'architecture'];
    const hasEngineeringBackground =
      userIndustries.some(ind => ind.toLowerCase().includes('engineering')) ||
      userSkills.some(skill => engineeringKeywords.some(keyword => skill.toLowerCase().includes(keyword))) ||
      engineeringKeywords.some(keyword => userResume.includes(keyword) || userRole.includes(keyword));
    
    if (!hasEngineeringBackground) return false;
  }
  
  return true;
};

/**
 * Check if industries are compatible for Adventure Zone
 * Allows for related industries and cross-industry transitions
 */
const isIndustryCompatible = (userIndustries: string[], careerIndustries: string[]): boolean => {
  if (!Array.isArray(userIndustries) || !Array.isArray(careerIndustries)) return true;
  if (userIndustries.length === 0 || careerIndustries.length === 0) return true;
  
  // Direct industry matches
  const directMatches = careerIndustries.some(careerInd => 
    userIndustries.some(userInd => 
      userInd.toLowerCase().includes(careerInd.toLowerCase()) ||
      careerInd.toLowerCase().includes(userInd.toLowerCase())
    )
  );
  
  if (directMatches) return true;
  
  // Related industry mapping for Adventure Zone
  const industryRelations: Record<string, string[]> = {
    'Technology & Software': ['Financial Services', 'E-commerce', 'Healthcare & Medical', 'Media & Entertainment'],
    'Financial Services': ['Technology & Software', 'Consulting & Professional Services', 'Real Estate'],
    'Healthcare & Medical': ['Technology & Software', 'Consulting & Professional Services', 'Education'],
    'Consulting & Professional Services': ['Financial Services', 'Technology & Software', 'Healthcare & Medical'],
    'Manufacturing & Industrial': ['Construction & Trades', 'Energy & Utilities', 'Transportation & Logistics'],
    'Construction & Trades': ['Manufacturing & Industrial', 'Real Estate', 'Energy & Utilities'],
    'Education': ['Healthcare & Medical', 'Government & Public Service', 'Non-Profit & Social Services'],
    'Media & Entertainment': ['Technology & Software', 'Arts & Culture', 'Sports & Recreation'],
    'E-commerce': ['Technology & Software', 'Retail & E-commerce', 'Transportation & Logistics']
  };
  
  // Check for related industries
  const relatedMatches = userIndustries.some(userInd => {
    const relatedIndustries = industryRelations[userInd] || [];
    return careerIndustries.some(careerInd => 
      relatedIndustries.some(related => 
        related.toLowerCase().includes(careerInd.toLowerCase()) ||
        careerInd.toLowerCase().includes(related.toLowerCase())
      )
    );
  });
  
  return relatedMatches;
};

/**
 * Check if career is appropriate for user's seniority level
 * Prevents showing entry-level service jobs to senior professionals
 */
const isSeniorityAppropriate = (userExperienceYears: number, userExperienceLevel: string, career: CareerTemplate): boolean => {
  // Define inappropriate combinations
  const inappropriateCombinations = [
    // Senior professionals (10+ years) shouldn't see basic service roles
    {
      userCondition: (years: number, level: string) => years >= 10 || level === 'senior' || level === 'executive',
      careerCondition: (career: CareerTemplate) => 
        (career.experienceLevel === 'entry' || career.experienceLevel === 'junior') &&
        (career.title.toLowerCase().includes('customer service') ||
         career.title.toLowerCase().includes('retail sales') ||
         career.title.toLowerCase().includes('medical assistant') ||
         career.title.toLowerCase().includes('cashier') ||
         career.title.toLowerCase().includes('receptionist') ||
         career.salaryMax < 45000) &&
        !career.transitionFriendly
    },
    
    // Executive level (15+ years) shouldn't see mid-level roles unless transition-friendly
    {
      userCondition: (years: number, level: string) => years >= 15 || level === 'executive',
      careerCondition: (career: CareerTemplate) => 
        (career.experienceLevel === 'entry' || career.experienceLevel === 'junior') &&
        career.salaryMax < 60000 &&
        !career.transitionFriendly
    },
    
    // People with college degrees shouldn't see high school level service jobs
    {
      userCondition: (years: number, level: string, userData?: UserAssessmentData) => 
        userData?.educationLevel === 'bachelors' || userData?.educationLevel === 'masters' || userData?.educationLevel === 'doctorate',
      careerCondition: (career: CareerTemplate) => 
        career.requiredEducation === 'high-school' &&
        career.salaryMax < 40000 &&
        (career.title.toLowerCase().includes('customer service') ||
         career.title.toLowerCase().includes('retail') ||
         career.title.toLowerCase().includes('food service'))
    }
  ];
  
  // Check each inappropriate combination
  for (const combo of inappropriateCombinations) {
    if (combo.userCondition(userExperienceYears, userExperienceLevel) && combo.careerCondition(career)) {
      return false;
    }
  }
  
  return true;
};

/**
 * Check if experience levels are reasonably compatible for Adventure Zone
 * More generous than Safe/Stretch zones but still has boundaries
 */
const isExperienceReasonable = (userExperienceYears: number, userExperienceLevel: string, career: CareerTemplate): boolean => {
  // Adventure Zone: Very generous experience boundaries
  const experienceGap = Math.min(
    Math.abs(userExperienceYears - career.minYearsExperience),
    Math.abs(userExperienceYears - career.maxYearsExperience)
  );
  
  // Allow much larger experience gaps in Adventure Zone
  if (experienceGap <= 20) return true;
  
  // Special cases for transition-friendly careers
  if (career.transitionFriendly || career.skillBasedEntry) return true;
  
  // Allow stretch opportunities within reason
  if (userExperienceLevel === 'senior' && career.experienceLevel === 'executive') return true;
  if (userExperienceLevel === 'mid' && (career.experienceLevel === 'senior' || career.experienceLevel === 'junior')) return true;
  
  return false;
};

// ========================================
// FIXED ADVENTURE ZONE FILTERING - ENSURES APPROPRIATE RECOMMENDATIONS
// ========================================

export const generateCareerRecommendations = (
  assessmentData: UserAssessmentData,
  explorationLevel: number = 1
): CareerMatch[] => {
  console.log('🚀 FIXED: Starting career recommendation generation...');
  console.log('🎯 Exploration Level:', explorationLevel);
  
  const normalizedData = normalizeAssessmentData(assessmentData);
  const userExperienceYears = getExperienceYears(normalizedData.experience);
  const userExperienceLevel = getExperienceLevel(normalizedData.experience);
  
  console.log('👤 User Profile:', { 
    experienceYears: userExperienceYears, 
    experienceLevel: userExperienceLevel, 
    explorationLevel,
    totalCareers: CAREER_TEMPLATES.length 
  });
  
  // ========================================
  // FIXED ADVENTURE ZONE FILTERING - PROPER BOUNDARIES
  // ========================================
  
  let candidateCareers = CAREER_TEMPLATES;
  
  if (explorationLevel === 1) {
    // Safe Zone: Experience level match + adjacent levels
    const safeExperienceLevels = [userExperienceLevel];
    const levelOrder = ['entry', 'junior', 'mid', 'senior', 'executive'];
    const currentIndex = levelOrder.indexOf(userExperienceLevel);
    
    if (currentIndex > 0) safeExperienceLevels.push(levelOrder[currentIndex - 1]);
    if (currentIndex < levelOrder.length - 1) safeExperienceLevels.push(levelOrder[currentIndex + 1]);
    
    candidateCareers = CAREER_TEMPLATES.filter(career => 
      safeExperienceLevels.includes(career.experienceLevel) ||
      (userExperienceYears >= career.minYearsExperience - 2 && 
       userExperienceYears <= career.maxYearsExperience + 3)
    );
    
    console.log(`🔍 Safe Zone: ${candidateCareers.length} careers after filtering`);
  } else if (explorationLevel === 2) {
    // Stretch Zone: Broader experience range
    candidateCareers = CAREER_TEMPLATES.filter(career => 
      userExperienceYears >= career.minYearsExperience - 5 && 
      userExperienceYears <= career.maxYearsExperience + 8
    );
    
    console.log(`🔍 Stretch Zone: ${candidateCareers.length} careers after filtering`);
  } else {
    // FIXED ADVENTURE ZONE: SMART FILTERING WITH SAFETY GUARDRAILS
    console.log('🎯 Adventure Zone: SMART DISCOVERY MODE - Filtering for appropriate opportunities...');
    
    candidateCareers = CAREER_TEMPLATES.filter(career => {
      // NEW: Safety-critical career check - HIGHEST PRIORITY
      if (isSafetyCriticalCareer(career) && !hasRelevantBackground(normalizedData, career)) {
        console.log(`🚨 SAFETY FILTER: Blocked ${career.title} - requires specialized training/licensing without relevant background`);
        return false;
      }
      
      // NEW: Enhanced filtering - Filter out inappropriate careers for users without relevant background
      const hasMinimalProfile = (
        (!normalizedData.resumeText || normalizedData.resumeText.length < 50) &&
        (!normalizedData.technicalSkills || normalizedData.technicalSkills.length === 0)
      );
      
      // Check if user has trades-relevant skills
      const userTechnicalSkills = normalizedData.technicalSkills || [];
      const tradesRelevantSkills = [
        "electrical", "plumbing", "hvac", "welding", "carpentry", "mechanical", "automotive",
        "construction", "maintenance", "machining", "fabrication", "installation", "repair"
      ];
      const hasTradesSkills = userTechnicalSkills.some(skill =>
        tradesRelevantSkills.some(tradesSkill => skill.toLowerCase().includes(tradesSkill))
      );
      
      // Check if user has medical-relevant skills
      const medicalRelevantSkills = [
        "medical", "clinical", "healthcare", "patient", "nursing", "laboratory", "radiology",
        "pharmacy", "medical equipment", "medical device", "healthcare technology"
      ];
      const hasMedicalSkills = userTechnicalSkills.some(skill =>
        medicalRelevantSkills.some(medicalSkill => skill.toLowerCase().includes(medicalSkill))
      );
      
      // Apply filtering for users without relevant background
      const shouldFilterTradesMedical = hasMinimalProfile || (!hasTradesSkills && !hasMedicalSkills);
      
      if (shouldFilterTradesMedical) {
        const inappropriateCareers = [
          "medical equipment technician", "clinical research coordinator", "plumber",
          "electrician", "hvac technician", "welder", "carpenter", "mechanic",
          "radiologic technologist", "medical laboratory technologist", "pharmacy technician",
          "diesel mechanic", "auto body technician", "sheet metal worker", "boilermaker",
          "pipefitter", "mason", "roofer", "concrete finisher", "drywall installer",
          "flooring installer", "heavy equipment operator", "automotive technician",
          "motorcycle technician", "machinist", "cnc operator", "industrial maintenance technician",
          "millwright", "glazier", "insulation worker", "power line technician", "locksmith",
          "refrigeration technician", "industrial electrician"
        ];
        
        const careerTitleLower = career.title.toLowerCase();
        if (inappropriateCareers.some(inappropriate => careerTitleLower.includes(inappropriate))) {
          if (hasMinimalProfile) {
            console.log(`❌ MINIMAL PROFILE FILTER: Blocked ${career.title} - inappropriate for minimal profile user`);
          } else {
            console.log(`❌ SKILLS FILTER: Blocked ${career.title} - user lacks relevant trades/medical background`);
          }
          return false;
        }
      }
      
      // FIXED: Apply industry compatibility check
      if (!isIndustryCompatible(normalizedData.industries, career.preferredIndustries)) {
        console.log(`❌ Industry incompatible: ${career.title} (${career.preferredIndustries.join(', ')}) vs user (${normalizedData.industries.join(', ')})`);
        return false;
      }
      
      // FIXED: Apply seniority appropriateness check
      if (!isSeniorityAppropriate(userExperienceYears, userExperienceLevel, career)) {
        console.log(`❌ Seniority inappropriate: ${career.title} for ${userExperienceLevel} (${userExperienceYears} years)`);
        return false;
      }
      
      // FIXED: Apply reasonable experience boundaries
      if (!isExperienceReasonable(userExperienceYears, userExperienceLevel, career)) {
        console.log(`❌ Experience unreasonable: ${career.title} (${career.minYearsExperience}-${career.maxYearsExperience} years) for user (${userExperienceYears} years)`);
        return false;
      }
      
      console.log(`✅ Adventure Zone approved: ${career.title}`);
      return true;
    });
    
    console.log(`🔍 Adventure Zone: ${candidateCareers.length} appropriate opportunities after SMART filtering`);
  }
  
  // CRITICAL FIX: Ensure we always have candidates
  if (candidateCareers.length === 0) {
    console.warn('⚠️ ZERO candidates after filtering - using fallback with looser constraints');
    
    // Fallback: Use industry-compatible careers only
    candidateCareers = CAREER_TEMPLATES.filter(career => 
      isIndustryCompatible(normalizedData.industries, career.preferredIndustries)
    );
    
    console.log(`🔄 Fallback: Using ${candidateCareers.length} industry-compatible careers`);
    
    // If still zero, use all careers as last resort
    if (candidateCareers.length === 0) {
      candidateCareers = CAREER_TEMPLATES;
      console.log(`🚨 Last resort: Using all ${candidateCareers.length} careers`);
    }
  }
  
  console.log(`📊 Processing ${candidateCareers.length} candidate careers...`);
  
  // CRITICAL FIX: Add error handling for career matching
  const careerMatches: CareerMatch[] = [];
  
  candidateCareers.forEach((career, index) => {
    try {
      const match = calculateCareerMatch(career, normalizedData, explorationLevel);
      careerMatches.push(match);
    } catch (error) {
      console.error(`❌ Error processing career ${index} (${career.title}):`, error);
      console.error('Career data:', career);
      // Skip this career and continue with others
    }
  });

  // Sort and return results
  const sortedMatches = careerMatches.sort((a, b) => b.relevanceScore - a.relevanceScore);
  
  // FIXED: Adventure Zone gets MORE results with LOWER minimum scores
  let targetResults;
  if (explorationLevel === 1) {
    targetResults = Math.min(5, sortedMatches.length);
  } else if (explorationLevel === 2) {
    targetResults = Math.min(8, sortedMatches.length);
  } else {
    // Adventure Zone: Show MORE opportunities
    targetResults = Math.min(12, sortedMatches.length);
  }
  
  const finalResults = sortedMatches.slice(0, Math.max(targetResults, 5));
  
  console.log(`🎯 FINAL RESULTS: ${finalResults.length} recommendations for exploration level ${explorationLevel}`);
  console.log('🏆 Top 3 matches:', finalResults.slice(0, 3).map(r => `${r.title} (${r.relevanceScore}%)`));
  
  // CRITICAL: Ensure we ALWAYS return results
  if (finalResults.length === 0) {
    console.error('🚨 CRITICAL: Still zero results - returning top 5 from all careers');
    const emergencyResults = CAREER_TEMPLATES
      .slice(0, 10) // Take first 10 to avoid processing errors
      .map(career => {
        try {
          return calculateCareerMatch(career, normalizedData, explorationLevel);
        } catch (error) {
          console.error('Emergency fallback error:', error);
          return null;
        }
      })
      .filter(Boolean) // Remove null results
      .sort((a, b) => b!.relevanceScore - a!.relevanceScore)
      .slice(0, 5) as CareerMatch[];
    return emergencyResults;
  }
  
  return finalResults;
};

// ========================================
// DATA NORMALIZATION
// ========================================

const normalizeAssessmentData = (assessmentData: UserAssessmentData): UserAssessmentData => {
  if (!assessmentData) {
    return getDefaultAssessmentData();
  }
  
  const normalized = { ...assessmentData };
  
  // Fix work preferences - convert arrays to numbers
  const workPrefs = ['workingWithData', 'workingWithPeople', 'creativeTasks', 'problemSolving', 'leadership'];
  workPrefs.forEach(field => {
    let value = normalized[field];
    if (Array.isArray(value)) value = value[0];
    if (typeof value !== 'number' || value < 1 || value > 5) value = 3;
    normalized[field] = value;
  });
  
  // Handle trades-specific preferences
  if (normalized.physicalHandsOnWork !== undefined) {
    let value = Array.isArray(normalized.physicalHandsOnWork) ? normalized.physicalHandsOnWork[0] : normalized.physicalHandsOnWork;
    if (typeof value !== 'number' || value < 1 || value > 5) value = 3;
    normalized.physicalHandsOnWork = value;
    normalized.handsOnWork = value;
    normalized.physicalWork = value;
  }
  
  if (normalized.outdoorWork !== undefined) {
    let value = Array.isArray(normalized.outdoorWork) ? normalized.outdoorWork[0] : normalized.outdoorWork;
    if (typeof value !== 'number' || value < 1 || value > 5) value = 3;
    normalized.outdoorWork = value;
  }
  
  if (normalized.mechanicalAptitude !== undefined) {
    let value = Array.isArray(normalized.mechanicalAptitude) ? normalized.mechanicalAptitude[0] : normalized.mechanicalAptitude;
    if (typeof value !== 'number' || value < 1 || value > 5) value = 3;
    normalized.mechanicalAptitude = value;
  }
  
  // Ensure arrays exist
  if (!Array.isArray(normalized.interests) || normalized.interests.length === 0) {
    normalized.interests = ['Technology & Software', 'Business & Entrepreneurship'];
  }
  if (!Array.isArray(normalized.industries) || normalized.industries.length === 0) {
    normalized.industries = ['Technology & Software', 'Financial Services'];
  }
  if (!Array.isArray(normalized.technicalSkills)) normalized.technicalSkills = [];
  if (!Array.isArray(normalized.softSkills)) normalized.softSkills = [];
  if (!normalized.experience) normalized.experience = '3-5';
  
  return normalized;
};

const getDefaultAssessmentData = (): UserAssessmentData => {
  return {
    experience: '3-5',
    technicalSkills: ['Excel/Spreadsheets', 'Communication'],
    softSkills: ['Problem Solving', 'Teamwork'],
    workingWithData: 3,
    workingWithPeople: 3,
    creativeTasks: 3,
    problemSolving: 3,
    leadership: 3,
    interests: ['Technology & Software', 'Business & Entrepreneurship'],
    industries: ['Technology & Software', 'Financial Services'],
    workEnvironment: 'hybrid',
    salaryExpectations: '70k-100k',
    careerGoals: 'Professional growth and development',
    age: '26-30',
    location: 'United States',
    educationLevel: 'bachelors',
    certifications: [],
    currentSituation: 'employed',
    currentRole: 'Professional',
    resumeText: '',
    linkedinProfile: '',
    workLifeBalance: 'important'
  };
};

// ========================================
// FIXED CAREER MATCH CALCULATION WITH DEFENSIVE PROGRAMMING
// ========================================

export const calculateCareerMatch = (
  career: CareerTemplate, 
  assessmentData: UserAssessmentData,
  explorationLevel: number = 1
): CareerMatch => {
  let totalScore = 0;
  let maxPossibleScore = 0;
  const matchReasons: string[] = [];

  // CRITICAL FIX: Defensive programming for skill arrays
  const safeRequiredTechnicalSkills = Array.isArray(career.requiredTechnicalSkills) ? career.requiredTechnicalSkills : [];
  const safeRequiredSoftSkills = Array.isArray(career.requiredSoftSkills) ? career.requiredSoftSkills : [];
  const safeUserTechnicalSkills = Array.isArray(assessmentData.technicalSkills) ? assessmentData.technicalSkills : [];
  const safeUserSoftSkills = Array.isArray(assessmentData.softSkills) ? assessmentData.softSkills : [];

  // FIXED: Adventure Zone weights heavily favor work preferences and discovery
  const weights = explorationLevel === 3 ? {
    experience: 5,    // Much lower weight on experience
    skills: 10,       // Lower weight on existing skills
    workPrefs: 50,    // MUCH higher weight on work preferences
    industry: 15,     // Moderate weight on industry
    interests: 20     // Higher weight on interests for discovery
  } : explorationLevel === 2 ? {
    experience: 20,
    skills: 20,
    workPrefs: 35,
    industry: 12,
    interests: 13
  } : {
    experience: 25,
    skills: 25,
    workPrefs: 30,
    industry: 10,
    interests: 10
  };

  // FIXED: Much more generous experience matching for Adventure Zone
  const userExperienceLevel = getExperienceLevel(assessmentData.experience);
  const userYears = getExperienceYears(assessmentData.experience);
  
  let experienceScore = 0;
  
  if (explorationLevel === 3) {
    // Adventure Zone: VERY generous experience scoring
    if (userExperienceLevel === career.experienceLevel) {
      experienceScore = weights.experience;
      matchReasons.push("Experience level match");
    } else if (career.transitionFriendly || career.skillBasedEntry) {
      experienceScore = weights.experience * 0.95; // Almost full points
      matchReasons.push("Career transition opportunity");
    } else {
      // FIXED: Give substantial points for ANY experience level in Adventure Zone
      const experienceGap = Math.min(
        Math.abs(userYears - career.minYearsExperience),
        Math.abs(userYears - career.maxYearsExperience)
      );
      
      if (experienceGap <= 15) {
        experienceScore = weights.experience * 0.85; // Very generous
        matchReasons.push("Growth opportunity");
      } else {
        experienceScore = weights.experience * 0.7; // Still generous
        matchReasons.push("Long-term career possibility");
      }
    }
  } else {
    // Safe/Stretch Zones: Standard logic
    if (userExperienceLevel === career.experienceLevel) {
      experienceScore = weights.experience;
      matchReasons.push("Perfect experience level match");
    } else if (userYears >= career.minYearsExperience && userYears <= career.maxYearsExperience) {
      experienceScore = weights.experience * 0.9;
      matchReasons.push("Experience within role requirements");
    } else {
      const experienceGap = Math.min(
        Math.abs(userYears - career.minYearsExperience),
        Math.abs(userYears - career.maxYearsExperience)
      );
      
      if (experienceGap <= 5) {
        experienceScore = weights.experience * 0.8;
        matchReasons.push("Close experience match");
      } else if (experienceGap <= 10) {
        experienceScore = weights.experience * 0.6;
        matchReasons.push("Growth opportunity");
      } else {
        experienceScore = weights.experience * 0.4;
        if (explorationLevel >= 2) {
          matchReasons.push("Stretch opportunity");
        }
      }
    }
  }
  
  totalScore += experienceScore;
  maxPossibleScore += weights.experience;

  // FIXED: Much more generous skills matching for Adventure Zone with defensive programming
  const userSkills = [...safeUserTechnicalSkills, ...safeUserSoftSkills];
  const requiredSkills = [...safeRequiredTechnicalSkills, ...safeRequiredSoftSkills];
  
  const directMatches = requiredSkills.filter(skill => 
    userSkills.some(userSkill => 
      userSkill.toLowerCase().includes(skill.toLowerCase()) || 
      skill.toLowerCase().includes(userSkill.toLowerCase())
    )
  );
  
  let skillScore;
  if (requiredSkills.length === 0) {
    skillScore = weights.skills * 0.8;
  } else if (directMatches.length === 0) {
    // FIXED: Adventure Zone gives higher scores for no skill matches, BUT not for safety-critical careers
    if (explorationLevel === 3 && isSafetyCriticalCareer(career)) {
      // Safety-critical careers require relevant skills - much lower score for no matches
      skillScore = weights.skills * 0.2;
    } else {
      // Non-safety-critical careers can have generous scoring for skill gaps
      skillScore = explorationLevel === 3 ? weights.skills * 0.8 : weights.skills * 0.5;
    }
  } else {
    skillScore = (directMatches.length / requiredSkills.length) * weights.skills;
    skillScore = Math.min(skillScore, weights.skills);
  }
  
  totalScore += skillScore;
  maxPossibleScore += weights.skills;
  
  if (directMatches.length > 0) {
    matchReasons.push(`${directMatches.length}/${requiredSkills.length} skills match`);
  } else if (explorationLevel === 3) {
    matchReasons.push("New skills to develop - growth opportunity");
  } else if (explorationLevel >= 2) {
    matchReasons.push("Skills can be developed");
  }

  // Work preferences alignment - MOST IMPORTANT for Adventure Zone
  const dataAlignment = 5 - Math.abs(assessmentData.workingWithData - career.workDataWeight);
  const peopleAlignment = 5 - Math.abs(assessmentData.workingWithPeople - career.workPeopleWeight);
  const creativityAlignment = 5 - Math.abs(assessmentData.creativeTasks - career.creativityWeight);
  const problemSolvingAlignment = 5 - Math.abs(assessmentData.problemSolving - career.problemSolvingWeight);
  const leadershipAlignment = 5 - Math.abs(assessmentData.leadership - career.leadershipWeight);
  
  let tradesAlignments: number[] = [];
  
  if (assessmentData.physicalHandsOnWork && career.handsOnWorkWeight) {
    tradesAlignments.push(5 - Math.abs(assessmentData.physicalHandsOnWork - career.handsOnWorkWeight));
  }
  
  if (assessmentData.mechanicalAptitude && career.mechanicalAptitudeWeight) {
    tradesAlignments.push(5 - Math.abs(assessmentData.mechanicalAptitude - career.mechanicalAptitudeWeight));
  }
  
  if (assessmentData.outdoorWork && career.outdoorWorkWeight) {
    tradesAlignments.push(5 - Math.abs(assessmentData.outdoorWork - career.outdoorWorkWeight));
  }
  
  const coreAlignments = [dataAlignment, peopleAlignment, creativityAlignment, problemSolvingAlignment, leadershipAlignment];
  const allAlignments = [...coreAlignments, ...tradesAlignments];
  
  const avgAlignment = allAlignments.reduce((sum, val) => sum + val, 0) / allAlignments.length;
  const workPrefScore = (avgAlignment / 5) * weights.workPrefs;
  
  totalScore += workPrefScore;
  maxPossibleScore += weights.workPrefs;
  
  if (avgAlignment >= 4.0) {
    matchReasons.push("Excellent work preferences alignment");
  } else if (avgAlignment >= 3.5) {
    matchReasons.push("Strong work preferences alignment");
  } else if (avgAlignment >= 2.5) {
    matchReasons.push("Good work style compatibility");
  } else if (explorationLevel === 3) {
    matchReasons.push("Different work style - new perspective opportunity");
  }

  // FIXED: Much more generous industry alignment for Adventure Zone with defensive programming
  const userIndustries = Array.isArray(assessmentData.industries) ? assessmentData.industries : [];
  const careerIndustries = Array.isArray(career.preferredIndustries) ? career.preferredIndustries : [];
  
  const industryMatches = careerIndustries.filter(industry => 
    userIndustries.some(userIndustry => 
      userIndustry.toLowerCase().includes(industry.toLowerCase()) ||
      industry.toLowerCase().includes(userIndustry.toLowerCase())
    )
  );
  
  let industryScore;
  if (careerIndustries.length === 0) {
    industryScore = weights.industry * 0.8;
  } else if (industryMatches.length === 0) {
    // FIXED: Adventure Zone gives high scores for new industries
    industryScore = explorationLevel === 3 ? weights.industry * 0.8 : weights.industry * 0.4;
  } else {
    industryScore = (industryMatches.length / careerIndustries.length) * weights.industry;
  }
  
  totalScore += industryScore;
  maxPossibleScore += weights.industry;
  
  if (industryMatches.length > 0) {
    matchReasons.push("Industry alignment");
  } else if (explorationLevel === 3) {
    matchReasons.push("New industry exploration opportunity");
  }

  // FIXED: Much more generous interest alignment for Adventure Zone with defensive programming
  const userInterests = Array.isArray(assessmentData.interests) ? assessmentData.interests : [];
  const careerInterests = Array.isArray(career.preferredInterests) ? career.preferredInterests : [];
  
  const interestMatches = careerInterests.filter(interest => 
    userInterests.some(userInterest => 
      userInterest.toLowerCase().includes(interest.toLowerCase()) ||
      interest.toLowerCase().includes(userInterest.toLowerCase())
    )
  );
  
  let interestScore;
  if (careerInterests.length === 0) {
    interestScore = weights.interests * 0.8;
  } else if (interestMatches.length === 0) {
    // FIXED: Adventure Zone gives high scores for new interests
    interestScore = explorationLevel === 3 ? weights.interests * 0.8 : weights.interests * 0.4;
  } else {
    interestScore = (interestMatches.length / careerInterests.length) * weights.interests;
  }
  
  totalScore += interestScore;
  maxPossibleScore += weights.interests;
  
  if (interestMatches.length > 0) {
    matchReasons.push("Shared interests");
  } else if (explorationLevel === 3) {
    matchReasons.push("New interest area to explore");
  }

  // Calculate final score
  let relevanceScore = Math.round((totalScore / maxPossibleScore) * 100);
  
  // FIXED: Adventure Zone gets more generous minimum scores, BUT higher minimums for safety-critical careers AND minimal profiles
  let minScore;
  if (explorationLevel === 1) {
    minScore = 60;
  } else if (explorationLevel === 2) {
    minScore = 50;
  } else {
    // Adventure Zone: Check for minimal profile
    const hasMinimalProfile = (
      (!assessmentData.resumeText || assessmentData.resumeText.length < 50) &&
      (!assessmentData.technicalSkills || assessmentData.technicalSkills.length === 0)
    );
    
    // Higher minimum scores for safety-critical careers and minimal profiles
    if (isSafetyCriticalCareer(career)) {
      minScore = 70; // Safety-critical careers need high relevance
    } else if (hasMinimalProfile) {
      minScore = 60; // Minimal profiles need higher relevance to prevent inappropriate recommendations
    } else {
      minScore = 35; // Standard Adventure Zone minimum
    }
  }
  relevanceScore = Math.max(minScore, relevanceScore);
  
  // FIXED: Adventure Zone gets bigger bonuses for work preference alignment
  if (explorationLevel === 3) {
    if (avgAlignment >= 3.5) {
      relevanceScore = Math.min(95, relevanceScore + 20); // Bigger bonus
    } else if (avgAlignment >= 2.5) {
      relevanceScore = Math.min(90, relevanceScore + 15); // Bigger bonus
    } else {
      relevanceScore = Math.min(85, relevanceScore + 10); // Still generous
    }
  }
  
  if (matchReasons.length === 0) {
    matchReasons.push(explorationLevel === 3 ? "Unexplored career opportunity" : "Profile compatibility");
  }

  const confidenceLevel = Math.min(95, relevanceScore + Math.random() * 10 - 5);

  return {
    ...career,
    relevanceScore,
    confidenceLevel: Math.round(confidenceLevel),
    matchReasons: matchReasons.slice(0, 4)
  };
};

// Keep existing helper functions for compatibility
export const parseEducationLevel = (education: string): number => {
  switch (education) {
    case 'high-school': return 1;
    case 'some-college': return 2;
    case 'trade-school': return 2.5;
    case 'associates': return 3;
    case 'certificate': return 3.5;
    case 'bachelors': return 4;
    case 'masters': return 5;
    case 'doctorate': return 6;
    case 'other': return 2;
    default: return 1;
  }
};

export const parseSalaryExpectation = (salaryExp: string): { min: number, max: number } => {
  switch (salaryExp) {
    case 'under-30k': return { min: 0, max: 30000 };
    case '30k-50k': return { min: 30000, max: 50000 };
    case '50k-70k': return { min: 50000, max: 70000 };
    case '70k-100k': return { min: 70000, max: 100000 };
    case '100k-150k': return { min: 100000, max: 150000 };
    case '150k-250k': return { min: 150000, max: 250000 };
    case '250k-plus': return { min: 250000, max: 500000 };
    case 'flexible': return { min: 0, max: 500000 };
    default: return { min: 0, max: 500000 };
  }
};

export const extractResumeSkills = (resumeText: string): string[] => {
  const skillKeywords = [
    'excel', 'sql', 'python', 'javascript', 'project management', 'data analysis',
    'leadership', 'communication', 'problem solving', 'teamwork', 'figma', 'adobe',
    'product management', 'user research', 'agile', 'scrum'
  ];
  
  const lowerText = resumeText.toLowerCase();
  return skillKeywords.filter(skill => lowerText.includes(skill));
};

export const analyzeResumeContent = (resumeText: string) => {
  return {
    extractedSkills: extractResumeSkills(resumeText),
    jobTitles: [],
    companies: [],
    industries: [],
    experienceLevel: 'unknown',
    careerProgression: [],
    achievements: [],
    educationMentions: [],
    certificationMentions: []
  };
};