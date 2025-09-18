// ========================================
// COMPREHENSIVE TRADES & ENTRY-LEVEL CAREER TEMPLATES
// ========================================
// Enhanced career paths for skilled trades, entry-level, and service industries
// NOW WITH: Trades-specific work preference weights and comprehensive coverage

import { CareerTemplate } from './careerMatching';

export const TRADES_CAREER_TEMPLATES: CareerTemplate[] = [
  // ========================================
  // SKILLED TRADES - ELECTRICAL
  // ========================================
  {
    title: "Apprentice Electrician",
    salaryRange: "$35,000 - $45,000",
    description: "Learn electrical installation, maintenance, and repair under supervision of licensed electricians. Start your journey in the electrical trades with hands-on training and classroom instruction.",
    requiredTechnicalSkills: ["Basic Math", "Hand Tools", "Safety Procedures", "Blueprint Reading"],
    requiredSoftSkills: ["Attention to Detail", "Problem Solving", "Physical Stamina", "Teamwork"],
    preferredInterests: ["Technology", "Building/Construction", "Problem Solving", "Hands-on Projects"],
    preferredIndustries: ["Construction", "Electrical Services", "Manufacturing", "Utilities"],
    workDataWeight: 2,
    workPeopleWeight: 3,
    creativityWeight: 2,
    problemSolvingWeight: 4,
    leadershipWeight: 2,
    learningPath: "4-year apprenticeship program",
    stretchLevel: "safe",
    careerType: "apprentice-electrician",
    requiresTechnical: true,
    companies: ["Local Electrical Contractors", "IBEW Union", "Industrial Plants", "Construction Companies"],
    dayInLife: "Start your day at 6:30 AM with safety briefing and tool check. Morning involves learning wire installation techniques under journeyman supervision, practicing conduit bending, and studying electrical codes. Afternoon includes hands-on work installing outlets and switches, troubleshooting basic electrical issues, and attending trade school classes twice a week. End day by cleaning work area and preparing for tomorrow's lessons.",
    experienceLevel: "entry",
    minYearsExperience: 0,
    maxYearsExperience: 1,
    salaryMin: 35000,
    salaryMax: 45000,
    remoteOptions: "None - hands-on trade work",
    workEnvironments: ["construction", "industrial", "outdoor"],
    
    requiredEducation: "high-school",
    preferredEducation: "high-school",
    valuedCertifications: ["OSHA 10", "Basic Electrical Safety", "First Aid/CPR"],
    requiredCertifications: [],
    workLifeBalanceRating: 3,
    agePreference: "18-35",
    locationFlexibility: "local-area",
    transitionFriendly: true,
    resumeKeywords: ["electrical", "apprentice", "construction", "maintenance", "wiring", "tools", "safety"],
    relatedJobTitles: ["Construction Helper", "Maintenance Assistant", "Electrical Helper"],
    valuedCompanies: ["Local Electrical Contractors", "IBEW", "Utility Companies"],
    preferredIndustryExperience: ["Construction", "Manufacturing", "Maintenance"],
    careerProgressionPatterns: ["High School → Apprentice → Journeyman → Master Electrician"],
    
    alternativeQualifications: ["High school diploma", "Physical ability", "Basic math skills", "Willingness to learn"],
    skillBasedEntry: true,
    experienceCanSubstitute: false,
    
    // NEW: Trades-specific work preference weights
    handsOnWorkWeight: 5, // Maximum hands-on work
    physicalWorkWeight: 4, // High physical demands
    outdoorWorkWeight: 3, // Some outdoor work
    mechanicalAptitudeWeight: 4 // High mechanical aptitude needed
  },

  {
    title: "Journeyman Electrician",
    salaryRange: "$55,000 - $75,000",
    description: "Licensed electrician capable of installing, maintaining, and repairing electrical systems independently. Lead apprentices and handle complex electrical projects in residential, commercial, and industrial settings.",
    requiredTechnicalSkills: ["Electrical Code Knowledge", "Blueprint Reading", "Electrical Testing", "Motor Controls"],
    requiredSoftSkills: ["Leadership", "Problem Solving", "Communication", "Time Management"],
    preferredInterests: ["Technology", "Building/Construction", "Problem Solving", "Mechanical Systems"],
    preferredIndustries: ["Construction", "Electrical Services", "Manufacturing", "Utilities"],
    workDataWeight: 3,
    workPeopleWeight: 4,
    creativityWeight: 3,
    problemSolvingWeight: 5,
    leadershipWeight: 4,
    learningPath: "Complete 4-year apprenticeship + licensing exam",
    stretchLevel: "safe",
    careerType: "journeyman-electrician",
    requiresTechnical: true,
    companies: ["Electrical Contractors", "Industrial Plants", "Utility Companies", "Government Facilities"],
    dayInLife: "Begin at 7:00 AM reviewing project plans and assigning tasks to apprentices. Morning involves installing complex electrical systems, troubleshooting power distribution issues, and ensuring code compliance. Afternoon includes leading a team on commercial wiring project, mentoring apprentices, and coordinating with other trades. Finish by completing daily reports and planning tomorrow's work schedule.",
    experienceLevel: "mid",
    minYearsExperience: 4,
    maxYearsExperience: 10,
    salaryMin: 55000,
    salaryMax: 75000,
    remoteOptions: "None - hands-on trade work",
    workEnvironments: ["construction", "industrial", "outdoor"],
    
    requiredEducation: "high-school",
    preferredEducation: "trade-school",
    valuedCertifications: ["Journeyman License", "OSHA 30", "NFPA 70E", "Motor Control"],
    requiredCertifications: ["Journeyman Electrician License"],
    workLifeBalanceRating: 3,
    agePreference: "22-50",
    locationFlexibility: "regional",
    transitionFriendly: false,
    resumeKeywords: ["journeyman", "licensed electrician", "electrical systems", "code compliance", "leadership"],
    relatedJobTitles: ["Electrical Technician", "Maintenance Electrician", "Industrial Electrician"],
    valuedCompanies: ["Major Electrical Contractors", "Industrial Plants", "Utility Companies"],
    preferredIndustryExperience: ["Electrical Construction", "Industrial Maintenance", "Utilities"],
    careerProgressionPatterns: ["Apprentice → Journeyman → Master Electrician → Electrical Contractor"],
    
    alternativeQualifications: ["Completed apprenticeship", "Journeyman license", "4+ years experience"],
    skillBasedEntry: false,
    experienceCanSubstitute: false,
    
    // NEW: Trades-specific work preference weights
    handsOnWorkWeight: 5, // Maximum hands-on work
    physicalWorkWeight: 4, // High physical demands
    outdoorWorkWeight: 3, // Some outdoor work
    mechanicalAptitudeWeight: 5 // Maximum mechanical aptitude needed
  },

  // ========================================
  // SKILLED TRADES - PLUMBING
  // ========================================
  {
    title: "Plumbing Apprentice",
    salaryRange: "$32,000 - $42,000",
    description: "Learn plumbing installation, repair, and maintenance under licensed plumber supervision. Gain hands-on experience with pipes, fixtures, and water systems in residential and commercial settings.",
    requiredTechnicalSkills: ["Basic Math", "Hand Tools", "Pipe Fitting", "Safety Procedures"],
    requiredSoftSkills: ["Physical Stamina", "Problem Solving", "Attention to Detail", "Reliability"],
    preferredInterests: ["Building/Construction", "Problem Solving", "Hands-on Work", "Mechanical Systems"],
    preferredIndustries: ["Construction", "Plumbing Services", "Maintenance"],
    workDataWeight: 2,
    workPeopleWeight: 3,
    creativityWeight: 2,
    problemSolvingWeight: 4,
    leadershipWeight: 2,
    learningPath: "4-5 year apprenticeship program",
    stretchLevel: "safe",
    careerType: "plumbing-apprentice",
    requiresTechnical: true,
    companies: ["Local Plumbing Contractors", "Construction Companies", "Maintenance Services"],
    dayInLife: "Start at 7:00 AM with tool preparation and safety review. Morning includes learning pipe installation techniques, practicing soldering and fitting connections, and assisting with drain cleaning. Afternoon involves hands-on work installing fixtures, learning water heater maintenance, and attending trade school classes. End day organizing tools and reviewing plumbing codes.",
    experienceLevel: "entry",
    minYearsExperience: 0,
    maxYearsExperience: 1,
    salaryMin: 32000,
    salaryMax: 42000,
    remoteOptions: "None - hands-on trade work",
    workEnvironments: ["construction", "residential", "commercial"],
    
    requiredEducation: "high-school",
    preferredEducation: "high-school",
    valuedCertifications: ["OSHA 10", "Basic Plumbing Safety", "First Aid"],
    requiredCertifications: [],
    workLifeBalanceRating: 3,
    agePreference: "18-35",
    locationFlexibility: "local-area",
    transitionFriendly: true,
    resumeKeywords: ["plumbing", "apprentice", "pipes", "fixtures", "construction", "maintenance"],
    relatedJobTitles: ["Construction Helper", "Maintenance Helper", "Pipe Fitter Helper"],
    valuedCompanies: ["Local Plumbing Companies", "Construction Contractors", "Property Management"],
    preferredIndustryExperience: ["Construction", "Maintenance", "Home Services"],
    careerProgressionPatterns: ["High School → Apprentice → Journeyman → Master Plumber"],
    
    alternativeQualifications: ["High school diploma", "Physical fitness", "Mechanical aptitude", "Reliability"],
    skillBasedEntry: true,
    experienceCanSubstitute: false,
    
    // NEW: Trades-specific work preference weights
    handsOnWorkWeight: 5, // Maximum hands-on work
    physicalWorkWeight: 5, // Maximum physical demands (crawling, lifting)
    outdoorWorkWeight: 2, // Mostly indoor work
    mechanicalAptitudeWeight: 4 // High mechanical aptitude needed
  },

  // ========================================
  // SKILLED TRADES - HVAC
  // ========================================
  {
    title: "HVAC Technician",
    salaryRange: "$45,000 - $65,000",
    description: "Install, maintain, and repair heating, ventilation, and air conditioning systems. Work on residential and commercial HVAC equipment, troubleshoot system problems, and ensure optimal climate control performance.",
    requiredTechnicalSkills: ["HVAC Systems", "Electrical Basics", "Refrigeration", "System Diagnostics"],
    requiredSoftSkills: ["Problem Solving", "Customer Service", "Physical Stamina", "Attention to Detail"],
    preferredInterests: ["Technology", "Problem Solving", "Mechanical Systems", "Hands-on Projects"],
    preferredIndustries: ["HVAC Services", "Construction", "Facilities Management"],
    workDataWeight: 3,
    workPeopleWeight: 4,
    creativityWeight: 3,
    problemSolvingWeight: 5,
    leadershipWeight: 3,
    learningPath: "6-month to 2-year HVAC program + EPA certification",
    stretchLevel: "safe",
    careerType: "hvac-technician",
    requiresTechnical: true,
    companies: ["HVAC Contractors", "Property Management", "Facilities Services", "Retail Chains"],
    dayInLife: "Begin at 8:00 AM checking service calls and loading truck with parts and tools. Morning involves diagnosing AC system problems, replacing faulty components, and performing routine maintenance. Afternoon includes installing new HVAC units, explaining system operation to customers, and completing service reports. End day restocking truck and planning next day's appointments.",
    experienceLevel: "mid",
    minYearsExperience: 1,
    maxYearsExperience: 8,
    salaryMin: 45000,
    salaryMax: 65000,
    remoteOptions: "None - field service work",
    workEnvironments: ["field service", "construction", "commercial"],
    
    requiredEducation: "high-school",
    preferredEducation: "trade-school",
    valuedCertifications: ["EPA 608", "NATE Certification", "OSHA 10", "Refrigeration License"],
    requiredCertifications: ["EPA 608 Certification"],
    workLifeBalanceRating: 3,
    agePreference: "20-50",
    locationFlexibility: "regional",
    transitionFriendly: true,
    resumeKeywords: ["hvac", "air conditioning", "heating", "refrigeration", "maintenance", "repair"],
    relatedJobTitles: ["Maintenance Technician", "Refrigeration Technician", "Building Engineer"],
    valuedCompanies: ["Major HVAC Contractors", "Property Management Companies", "Facilities Services"],
    preferredIndustryExperience: ["HVAC", "Maintenance", "Construction", "Facilities"],
    careerProgressionPatterns: ["Helper → Technician → Senior Tech → Service Manager"],
    
    alternativeQualifications: ["Trade school completion", "EPA certification", "Mechanical aptitude", "Customer service skills"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    
    // NEW: Trades-specific work preference weights
    handsOnWorkWeight: 5, // Maximum hands-on work
    physicalWorkWeight: 4, // High physical demands (climbing, lifting)
    outdoorWorkWeight: 3, // Some outdoor work (rooftop units)
    mechanicalAptitudeWeight: 5 // Maximum mechanical aptitude needed
  },

  // ========================================
  // ENTRY-LEVEL SERVICE INDUSTRY
  // ========================================
  {
    title: "Customer Service Representative",
    salaryRange: "$28,000 - $38,000",
    description: "Handle customer inquiries, resolve complaints, and provide product information via phone, email, or chat. Build communication skills while learning business operations and customer relationship management.",
    requiredTechnicalSkills: ["Computer Basics", "Phone Systems", "Data Entry", "CRM Software"],
    requiredSoftSkills: ["Communication", "Patience", "Problem Solving", "Active Listening"],
    preferredInterests: ["Helping People", "Communication", "Problem Solving"],
    preferredIndustries: ["Retail", "Healthcare", "Financial Services", "Technology"],
    workDataWeight: 3,
    workPeopleWeight: 5,
    creativityWeight: 2,
    problemSolvingWeight: 4,
    leadershipWeight: 2,
    learningPath: "On-the-job training + customer service certification",
    stretchLevel: "safe",
    careerType: "customer-service-rep",
    requiresTechnical: false,
    companies: ["Call Centers", "Retail Companies", "Banks", "Insurance Companies", "Tech Support"],
    dayInLife: "Start at 9:00 AM logging into phone system and reviewing daily goals. Morning involves answering customer calls, resolving billing issues, and updating customer accounts. Afternoon includes handling live chat support, escalating complex issues to supervisors, and participating in product training. End day completing call summaries and preparing for tomorrow's shift.",
    experienceLevel: "entry",
    minYearsExperience: 0,
    maxYearsExperience: 3,
    salaryMin: 28000,
    salaryMax: 38000,
    remoteOptions: "High - 70% of positions offer remote work",
    workEnvironments: ["office", "remote", "call center"],
    
    requiredEducation: "high-school",
    preferredEducation: "high-school",
    valuedCertifications: ["Customer Service", "Microsoft Office", "Communication Skills"],
    requiredCertifications: [],
    workLifeBalanceRating: 4,
    agePreference: "18-45",
    locationFlexibility: "very-flexible",
    transitionFriendly: true,
    resumeKeywords: ["customer service", "communication", "problem solving", "phone support", "data entry"],
    relatedJobTitles: ["Call Center Agent", "Support Specialist", "Client Services", "Help Desk"],
    valuedCompanies: ["Major Retailers", "Banks", "Insurance Companies", "Tech Companies"],
    preferredIndustryExperience: ["Retail", "Hospitality", "Any customer-facing role"],
    careerProgressionPatterns: ["CSR → Senior CSR → Team Lead → Supervisor → Manager"],
    
    alternativeQualifications: ["High school diploma", "Good communication skills", "Computer literacy", "Patience with customers"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    
    // NEW: Trades-specific work preference weights (low for office role)
    handsOnWorkWeight: 1, // Minimal hands-on work
    physicalWorkWeight: 1, // Sedentary work
    outdoorWorkWeight: 1, // Indoor office work
    mechanicalAptitudeWeight: 2 // Basic technical skills needed
  },

  {
    title: "Retail Sales Associate",
    salaryRange: "$25,000 - $35,000",
    description: "Assist customers with product selection, process transactions, and maintain store appearance. Learn sales techniques, inventory management, and customer service skills that transfer to many industries.",
    requiredTechnicalSkills: ["Point of Sale Systems", "Inventory Management", "Basic Math", "Product Knowledge"],
    requiredSoftSkills: ["Customer Service", "Communication", "Teamwork", "Reliability"],
    preferredInterests: ["Helping People", "Sales", "Fashion/Products"],
    preferredIndustries: ["Retail", "Fashion", "Electronics", "Home Improvement"],
    workDataWeight: 2,
    workPeopleWeight: 5,
    creativityWeight: 3,
    problemSolvingWeight: 3,
    leadershipWeight: 2,
    learningPath: "On-the-job training + retail management courses",
    stretchLevel: "safe",
    careerType: "retail-sales-associate",
    requiresTechnical: false,
    companies: ["Target", "Walmart", "Best Buy", "Home Depot", "Macy's", "Local Retailers"],
    dayInLife: "Arrive at 10:00 AM for opening procedures and team briefing. Morning includes helping customers find products, processing returns and exchanges, and restocking merchandise. Afternoon involves working the register during busy periods, assisting with inventory counts, and learning about new products. End shift by cleaning work area and preparing store for closing.",
    experienceLevel: "entry",
    minYearsExperience: 0,
    maxYearsExperience: 2,
    salaryMin: 25000,
    salaryMax: 35000,
    remoteOptions: "None - in-person retail work",
    workEnvironments: ["retail", "customer-facing"],
    
    requiredEducation: "high-school",
    preferredEducation: "high-school",
    valuedCertifications: ["Customer Service", "Sales Training", "Product Knowledge"],
    requiredCertifications: [],
    workLifeBalanceRating: 3,
    agePreference: "16-40",
    locationFlexibility: "local-area",
    transitionFriendly: true,
    resumeKeywords: ["retail", "sales", "customer service", "cash handling", "inventory", "teamwork"],
    relatedJobTitles: ["Cashier", "Sales Clerk", "Store Associate", "Customer Service"],
    valuedCompanies: ["Major Retailers", "Department Stores", "Specialty Stores"],
    preferredIndustryExperience: ["Any customer service", "Food service", "Hospitality"],
    careerProgressionPatterns: ["Associate → Senior Associate → Team Lead → Assistant Manager → Store Manager"],
    
    alternativeQualifications: ["High school diploma", "Customer service attitude", "Reliability", "Basic math skills"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    
    // NEW: Trades-specific work preference weights (low for retail role)
    handsOnWorkWeight: 2, // Some hands-on work (stocking, displays)
    physicalWorkWeight: 3, // Moderate physical work (standing, lifting)
    outdoorWorkWeight: 1, // Indoor retail work
    mechanicalAptitudeWeight: 1 // Minimal mechanical skills needed
  },

  // ========================================
  // MANUFACTURING & PRODUCTION
  // ========================================
  {
    title: "Production Worker",
    salaryRange: "$30,000 - $42,000",
    description: "Operate manufacturing equipment, assemble products, and maintain quality standards in production environment. Learn manufacturing processes, safety procedures, and quality control while building toward supervisory roles.",
    requiredTechnicalSkills: ["Machine Operation", "Quality Control", "Safety Procedures", "Basic Maintenance"],
    requiredSoftSkills: ["Attention to Detail", "Reliability", "Teamwork", "Physical Stamina"],
    preferredInterests: ["Manufacturing", "Hands-on Work", "Mechanical Systems"],
    preferredIndustries: ["Manufacturing", "Automotive", "Food Production", "Electronics"],
    workDataWeight: 3,
    workPeopleWeight: 3,
    creativityWeight: 2,
    problemSolvingWeight: 3,
    leadershipWeight: 2,
    learningPath: "On-the-job training + manufacturing certifications",
    stretchLevel: "safe",
    careerType: "production-worker",
    requiresTechnical: true,
    companies: ["Manufacturing Plants", "Automotive Companies", "Food Processors", "Electronics Manufacturers"],
    dayInLife: "Clock in at 6:00 AM for shift briefing and safety review. Morning involves operating production machinery, monitoring quality standards, and following work instructions. Afternoon includes rotating to different stations, participating in continuous improvement activities, and maintaining equipment. End shift by cleaning work area and reporting production metrics.",
    experienceLevel: "entry",
    minYearsExperience: 0,
    maxYearsExperience: 3,
    salaryMin: 30000,
    salaryMax: 42000,
    remoteOptions: "None - manufacturing floor work",
    workEnvironments: ["manufacturing", "industrial"],
    
    requiredEducation: "high-school",
    preferredEducation: "high-school",
    valuedCertifications: ["OSHA 10", "Forklift License", "Quality Control", "Lean Manufacturing"],
    requiredCertifications: [],
    workLifeBalanceRating: 3,
    agePreference: "18-55",
    locationFlexibility: "local-area",
    transitionFriendly: true,
    resumeKeywords: ["production", "manufacturing", "assembly", "quality control", "safety", "machinery"],
    relatedJobTitles: ["Assembly Worker", "Machine Operator", "Quality Inspector", "Warehouse Worker"],
    valuedCompanies: ["Manufacturing Companies", "Automotive Plants", "Food Processors"],
    preferredIndustryExperience: ["Any hands-on work", "Construction", "Maintenance"],
    careerProgressionPatterns: ["Production Worker → Lead Worker → Supervisor → Production Manager"],
    
    alternativeQualifications: ["High school diploma", "Physical ability", "Reliability", "Willingness to learn"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    
    // NEW: Trades-specific work preference weights
    handsOnWorkWeight: 4, // High hands-on work
    physicalWorkWeight: 4, // High physical demands
    outdoorWorkWeight: 1, // Indoor manufacturing work
    mechanicalAptitudeWeight: 4 // High mechanical aptitude helpful
  },

  // ========================================
  // TRANSPORTATION & LOGISTICS
  // ========================================
  {
    title: "Delivery Driver",
    salaryRange: "$32,000 - $48,000",
    description: "Transport goods and packages to customers, maintain delivery schedules, and provide excellent customer service. Build logistics knowledge and customer relationships while developing toward fleet management or logistics coordination roles.",
    requiredTechnicalSkills: ["Safe Driving", "Route Planning", "GPS Navigation", "Vehicle Maintenance"],
    requiredSoftSkills: ["Customer Service", "Time Management", "Reliability", "Physical Stamina"],
    preferredInterests: ["Driving", "Customer Service", "Independence"],
    preferredIndustries: ["Logistics", "E-commerce", "Food Delivery", "Package Delivery"],
    workDataWeight: 2,
    workPeopleWeight: 4,
    creativityWeight: 2,
    problemSolvingWeight: 3,
    leadershipWeight: 2,
    learningPath: "CDL training + logistics certifications",
    stretchLevel: "safe",
    careerType: "delivery-driver",
    requiresTechnical: true,
    companies: ["UPS", "FedEx", "Amazon", "DoorDash", "Local Delivery Services"],
    dayInLife: "Start at 7:00 AM with vehicle inspection and route planning. Morning involves loading packages, following delivery schedule, and providing friendly customer service. Afternoon includes navigating traffic efficiently, handling special delivery requests, and maintaining delivery records. End day by returning vehicle, completing paperwork, and preparing for next day's route.",
    experienceLevel: "entry",
    minYearsExperience: 0,
    maxYearsExperience: 5,
    salaryMin: 32000,
    salaryMax: 48000,
    remoteOptions: "None - driving/delivery work",
    workEnvironments: ["driving", "customer-facing", "outdoor"],
    
    requiredEducation: "high-school",
    preferredEducation: "high-school",
    valuedCertifications: ["CDL License", "DOT Physical", "Defensive Driving", "Customer Service"],
    requiredCertifications: ["Valid Driver's License"],
    workLifeBalanceRating: 3,
    agePreference: "21-60",
    locationFlexibility: "local-regional",
    transitionFriendly: true,
    resumeKeywords: ["delivery", "driving", "customer service", "logistics", "route planning", "cdl"],
    relatedJobTitles: ["Truck Driver", "Courier", "Route Driver", "Package Handler"],
    valuedCompanies: ["UPS", "FedEx", "Amazon", "Local Delivery Companies"],
    preferredIndustryExperience: ["Any driving experience", "Customer service", "Physical work"],
    careerProgressionPatterns: ["Driver → Senior Driver → Dispatcher → Fleet Manager"],
    
    alternativeQualifications: ["Clean driving record", "Customer service skills", "Physical fitness", "Reliability"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    
    // NEW: Trades-specific work preference weights
    handsOnWorkWeight: 3, // Moderate hands-on work (loading, vehicle maintenance)
    physicalWorkWeight: 4, // High physical demands (lifting packages)
    outdoorWorkWeight: 4, // High outdoor work
    mechanicalAptitudeWeight: 3 // Moderate mechanical skills helpful
  },

  // ========================================
  // HEALTHCARE SUPPORT
  // ========================================
  {
    title: "Medical Assistant",
    salaryRange: "$32,000 - $42,000",
    description: "Support healthcare providers by taking vital signs, preparing patients for examinations, and handling administrative tasks. Gain healthcare experience while building toward nursing or other medical careers.",
    requiredTechnicalSkills: ["Medical Terminology", "Vital Signs", "Electronic Health Records", "Basic Medical Procedures"],
    requiredSoftSkills: ["Compassion", "Communication", "Attention to Detail", "Multitasking"],
    preferredInterests: ["Healthcare", "Helping People", "Medical Science"],
    preferredIndustries: ["Healthcare", "Medical Clinics", "Hospitals"],
    workDataWeight: 3,
    workPeopleWeight: 5,
    creativityWeight: 2,
    problemSolvingWeight: 3,
    leadershipWeight: 2,
    learningPath: "9-month to 2-year medical assistant program",
    stretchLevel: "safe",
    careerType: "medical-assistant",
    requiresTechnical: true,
    companies: ["Medical Clinics", "Hospitals", "Urgent Care Centers", "Specialty Practices"],
    dayInLife: "Arrive at 8:00 AM to prepare exam rooms and review patient schedules. Morning involves taking patient vital signs, updating medical records, and assisting with examinations. Afternoon includes scheduling appointments, handling insurance verification, and supporting medical procedures. End day by cleaning equipment and preparing for next day's patients.",
    experienceLevel: "entry",
    minYearsExperience: 0,
    maxYearsExperience: 3,
    salaryMin: 32000,
    salaryMax: 42000,
    remoteOptions: "Low - mostly in-person patient care",
    workEnvironments: ["medical facility", "clinic", "hospital"],
    
    requiredEducation: "high-school",
    preferredEducation: "certificate",
    valuedCertifications: ["Medical Assistant Certification", "CPR", "First Aid", "HIPAA Training"],
    requiredCertifications: ["Medical Assistant Certification"],
    workLifeBalanceRating: 4,
    agePreference: "18-50",
    locationFlexibility: "local-area",
    transitionFriendly: true,
    resumeKeywords: ["medical assistant", "healthcare", "patient care", "medical records", "vital signs"],
    relatedJobTitles: ["Healthcare Assistant", "Clinical Assistant", "Patient Care Technician"],
    valuedCompanies: ["Hospitals", "Medical Clinics", "Healthcare Systems"],
    preferredIndustryExperience: ["Healthcare", "Customer service", "Administrative work"],
    careerProgressionPatterns: ["Medical Assistant → Senior MA → Office Manager → Practice Administrator"],
    
    alternativeQualifications: ["Medical assistant certification", "Healthcare experience", "Compassionate nature", "Detail-oriented"],
    skillBasedEntry: false,
    experienceCanSubstitute: false,
    
    // NEW: Trades-specific work preference weights (low for healthcare role)
    handsOnWorkWeight: 2, // Some hands-on work (patient care)
    physicalWorkWeight: 3, // Moderate physical work (standing, moving)
    outdoorWorkWeight: 1, // Indoor medical facility work
    mechanicalAptitudeWeight: 2 // Basic technical skills for medical equipment
  },

  // ========================================
  // ADDITIONAL COMPREHENSIVE TRADES CAREERS
  // ========================================
  {
    title: "Automotive Technician",
    salaryRange: "$38,000 - $58,000",
    description: "Diagnose, repair, and maintain vehicles using advanced diagnostic equipment and hand tools. Work on engines, brakes, electrical systems, and other automotive components in dealerships or independent shops.",
    requiredTechnicalSkills: ["Automotive Repair", "Engine Diagnostics", "Electrical Systems", "Brake Systems"],
    requiredSoftSkills: ["Problem Solving", "Attention to Detail", "Customer Service", "Physical Stamina"],
    preferredInterests: ["Automotive", "Mechanical Systems", "Problem Solving", "Technology"],
    preferredIndustries: ["Automotive", "Transportation", "Manufacturing"],
    workDataWeight: 2,
    workPeopleWeight: 3,
    creativityWeight: 3,
    problemSolvingWeight: 5,
    leadershipWeight: 2,
    learningPath: "2-year automotive program + ASE certification",
    stretchLevel: "safe",
    careerType: "automotive-technician",
    requiresTechnical: true,
    companies: ["Auto Dealerships", "Independent Repair Shops", "Quick Lube Chains", "Fleet Services"],
    dayInLife: "Start at 8:00 AM reviewing work orders and gathering tools. Morning involves diagnosing engine problems using computer scanners, replacing brake pads, and performing oil changes. Afternoon includes electrical system troubleshooting, explaining repairs to customers, and completing detailed service reports. End day by cleaning workspace and preparing for tomorrow's appointments.",
    experienceLevel: "mid",
    minYearsExperience: 1,
    maxYearsExperience: 8,
    salaryMin: 38000,
    salaryMax: 58000,
    remoteOptions: "None - hands-on automotive work",
    workEnvironments: ["automotive shop", "indoor", "commercial"],
    
    requiredEducation: "high-school",
    preferredEducation: "trade-school",
    valuedCertifications: ["ASE Certification", "Automotive Service Excellence", "Manufacturer Training"],
    requiredCertifications: [],
    workLifeBalanceRating: 3,
    agePreference: "18-50",
    locationFlexibility: "local-area",
    transitionFriendly: true,
    resumeKeywords: ["automotive", "mechanic", "repair", "diagnostics", "maintenance", "ase"],
    relatedJobTitles: ["Auto Mechanic", "Service Technician", "Automotive Specialist"],
    valuedCompanies: ["Auto Dealerships", "Jiffy Lube", "Valvoline Instant Oil Change", "Independent Shops"],
    preferredIndustryExperience: ["Automotive", "Mechanical", "Manufacturing"],
    careerProgressionPatterns: ["Lube Tech → Technician → Master Tech → Service Manager"],
    
    alternativeQualifications: ["Automotive training", "Mechanical aptitude", "Problem-solving skills", "Customer service experience"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    
    // NEW: Trades-specific work preference weights
    handsOnWorkWeight: 5, // Maximum hands-on work
    physicalWorkWeight: 4, // High physical demands
    outdoorWorkWeight: 1, // Indoor shop work
    mechanicalAptitudeWeight: 5 // Maximum mechanical aptitude needed
  },

  {
    title: "Welder",
    salaryRange: "$40,000 - $60,000",
    description: "Join metal parts using various welding techniques including MIG, TIG, and stick welding. Work in construction, manufacturing, or fabrication shops creating structural components and repairing metal equipment.",
    requiredTechnicalSkills: ["Welding", "MIG/TIG Welding", "Metal Fabrication", "Blueprint Reading"],
    requiredSoftSkills: ["Attention to Detail", "Physical Stamina", "Safety Consciousness", "Hand-Eye Coordination"],
    preferredInterests: ["Mechanical Systems", "Building/Construction", "Hands-on Projects", "Manufacturing"],
    preferredIndustries: ["Construction", "Manufacturing", "Automotive", "Aerospace"],
    workDataWeight: 1,
    workPeopleWeight: 2,
    creativityWeight: 3,
    problemSolvingWeight: 4,
    leadershipWeight: 2,
    learningPath: "6-month to 2-year welding program + AWS certification",
    stretchLevel: "safe",
    careerType: "welder",
    requiresTechnical: true,
    companies: ["Construction Companies", "Manufacturing Plants", "Fabrication Shops", "Shipyards"],
    dayInLife: "Begin at 7:00 AM with safety equipment check and reviewing blueprints. Morning involves setting up welding equipment, preparing metal surfaces, and welding structural components. Afternoon includes quality inspection of welds, grinding and finishing work, and maintaining welding equipment. End day by cleaning workspace and securing equipment.",
    experienceLevel: "mid",
    minYearsExperience: 1,
    maxYearsExperience: 10,
    salaryMin: 40000,
    salaryMax: 60000,
    remoteOptions: "None - hands-on welding work",
    workEnvironments: ["manufacturing", "construction", "industrial"],
    
    requiredEducation: "high-school",
    preferredEducation: "trade-school",
    valuedCertifications: ["AWS Welding Certification", "OSHA 10", "Structural Welding"],
    requiredCertifications: [],
    workLifeBalanceRating: 3,
    agePreference: "18-55",
    locationFlexibility: "regional",
    transitionFriendly: true,
    resumeKeywords: ["welding", "fabrication", "mig", "tig", "construction", "manufacturing"],
    relatedJobTitles: ["Fabricator", "Metal Worker", "Structural Welder", "Pipe Welder"],
    valuedCompanies: ["Construction Companies", "Manufacturing Plants", "Fabrication Shops"],
    preferredIndustryExperience: ["Construction", "Manufacturing", "Metal Working"],
    careerProgressionPatterns: ["Helper → Welder → Lead Welder → Welding Inspector"],
    
    alternativeQualifications: ["Welding training", "Manual dexterity", "Attention to detail", "Safety consciousness"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    
    // NEW: Trades-specific work preference weights
    handsOnWorkWeight: 5, // Maximum hands-on work
    physicalWorkWeight: 4, // High physical demands
    outdoorWorkWeight: 3, // Some outdoor construction work
    mechanicalAptitudeWeight: 4 // High mechanical aptitude needed
  },

  {
    title: "Construction Laborer",
    salaryRange: "$28,000 - $40,000",
    description: "Perform various physical tasks at construction sites including digging, lifting, carrying materials, and assisting skilled tradespeople. Entry-level position that provides pathway to specialized construction trades.",
    requiredTechnical

: ["Basic Tools", "Safety Procedures", "Construction Materials", "Physical Labor"],
    requiredSoftSkills: ["Physical Stamina", "Teamwork", "Reliability", "Following Instructions"],
    preferredInterests: ["Building/Construction", "Physical Work", "Outdoor Work", "Hands-on Projects"],
    preferredIndustries: ["Construction", "Infrastructure", "Building Trades"],
    workDataWeight: 1,
    workPeopleWeight: 3,
    creativityWeight: 2,
    problemSolvingWeight: 2,
    leadershipWeight: 1,
    learningPath: "On-the-job training + OSHA safety certification",
    stretchLevel: "safe",
    careerType: "construction-laborer",
    requiresTechnical: false,
    companies: ["Construction Companies", "General Contractors", "Infrastructure Projects", "Road Construction"],
    dayInLife: "Start at 6:30 AM with safety briefing and tool distribution. Morning involves digging trenches, moving materials, and assisting carpenters with framing. Afternoon includes cleaning work areas, operating basic equipment, and helping with concrete pours. End day by securing tools and preparing site for next day's work.",
    experienceLevel: "entry",
    minYearsExperience: 0,
    maxYearsExperience: 2,
    salaryMin: 28000,
    salaryMax: 40000,
    remoteOptions: "None - construction site work",
    workEnvironments: ["construction", "outdoor", "industrial"],
    
    requiredEducation: "high-school",
    preferredEducation: "high-school",
    valuedCertifications: ["OSHA 10", "Construction Safety", "First Aid"],
    requiredCertifications: [],
    workLifeBalanceRating: 3,
    agePreference: "18-50",
    locationFlexibility: "local-regional",
    transitionFriendly: true,
    resumeKeywords: ["construction", "laborer", "physical work", "safety", "teamwork"],
    relatedJobTitles: ["Construction Helper", "General Laborer", "Construction Worker"],
    valuedCompanies: ["Construction Companies", "General Contractors", "Infrastructure Companies"],
    preferredIndustryExperience: ["Any physical work", "Landscaping", "Moving/Warehouse"],
    careerProgressionPatterns: ["Laborer → Skilled Helper → Apprentice → Journeyman"],
    
    alternativeQualifications: ["Physical fitness", "Reliability", "Willingness to learn", "Safety consciousness"],
    skillBasedEntry: true,
    experienceCanSubstitute: true,
    
    // NEW: Trades-specific work preference weights
    handsOnWorkWeight: 5, // Maximum hands-on work
    physicalWorkWeight: 5, // Maximum physical demands
    outdoorWorkWeight: 5, // Maximum outdoor work
    mechanicalAptitudeWeight: 2 // Basic mechanical skills helpful
  }
];