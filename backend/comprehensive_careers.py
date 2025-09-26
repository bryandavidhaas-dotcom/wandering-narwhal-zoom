"""
Comprehensive career database with proper salary ranges and experience levels.
Now includes multiple industry clusters for complete career coverage.
"""

# Import additional career clusters
from healthcare_careers import HEALTHCARE_CAREERS
from skilled_trades_careers import SKILLED_TRADES_CAREERS
from education_careers import EDUCATION_CAREERS
from business_finance_careers import BUSINESS_FINANCE_CAREERS
from legal_law_careers import LEGAL_LAW_CAREERS
from creative_arts_careers import CREATIVE_ARTS_CAREERS
from public_service_careers import PUBLIC_SERVICE_CAREERS
from hospitality_service_careers import HOSPITALITY_SERVICE_CAREERS
from manufacturing_industrial_careers import MANUFACTURING_INDUSTRIAL_CAREERS
from agriculture_environment_careers import AGRICULTURE_ENVIRONMENT_CAREERS

# Combine all career databases
COMPREHENSIVE_CAREERS = [
    # EXECUTIVE LEVEL (20+ years, $200k+)
    {
        "title": "Chief Technology Officer",
        "careerType": "cto",
        "description": "Lead technology strategy and vision for the entire organization, manage engineering teams, drive digital transformation.",
        "salaryRange": "$250,000 - $400,000",
        "experienceLevel": "executive",
        "requiredTechnicalSkills": ["Strategic Planning", "Technology Leadership", "System Architecture", "Team Management"],
        "requiredSoftSkills": ["Executive Leadership", "Strategic Thinking", "Communication", "Vision Setting"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Uber"],
        "learningPath": "Executive Leadership Program (6-12 months)",
        "relevanceScore": 75,
        "confidenceLevel": 80,
        "matchReasons": ["Executive leadership experience", "Technology strategy background"],
        "minExperienceYears": 15,
        "maxExperienceYears": 30,
        "minSalary": 250000,
        "maxSalary": 400000
    },
    {
        "title": "VP of Engineering",
        "careerType": "vp-engineering",
        "description": "Oversee all engineering operations, manage multiple engineering teams, drive technical excellence and delivery.",
        "salaryRange": "$220,000 - $350,000",
        "experienceLevel": "executive",
        "requiredTechnicalSkills": ["Engineering Management", "System Architecture", "Team Leadership", "Technical Strategy"],
        "requiredSoftSkills": ["Leadership", "Strategic Planning", "Communication", "Team Building"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Stripe", "Airbnb"],
        "learningPath": "VP Engineering Leadership (6-12 months)",
        "relevanceScore": 75,
        "confidenceLevel": 80,
        "matchReasons": ["Senior engineering leadership", "Team management experience"],
        "minExperienceYears": 12,
        "maxExperienceYears": 25,
        "minSalary": 220000,
        "maxSalary": 350000
    },
    {
        "title": "Chief Data Officer",
        "careerType": "cdo",
        "description": "Lead data strategy across the organization, oversee data science and analytics teams, drive data-driven decision making.",
        "salaryRange": "$230,000 - $380,000",
        "experienceLevel": "executive",
        "requiredTechnicalSkills": ["Data Strategy", "Analytics Leadership", "Machine Learning", "Data Governance"],
        "requiredSoftSkills": ["Executive Leadership", "Strategic Thinking", "Communication", "Change Management"],
        "companies": ["Google", "Microsoft", "Amazon", "Netflix", "Uber", "Airbnb"],
        "learningPath": "Chief Data Officer Program (6-12 months)",
        "relevanceScore": 75,
        "confidenceLevel": 80,
        "matchReasons": ["Data leadership experience", "Analytics strategy background"],
        "minExperienceYears": 15,
        "maxExperienceYears": 30,
        "minSalary": 230000,
        "maxSalary": 380000
    },

    # SENIOR LEVEL (10-20 years, $150k-250k)
    {
        "title": "Principal Software Engineer",
        "careerType": "principal-engineer",
        "description": "Lead complex technical initiatives, architect large-scale systems, mentor senior engineers, drive technical excellence.",
        "salaryRange": "$180,000 - $280,000",
        "experienceLevel": "senior",
        "requiredTechnicalSkills": ["System Architecture", "Advanced Programming", "Technical Leadership", "Distributed Systems"],
        "requiredSoftSkills": ["Technical Leadership", "Mentoring", "Communication", "Problem Solving"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Stripe"],
        "learningPath": "Principal Engineer Track (6-8 months)",
        "relevanceScore": 85,
        "confidenceLevel": 85,
        "matchReasons": ["Senior technical experience", "Architecture background"],
        "minExperienceYears": 10,
        "maxExperienceYears": 20,
        "minSalary": 180000,
        "maxSalary": 280000
    },
    {
        "title": "Senior Data Scientist",
        "careerType": "senior-data-scientist",
        "description": "Lead data science initiatives, build advanced machine learning models, drive data-driven decision making across the organization.",
        "salaryRange": "$160,000 - $240,000",
        "experienceLevel": "senior",
        "requiredTechnicalSkills": ["Python", "Machine Learning", "SQL", "Statistical Analysis", "Deep Learning"],
        "requiredSoftSkills": ["Problem Solving", "Communication", "Leadership", "Critical Thinking"],
        "companies": ["Google", "Microsoft", "Netflix", "Uber", "Airbnb", "Spotify"],
        "learningPath": "Advanced Data Science and ML Leadership (6-8 months)",
        "relevanceScore": 88,
        "confidenceLevel": 85,
        "matchReasons": ["Strong analytical skills match", "Experience level alignment", "Technical background fits"],
        "minExperienceYears": 8,
        "maxExperienceYears": 18,
        "minSalary": 160000,
        "maxSalary": 240000
    },
    {
        "title": "Engineering Manager",
        "careerType": "engineering-manager",
        "description": "Lead engineering teams, manage software development processes, drive technical and people management.",
        "salaryRange": "$150,000 - $220,000",
        "experienceLevel": "senior",
        "requiredTechnicalSkills": ["Software Engineering", "Team Management", "Agile/Scrum", "System Architecture"],
        "requiredSoftSkills": ["Leadership", "Communication", "Team Building", "Strategic Thinking"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Stripe"],
        "learningPath": "Engineering Management Program (4-6 months)",
        "relevanceScore": 82,
        "confidenceLevel": 80,
        "matchReasons": ["Leadership potential", "Technical background", "Team collaboration skills"],
        "minExperienceYears": 8,
        "maxExperienceYears": 15,
        "minSalary": 150000,
        "maxSalary": 220000
    },
    {
        "title": "Senior Product Manager",
        "careerType": "senior-product-manager",
        "description": "Own product strategy and roadmap, lead cross-functional teams, drive product success through data-driven decisions.",
        "salaryRange": "$140,000 - $200,000",
        "experienceLevel": "senior",
        "requiredTechnicalSkills": ["Product Management", "Data Analysis", "User Research", "Strategic Planning"],
        "requiredSoftSkills": ["Communication", "Strategic Thinking", "Problem Solving", "Leadership"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Airbnb"],
        "learningPath": "Senior Product Management Certification (4-6 months)",
        "relevanceScore": 80,
        "confidenceLevel": 78,
        "matchReasons": ["Strategic thinking alignment", "Communication skills", "Business acumen"],
        "minExperienceYears": 7,
        "maxExperienceYears": 15,
        "minSalary": 140000,
        "maxSalary": 200000
    },
    {
        "title": "Solutions Architect",
        "careerType": "solutions-architect",
        "description": "Design and implement complex technical solutions, work with enterprise clients, lead technical pre-sales.",
        "salaryRange": "$150,000 - $210,000",
        "experienceLevel": "senior",
        "requiredTechnicalSkills": ["System Architecture", "Cloud Platforms", "Enterprise Solutions", "Technical Consulting"],
        "requiredSoftSkills": ["Communication", "Problem Solving", "Client Management", "Presentation Skills"],
        "companies": ["AWS", "Microsoft", "Google Cloud", "IBM", "Oracle", "Salesforce"],
        "learningPath": "Solutions Architecture Certification (4-6 months)",
        "relevanceScore": 78,
        "confidenceLevel": 75,
        "matchReasons": ["Architecture experience", "Technical consulting skills"],
        "minExperienceYears": 8,
        "maxExperienceYears": 18,
        "minSalary": 150000,
        "maxSalary": 210000
    },

    # MID LEVEL (5-12 years, $100k-180k)
    {
        "title": "Staff Software Engineer",
        "careerType": "staff-engineer",
        "description": "Lead technical projects, mentor other engineers, contribute to architectural decisions, drive technical excellence.",
        "salaryRange": "$140,000 - $190,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Advanced Programming", "System Design", "Technical Leadership", "Code Review"],
        "requiredSoftSkills": ["Mentoring", "Communication", "Problem Solving", "Technical Writing"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Stripe"],
        "learningPath": "Staff Engineer Development (4-6 months)",
        "relevanceScore": 82,
        "confidenceLevel": 80,
        "matchReasons": ["Strong technical skills", "Leadership potential"],
        "minExperienceYears": 6,
        "maxExperienceYears": 12,
        "minSalary": 140000,
        "maxSalary": 190000
    },
    {
        "title": "Data Scientist",
        "careerType": "data-scientist",
        "description": "Build machine learning models, analyze complex datasets, provide data-driven insights for business decisions.",
        "salaryRange": "$120,000 - $170,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Python", "Machine Learning", "SQL", "Statistics", "Data Visualization"],
        "requiredSoftSkills": ["Analytical Thinking", "Communication", "Problem Solving", "Business Acumen"],
        "companies": ["Google", "Microsoft", "Netflix", "Uber", "Airbnb", "Spotify"],
        "learningPath": "Data Science Specialization (4-6 months)",
        "relevanceScore": 85,
        "confidenceLevel": 82,
        "matchReasons": ["Data analysis skills", "Technical background", "Analytical mindset"],
        "minExperienceYears": 4,
        "maxExperienceYears": 10,
        "minSalary": 120000,
        "maxSalary": 170000
    },
    {
        "title": "Product Manager",
        "careerType": "product-manager",
        "description": "Own product roadmap and strategy, work with engineering teams, drive product success through data-driven decisions.",
        "salaryRange": "$110,000 - $160,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Product Management", "Data Analysis", "User Research", "Agile/Scrum"],
        "requiredSoftSkills": ["Communication", "Strategic Thinking", "Problem Solving", "Leadership"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Airbnb"],
        "learningPath": "Product Management Certification (3-4 months)",
        "relevanceScore": 78,
        "confidenceLevel": 75,
        "matchReasons": ["Strategic thinking alignment", "Communication skills", "Business acumen"],
        "minExperienceYears": 4,
        "maxExperienceYears": 10,
        "minSalary": 110000,
        "maxSalary": 160000
    },
    {
        "title": "DevOps Engineer",
        "careerType": "devops-engineer",
        "description": "Manage infrastructure and deployment pipelines, implement CI/CD processes, ensure system reliability.",
        "salaryRange": "$115,000 - $165,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["AWS", "Docker", "Kubernetes", "CI/CD", "Linux", "Infrastructure as Code"],
        "requiredSoftSkills": ["Problem Solving", "Communication", "Attention to Detail", "Collaboration"],
        "companies": ["AWS", "Google Cloud", "Microsoft", "Netflix", "Uber", "Stripe"],
        "learningPath": "DevOps Engineering Certification (4-6 months)",
        "relevanceScore": 75,
        "confidenceLevel": 72,
        "matchReasons": ["Infrastructure experience", "Systematic thinking"],
        "minExperienceYears": 4,
        "maxExperienceYears": 10,
        "minSalary": 115000,
        "maxSalary": 165000
    },

    # JUNIOR/ENTRY LEVEL (0-5 years, $60k-120k)
    {
        "title": "Software Engineer",
        "careerType": "software-engineer",
        "description": "Develop software applications, write clean code, participate in code reviews, learn from senior engineers.",
        "salaryRange": "$90,000 - $130,000",
        "experienceLevel": "junior",
        "requiredTechnicalSkills": ["Programming", "Software Development", "Version Control", "Testing"],
        "requiredSoftSkills": ["Learning Agility", "Communication", "Problem Solving", "Teamwork"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Stripe"],
        "learningPath": "Software Engineering Fundamentals (3-6 months)",
        "relevanceScore": 70,
        "confidenceLevel": 75,
        "matchReasons": ["Programming aptitude", "Problem-solving skills"],
        "minExperienceYears": 0,
        "maxExperienceYears": 5,
        "minSalary": 90000,
        "maxSalary": 130000
    },
    {
        "title": "Data Analyst",
        "careerType": "data-analyst",
        "description": "Analyze data to provide business insights, create reports and dashboards, support data-driven decision making.",
        "salaryRange": "$70,000 - $100,000",
        "experienceLevel": "junior",
        "requiredTechnicalSkills": ["SQL", "Excel", "Data Visualization", "Statistics", "Python/R"],
        "requiredSoftSkills": ["Analytical Thinking", "Communication", "Attention to Detail", "Business Acumen"],
        "companies": ["Deloitte", "Accenture", "IBM", "Microsoft", "Oracle", "Tableau"],
        "learningPath": "Data Analysis Certification (2-4 months)",
        "relevanceScore": 75,
        "confidenceLevel": 78,
        "matchReasons": ["Analytical skills", "Data-focused mindset"],
        "minExperienceYears": 0,
        "maxExperienceYears": 4,
        "minSalary": 70000,
        "maxSalary": 100000
    },
    {
        "title": "Business Intelligence Analyst",
        "careerType": "business-intelligence-analyst",
        "description": "Transform data into actionable business insights, create dashboards and reports, support strategic decision making.",
        "salaryRange": "$75,000 - $110,000",
        "experienceLevel": "junior",
        "requiredTechnicalSkills": ["SQL", "Business Intelligence", "Data Visualization", "Excel", "Tableau/Power BI"],
        "requiredSoftSkills": ["Analytical Thinking", "Communication", "Problem Solving", "Attention to Detail"],
        "companies": ["Deloitte", "Accenture", "IBM", "Microsoft", "Oracle", "Salesforce"],
        "learningPath": "Business Intelligence Certification (2-3 months)",
        "relevanceScore": 72,
        "confidenceLevel": 75,
        "matchReasons": ["Data analysis skills", "Business focus", "Analytical mindset"],
        "minExperienceYears": 1,
        "maxExperienceYears": 5,
        "minSalary": 75000,
        "maxSalary": 110000
    },
    {
        "title": "Junior Product Manager",
        "careerType": "junior-product-manager",
        "description": "Support product development, conduct user research, assist with product roadmap planning, learn product management.",
        "salaryRange": "$80,000 - $120,000",
        "experienceLevel": "junior",
        "requiredTechnicalSkills": ["Product Management Basics", "User Research", "Data Analysis", "Project Management"],
        "requiredSoftSkills": ["Communication", "Learning Agility", "Problem Solving", "Collaboration"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Airbnb", "Stripe"],
        "learningPath": "Product Management Fundamentals (3-4 months)",
        "relevanceScore": 68,
        "confidenceLevel": 70,
        "matchReasons": ["Business thinking", "Communication skills"],
        "minExperienceYears": 0,
        "maxExperienceYears": 3,
        "minSalary": 80000,
        "maxSalary": 120000
    },
    
    # ADDITIONAL EXECUTIVE LEVEL CAREERS
    {
        "title": "Chief Product Officer",
        "careerType": "cpo",
        "description": "Lead product strategy across the organization, oversee product teams, drive product innovation and market success.",
        "salaryRange": "$240,000 - $380,000",
        "experienceLevel": "executive",
        "requiredTechnicalSkills": ["Product Strategy", "Market Analysis", "Product Management", "Data-Driven Decision Making"],
        "requiredSoftSkills": ["Executive Leadership", "Strategic Vision", "Communication", "Innovation"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Airbnb", "Uber"],
        "learningPath": "Chief Product Officer Program (6-12 months)",
        "relevanceScore": 75,
        "confidenceLevel": 80,
        "matchReasons": ["Product leadership experience", "Strategic thinking"],
        "minExperienceYears": 15,
        "maxExperienceYears": 30,
        "minSalary": 240000,
        "maxSalary": 380000
    },
    {
        "title": "VP of Product",
        "careerType": "vp-product",
        "description": "Lead product organization, define product vision and strategy, manage product teams across multiple product lines.",
        "salaryRange": "$200,000 - $320,000",
        "experienceLevel": "executive",
        "requiredTechnicalSkills": ["Product Strategy", "Product Management", "Market Research", "Product Analytics"],
        "requiredSoftSkills": ["Executive Leadership", "Strategic Thinking", "Communication", "Team Building"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Stripe"],
        "learningPath": "VP Product Leadership Program (6-12 months)",
        "relevanceScore": 90,
        "confidenceLevel": 85,
        "matchReasons": ["Product management expertise", "Leadership experience", "Strategic vision"],
        "minExperienceYears": 12,
        "maxExperienceYears": 25,
        "minSalary": 200000,
        "maxSalary": 320000
    },
    {
        "title": "Head of Product",
        "careerType": "head-of-product",
        "description": "Lead product strategy and execution, manage product teams, drive product-market fit and growth.",
        "salaryRange": "$180,000 - $280,000",
        "experienceLevel": "executive",
        "requiredTechnicalSkills": ["Product Management", "Product Strategy", "User Research", "Product Analytics"],
        "requiredSoftSkills": ["Leadership", "Strategic Thinking", "Communication", "Cross-functional Collaboration"],
        "companies": ["Airbnb", "Uber", "Stripe", "Slack", "Zoom", "Dropbox"],
        "learningPath": "Head of Product Program (4-8 months)",
        "relevanceScore": 88,
        "confidenceLevel": 82,
        "matchReasons": ["Product leadership experience", "Strategic product thinking"],
        "minExperienceYears": 10,
        "maxExperienceYears": 20,
        "minSalary": 180000,
        "maxSalary": 280000
    },
    {
        "title": "Chief Information Officer",
        "careerType": "cio",
        "description": "Lead IT strategy and operations, manage technology infrastructure, drive digital transformation initiatives.",
        "salaryRange": "$220,000 - $360,000",
        "experienceLevel": "executive",
        "requiredTechnicalSkills": ["IT Strategy", "Enterprise Architecture", "Digital Transformation", "Cybersecurity"],
        "requiredSoftSkills": ["Executive Leadership", "Strategic Planning", "Change Management", "Communication"],
        "companies": ["IBM", "Microsoft", "Oracle", "Accenture", "Deloitte", "PwC"],
        "learningPath": "CIO Leadership Program (6-12 months)",
        "relevanceScore": 75,
        "confidenceLevel": 80,
        "matchReasons": ["IT leadership experience", "Strategic technology background"],
        "minExperienceYears": 15,
        "maxExperienceYears": 30,
        "minSalary": 220000,
        "maxSalary": 360000
    },
    
    # ADDITIONAL SENIOR LEVEL CAREERS
    {
        "title": "Director of Product Management",
        "careerType": "director-product-management",
        "description": "Lead multiple product teams, define product strategy, drive cross-functional collaboration and product success.",
        "salaryRange": "$160,000 - $240,000",
        "experienceLevel": "senior",
        "requiredTechnicalSkills": ["Product Management", "Product Strategy", "Team Leadership", "Product Analytics"],
        "requiredSoftSkills": ["Leadership", "Strategic Thinking", "Communication", "Cross-functional Collaboration"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Airbnb"],
        "learningPath": "Director Product Management Program (4-6 months)",
        "relevanceScore": 92,
        "confidenceLevel": 88,
        "matchReasons": ["Product management leadership", "Strategic product experience"],
        "minExperienceYears": 10,
        "maxExperienceYears": 18,
        "minSalary": 160000,
        "maxSalary": 240000
    },
    {
        "title": "Principal Product Manager",
        "careerType": "principal-product-manager",
        "description": "Lead complex product initiatives, drive product strategy, mentor product teams, work on high-impact products.",
        "salaryRange": "$150,000 - $220,000",
        "experienceLevel": "senior",
        "requiredTechnicalSkills": ["Product Management", "Product Strategy", "User Research", "Data Analysis"],
        "requiredSoftSkills": ["Strategic Thinking", "Leadership", "Communication", "Problem Solving"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Stripe"],
        "learningPath": "Principal Product Manager Track (4-6 months)",
        "relevanceScore": 90,
        "confidenceLevel": 85,
        "matchReasons": ["Senior product management experience", "Strategic product leadership"],
        "minExperienceYears": 8,
        "maxExperienceYears": 16,
        "minSalary": 150000,
        "maxSalary": 220000
    },
    {
        "title": "Senior Software Architect",
        "careerType": "senior-software-architect",
        "description": "Design enterprise software architecture, lead technical decisions, mentor engineering teams on best practices.",
        "salaryRange": "$170,000 - $260,000",
        "experienceLevel": "senior",
        "requiredTechnicalSkills": ["Software Architecture", "System Design", "Cloud Platforms", "Microservices"],
        "requiredSoftSkills": ["Technical Leadership", "Communication", "Mentoring", "Problem Solving"],
        "companies": ["Google", "Microsoft", "Amazon", "Netflix", "Uber", "Airbnb"],
        "learningPath": "Software Architecture Mastery (6-8 months)",
        "relevanceScore": 85,
        "confidenceLevel": 82,
        "matchReasons": ["Architecture experience", "Technical leadership skills"],
        "minExperienceYears": 10,
        "maxExperienceYears": 20,
        "minSalary": 170000,
        "maxSalary": 260000
    },
    {
        "title": "Data Science Manager",
        "careerType": "data-science-manager",
        "description": "Lead data science teams, drive ML initiatives, translate business problems into data solutions.",
        "salaryRange": "$155,000 - $230,000",
        "experienceLevel": "senior",
        "requiredTechnicalSkills": ["Machine Learning", "Data Science", "Team Management", "Statistical Analysis"],
        "requiredSoftSkills": ["Leadership", "Communication", "Strategic Thinking", "Problem Solving"],
        "companies": ["Google", "Microsoft", "Netflix", "Uber", "Airbnb", "Spotify"],
        "learningPath": "Data Science Leadership (4-6 months)",
        "relevanceScore": 88,
        "confidenceLevel": 85,
        "matchReasons": ["Data science expertise", "Leadership potential"],
        "minExperienceYears": 8,
        "maxExperienceYears": 15,
        "minSalary": 155000,
        "maxSalary": 230000
    },
    {
        "title": "Senior UX Designer",
        "careerType": "senior-ux-designer",
        "description": "Lead user experience design, conduct user research, create design systems, mentor junior designers.",
        "salaryRange": "$130,000 - $190,000",
        "experienceLevel": "senior",
        "requiredTechnicalSkills": ["UX Design", "User Research", "Design Systems", "Prototyping"],
        "requiredSoftSkills": ["Creativity", "Empathy", "Communication", "Problem Solving"],
        "companies": ["Google", "Apple", "Microsoft", "Adobe", "Figma", "Airbnb"],
        "learningPath": "Senior UX Design Certification (4-6 months)",
        "relevanceScore": 78,
        "confidenceLevel": 75,
        "matchReasons": ["Design thinking", "User-centered approach"],
        "minExperienceYears": 8,
        "maxExperienceYears": 15,
        "minSalary": 130000,
        "maxSalary": 190000
    },
    {
        "title": "Technical Program Manager",
        "careerType": "technical-program-manager",
        "description": "Manage complex technical programs, coordinate cross-functional teams, drive technical project delivery.",
        "salaryRange": "$145,000 - $210,000",
        "experienceLevel": "senior",
        "requiredTechnicalSkills": ["Program Management", "Technical Understanding", "Project Planning", "Risk Management"],
        "requiredSoftSkills": ["Leadership", "Communication", "Organization", "Problem Solving"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix"],
        "learningPath": "Technical Program Management (4-6 months)",
        "relevanceScore": 80,
        "confidenceLevel": 78,
        "matchReasons": ["Program management skills", "Technical background"],
        "minExperienceYears": 8,
        "maxExperienceYears": 15,
        "minSalary": 145000,
        "maxSalary": 210000
    },
    {
        "title": "Group Product Manager",
        "careerType": "group-product-manager",
        "description": "Lead multiple product managers, drive product strategy across product portfolio, manage complex product initiatives.",
        "salaryRange": "$140,000 - $200,000",
        "experienceLevel": "senior",
        "requiredTechnicalSkills": ["Product Management", "Product Strategy", "Team Leadership", "Portfolio Management"],
        "requiredSoftSkills": ["Leadership", "Strategic Thinking", "Communication", "Mentoring"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Uber"],
        "learningPath": "Group Product Manager Program (4-6 months)",
        "relevanceScore": 88,
        "confidenceLevel": 82,
        "matchReasons": ["Product management leadership", "Team management experience"],
        "minExperienceYears": 8,
        "maxExperienceYears": 15,
        "minSalary": 140000,
        "maxSalary": 200000
    },
    
    # ADDITIONAL MID LEVEL CAREERS
    {
        "title": "Machine Learning Engineer",
        "careerType": "ml-engineer",
        "description": "Build and deploy ML models, optimize model performance, work with data science teams on production systems.",
        "salaryRange": "$125,000 - $180,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Machine Learning", "Python", "MLOps", "Cloud Platforms", "Deep Learning"],
        "requiredSoftSkills": ["Problem Solving", "Collaboration", "Learning Agility", "Communication"],
        "companies": ["Google", "Microsoft", "Netflix", "Uber", "Airbnb", "OpenAI"],
        "learningPath": "ML Engineering Specialization (4-6 months)",
        "relevanceScore": 85,
        "confidenceLevel": 82,
        "matchReasons": ["ML expertise", "Engineering skills"],
        "minExperienceYears": 4,
        "maxExperienceYears": 10,
        "minSalary": 125000,
        "maxSalary": 180000
    },
    {
        "title": "Cloud Solutions Engineer",
        "careerType": "cloud-solutions-engineer",
        "description": "Design and implement cloud infrastructure, optimize cloud costs, ensure security and scalability.",
        "salaryRange": "$110,000 - $160,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["AWS/Azure/GCP", "Infrastructure as Code", "Containerization", "Monitoring"],
        "requiredSoftSkills": ["Problem Solving", "Communication", "Attention to Detail", "Collaboration"],
        "companies": ["AWS", "Microsoft", "Google Cloud", "IBM", "Oracle", "Salesforce"],
        "learningPath": "Cloud Engineering Certification (4-6 months)",
        "relevanceScore": 78,
        "confidenceLevel": 75,
        "matchReasons": ["Cloud expertise", "Infrastructure skills"],
        "minExperienceYears": 4,
        "maxExperienceYears": 10,
        "minSalary": 110000,
        "maxSalary": 160000
    },
    {
        "title": "Cybersecurity Analyst",
        "careerType": "cybersecurity-analyst",
        "description": "Monitor security threats, implement security measures, conduct security assessments and incident response.",
        "salaryRange": "$105,000 - $155,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Cybersecurity", "Network Security", "Incident Response", "Risk Assessment"],
        "requiredSoftSkills": ["Attention to Detail", "Problem Solving", "Communication", "Critical Thinking"],
        "companies": ["IBM", "Microsoft", "Cisco", "Palo Alto Networks", "CrowdStrike", "FireEye"],
        "learningPath": "Cybersecurity Specialization (4-6 months)",
        "relevanceScore": 75,
        "confidenceLevel": 72,
        "matchReasons": ["Security mindset", "Analytical skills"],
        "minExperienceYears": 4,
        "maxExperienceYears": 10,
        "minSalary": 105000,
        "maxSalary": 155000
    },
    {
        "title": "Full Stack Developer",
        "careerType": "full-stack-developer",
        "description": "Develop both frontend and backend applications, work with databases, create end-to-end solutions.",
        "salaryRange": "$100,000 - $150,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["JavaScript", "React/Angular", "Node.js", "Databases", "APIs"],
        "requiredSoftSkills": ["Problem Solving", "Learning Agility", "Communication", "Teamwork"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Stripe"],
        "learningPath": "Full Stack Development (4-6 months)",
        "relevanceScore": 80,
        "confidenceLevel": 78,
        "matchReasons": ["Programming skills", "Versatility"],
        "minExperienceYears": 3,
        "maxExperienceYears": 8,
        "minSalary": 100000,
        "maxSalary": 150000
    },
    {
        "title": "UX/UI Designer",
        "careerType": "ux-ui-designer",
        "description": "Design user interfaces and experiences, create wireframes and prototypes, conduct user testing.",
        "salaryRange": "$95,000 - $140,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["UI/UX Design", "Figma/Sketch", "Prototyping", "User Research"],
        "requiredSoftSkills": ["Creativity", "Empathy", "Communication", "Problem Solving"],
        "companies": ["Google", "Apple", "Microsoft", "Adobe", "Figma", "Airbnb"],
        "learningPath": "UX/UI Design Certification (3-4 months)",
        "relevanceScore": 75,
        "confidenceLevel": 72,
        "matchReasons": ["Design thinking", "User focus"],
        "minExperienceYears": 3,
        "maxExperienceYears": 8,
        "minSalary": 95000,
        "maxSalary": 140000
    },
    
    # ADDITIONAL JUNIOR LEVEL CAREERS
    {
        "title": "Frontend Developer",
        "careerType": "frontend-developer",
        "description": "Build user interfaces, implement responsive designs, work with modern JavaScript frameworks.",
        "salaryRange": "$75,000 - $110,000",
        "experienceLevel": "junior",
        "requiredTechnicalSkills": ["HTML/CSS", "JavaScript", "React/Vue", "Responsive Design"],
        "requiredSoftSkills": ["Learning Agility", "Attention to Detail", "Communication", "Problem Solving"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Stripe"],
        "learningPath": "Frontend Development Bootcamp (3-4 months)",
        "relevanceScore": 72,
        "confidenceLevel": 75,
        "matchReasons": ["Web development interest", "Visual thinking"],
        "minExperienceYears": 0,
        "maxExperienceYears": 4,
        "minSalary": 75000,
        "maxSalary": 110000
    },
    {
        "title": "Backend Developer",
        "careerType": "backend-developer",
        "description": "Build server-side applications, design APIs, work with databases and cloud services.",
        "salaryRange": "$80,000 - $115,000",
        "experienceLevel": "junior",
        "requiredTechnicalSkills": ["Python/Java/Node.js", "Databases", "APIs", "Cloud Services"],
        "requiredSoftSkills": ["Problem Solving", "Logical Thinking", "Communication", "Learning Agility"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Stripe"],
        "learningPath": "Backend Development Program (3-4 months)",
        "relevanceScore": 75,
        "confidenceLevel": 78,
        "matchReasons": ["Programming aptitude", "Systems thinking"],
        "minExperienceYears": 0,
        "maxExperienceYears": 4,
        "minSalary": 80000,
        "maxSalary": 115000
    },
    {
        "title": "Quality Assurance Engineer",
        "careerType": "qa-engineer",
        "description": "Test software applications, create test plans, ensure product quality and reliability.",
        "salaryRange": "$65,000 - $95,000",
        "experienceLevel": "junior",
        "requiredTechnicalSkills": ["Testing", "Test Automation", "Bug Tracking", "Quality Processes"],
        "requiredSoftSkills": ["Attention to Detail", "Communication", "Problem Solving", "Patience"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Adobe"],
        "learningPath": "QA Engineering Certification (2-3 months)",
        "relevanceScore": 70,
        "confidenceLevel": 72,
        "matchReasons": ["Detail-oriented", "Quality focus"],
        "minExperienceYears": 0,
        "maxExperienceYears": 4,
        "minSalary": 65000,
        "maxSalary": 95000
    },
    {
        "title": "Digital Marketing Specialist",
        "careerType": "digital-marketing-specialist",
        "description": "Manage digital marketing campaigns, analyze marketing data, optimize online presence and engagement.",
        "salaryRange": "$55,000 - $85,000",
        "experienceLevel": "junior",
        "requiredTechnicalSkills": ["Digital Marketing", "Google Analytics", "Social Media", "SEO/SEM"],
        "requiredSoftSkills": ["Creativity", "Communication", "Analytical Thinking", "Adaptability"],
        "companies": ["Google", "Meta", "HubSpot", "Salesforce", "Adobe", "Mailchimp"],
        "learningPath": "Digital Marketing Certification (2-3 months)",
        "relevanceScore": 68,
        "confidenceLevel": 70,
        "matchReasons": ["Marketing interest", "Data-driven approach"],
        "minExperienceYears": 0,
        "maxExperienceYears": 3,
        "minSalary": 55000,
        "maxSalary": 85000
    },
    {
        "title": "Technical Writer",
        "careerType": "technical-writer",
        "description": "Create technical documentation, user guides, API documentation, and developer resources.",
        "salaryRange": "$60,000 - $90,000",
        "experienceLevel": "junior",
        "requiredTechnicalSkills": ["Technical Writing", "Documentation Tools", "Basic Programming", "Content Management"],
        "requiredSoftSkills": ["Writing Skills", "Communication", "Attention to Detail", "Learning Agility"],
        "companies": ["Google", "Microsoft", "Amazon", "Atlassian", "GitLab", "MongoDB"],
        "learningPath": "Technical Writing Certification (2-3 months)",
        "relevanceScore": 65,
        "confidenceLevel": 68,
        "matchReasons": ["Writing skills", "Technical interest"],
        "minExperienceYears": 0,
        "maxExperienceYears": 3,
        "minSalary": 60000,
        "maxSalary": 90000
    },
    {
        "title": "Sales Development Representative",
        "careerType": "sdr",
        "description": "Generate leads, qualify prospects, support sales team with pipeline development and customer outreach.",
        "salaryRange": "$50,000 - $80,000",
        "experienceLevel": "junior",
        "requiredTechnicalSkills": ["CRM Software", "Sales Tools", "Lead Generation", "Data Analysis"],
        "requiredSoftSkills": ["Communication", "Persistence", "Relationship Building", "Goal-Oriented"],
        "companies": ["Salesforce", "HubSpot", "Zoom", "Slack", "Stripe", "Atlassian"],
        "learningPath": "Sales Development Program (1-2 months)",
        "relevanceScore": 60,
        "confidenceLevel": 65,
        "matchReasons": ["People skills", "Goal-driven"],
        "minExperienceYears": 0,
        "maxExperienceYears": 2,
        "minSalary": 50000,
        "maxSalary": 80000
    },
    
    # SOFTWARE ENGINEERING SPECIALIZATIONS
    {
        "title": "Embedded Systems Engineer",
        "careerType": "embedded-systems-engineer",
        "description": "Design and develop embedded software for hardware devices, IoT systems, and real-time applications.",
        "salaryRange": "$105,000 - $155,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["C/C++", "Embedded Systems", "Real-time OS", "Hardware Integration", "Microcontrollers"],
        "requiredSoftSkills": ["Problem Solving", "Attention to Detail", "Systems Thinking", "Communication"],
        "companies": ["Intel", "Qualcomm", "Texas Instruments", "ARM", "NVIDIA", "Bosch"],
        "learningPath": "Embedded Systems Development (4-6 months)",
        "relevanceScore": 80,
        "confidenceLevel": 78,
        "matchReasons": ["Hardware-software integration", "Systems programming"],
        "minExperienceYears": 3,
        "maxExperienceYears": 10,
        "minSalary": 105000,
        "maxSalary": 155000
    },
    {
        "title": "Mobile App Developer",
        "careerType": "mobile-app-developer",
        "description": "Develop native and cross-platform mobile applications for iOS and Android platforms.",
        "salaryRange": "$95,000 - $145,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Swift/Kotlin", "React Native/Flutter", "Mobile UI/UX", "App Store Deployment", "Mobile Testing"],
        "requiredSoftSkills": ["Creativity", "User Focus", "Problem Solving", "Learning Agility"],
        "companies": ["Apple", "Google", "Meta", "Uber", "Airbnb", "Spotify"],
        "learningPath": "Mobile Development Bootcamp (3-5 months)",
        "relevanceScore": 82,
        "confidenceLevel": 80,
        "matchReasons": ["Mobile development interest", "User-focused thinking"],
        "minExperienceYears": 2,
        "maxExperienceYears": 8,
        "minSalary": 95000,
        "maxSalary": 145000
    },
    {
        "title": "Game Developer",
        "careerType": "game-developer",
        "description": "Create video games and interactive entertainment software using game engines and programming languages.",
        "salaryRange": "$85,000 - $130,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Unity/Unreal Engine", "C#/C++", "Game Physics", "3D Graphics", "Game Design"],
        "requiredSoftSkills": ["Creativity", "Problem Solving", "Teamwork", "Passion for Gaming"],
        "companies": ["Epic Games", "Unity", "Blizzard", "EA", "Ubisoft", "Riot Games"],
        "learningPath": "Game Development Program (4-6 months)",
        "relevanceScore": 75,
        "confidenceLevel": 72,
        "matchReasons": ["Creative programming", "Interactive systems"],
        "minExperienceYears": 2,
        "maxExperienceYears": 8,
        "minSalary": 85000,
        "maxSalary": 130000
    },
    {
        "title": "Blockchain Developer",
        "careerType": "blockchain-developer",
        "description": "Develop decentralized applications, smart contracts, and blockchain-based solutions.",
        "salaryRange": "$120,000 - $180,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Solidity", "Web3", "Smart Contracts", "Ethereum", "Cryptocurrency"],
        "requiredSoftSkills": ["Innovation", "Problem Solving", "Security Mindset", "Learning Agility"],
        "companies": ["Coinbase", "ConsenSys", "Chainlink", "Polygon", "Binance", "OpenSea"],
        "learningPath": "Blockchain Development Certification (4-6 months)",
        "relevanceScore": 78,
        "confidenceLevel": 75,
        "matchReasons": ["Emerging technology interest", "Decentralized systems"],
        "minExperienceYears": 3,
        "maxExperienceYears": 10,
        "minSalary": 120000,
        "maxSalary": 180000
    },
    
    # CIVIL ENGINEERING CAREERS
    {
        "title": "Structural Engineer",
        "careerType": "structural-engineer",
        "description": "Design and analyze building structures, bridges, and infrastructure to ensure safety and stability.",
        "salaryRange": "$85,000 - $130,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Structural Analysis", "AutoCAD", "SAP2000", "Building Codes", "Materials Science"],
        "requiredSoftSkills": ["Attention to Detail", "Problem Solving", "Communication", "Project Management"],
        "companies": ["AECOM", "Jacobs", "WSP", "Arup", "Skanska", "Turner Construction"],
        "learningPath": "Structural Engineering Certification (6-8 months)",
        "relevanceScore": 82,
        "confidenceLevel": 80,
        "matchReasons": ["Engineering mindset", "Mathematical skills"],
        "minExperienceYears": 4,
        "maxExperienceYears": 12,
        "minSalary": 85000,
        "maxSalary": 130000
    },
    {
        "title": "Transportation Engineer",
        "careerType": "transportation-engineer",
        "description": "Plan and design transportation systems including roads, highways, airports, and public transit.",
        "salaryRange": "$80,000 - $125,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Traffic Engineering", "Transportation Planning", "GIS", "AutoCAD", "Traffic Simulation"],
        "requiredSoftSkills": ["Systems Thinking", "Communication", "Project Management", "Problem Solving"],
        "companies": ["AECOM", "WSP", "Jacobs", "HDR", "Parsons", "Stantec"],
        "learningPath": "Transportation Engineering Program (6-8 months)",
        "relevanceScore": 78,
        "confidenceLevel": 75,
        "matchReasons": ["Infrastructure planning", "Systems optimization"],
        "minExperienceYears": 3,
        "maxExperienceYears": 10,
        "minSalary": 80000,
        "maxSalary": 125000
    },
    {
        "title": "Environmental Engineer",
        "careerType": "environmental-engineer",
        "description": "Develop solutions for environmental problems, design pollution control systems, and ensure regulatory compliance.",
        "salaryRange": "$75,000 - $115,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Environmental Regulations", "Water Treatment", "Air Quality", "Waste Management", "Environmental Modeling"],
        "requiredSoftSkills": ["Problem Solving", "Communication", "Attention to Detail", "Sustainability Focus"],
        "companies": ["AECOM", "Jacobs", "Tetra Tech", "CH2M Hill", "Golder Associates", "Arcadis"],
        "learningPath": "Environmental Engineering Certification (6-8 months)",
        "relevanceScore": 80,
        "confidenceLevel": 78,
        "matchReasons": ["Environmental consciousness", "Regulatory knowledge"],
        "minExperienceYears": 3,
        "maxExperienceYears": 10,
        "minSalary": 75000,
        "maxSalary": 115000
    },
    
    # MECHANICAL ENGINEERING CAREERS
    {
        "title": "Mechanical Design Engineer",
        "careerType": "mechanical-design-engineer",
        "description": "Design mechanical systems, components, and products using CAD software and engineering principles.",
        "salaryRange": "$85,000 - $130,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["SolidWorks/AutoCAD", "Mechanical Design", "FEA Analysis", "Manufacturing Processes", "Materials Science"],
        "requiredSoftSkills": ["Problem Solving", "Creativity", "Attention to Detail", "Communication"],
        "companies": ["Boeing", "General Electric", "Ford", "Tesla", "Caterpillar", "3M"],
        "learningPath": "Mechanical Design Engineering (6-8 months)",
        "relevanceScore": 85,
        "confidenceLevel": 82,
        "matchReasons": ["Design thinking", "Technical problem solving"],
        "minExperienceYears": 3,
        "maxExperienceYears": 10,
        "minSalary": 85000,
        "maxSalary": 130000
    },
    {
        "title": "HVAC Engineer",
        "careerType": "hvac-engineer",
        "description": "Design heating, ventilation, and air conditioning systems for buildings and industrial facilities.",
        "salaryRange": "$80,000 - $120,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["HVAC Design", "Energy Modeling", "Building Codes", "AutoCAD", "Thermodynamics"],
        "requiredSoftSkills": ["Problem Solving", "Attention to Detail", "Communication", "Project Management"],
        "companies": ["Johnson Controls", "Carrier", "Trane", "Honeywell", "AECOM", "WSP"],
        "learningPath": "HVAC Engineering Certification (4-6 months)",
        "relevanceScore": 78,
        "confidenceLevel": 75,
        "matchReasons": ["Systems engineering", "Energy efficiency focus"],
        "minExperienceYears": 3,
        "maxExperienceYears": 10,
        "minSalary": 80000,
        "maxSalary": 120000
    },
    {
        "title": "Manufacturing Engineer",
        "careerType": "manufacturing-engineer",
        "description": "Optimize manufacturing processes, improve production efficiency, and ensure quality control.",
        "salaryRange": "$85,000 - $125,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Lean Manufacturing", "Six Sigma", "Process Optimization", "Quality Control", "Automation"],
        "requiredSoftSkills": ["Problem Solving", "Continuous Improvement", "Communication", "Leadership"],
        "companies": ["Toyota", "General Motors", "Boeing", "Intel", "3M", "Caterpillar"],
        "learningPath": "Manufacturing Engineering Program (4-6 months)",
        "relevanceScore": 82,
        "confidenceLevel": 80,
        "matchReasons": ["Process optimization", "Efficiency focus"],
        "minExperienceYears": 3,
        "maxExperienceYears": 10,
        "minSalary": 85000,
        "maxSalary": 125000
    },
    
    # ELECTRICAL ENGINEERING CAREERS
    {
        "title": "Power Systems Engineer",
        "careerType": "power-systems-engineer",
        "description": "Design and maintain electrical power generation, transmission, and distribution systems.",
        "salaryRange": "$90,000 - $140,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Power Systems", "Electrical Grid", "SCADA", "Power Electronics", "Renewable Energy"],
        "requiredSoftSkills": ["Problem Solving", "Attention to Detail", "Communication", "Safety Focus"],
        "companies": ["General Electric", "Siemens", "ABB", "Schneider Electric", "Eaton", "Duke Energy"],
        "learningPath": "Power Systems Engineering (6-8 months)",
        "relevanceScore": 85,
        "confidenceLevel": 82,
        "matchReasons": ["Electrical systems expertise", "Infrastructure focus"],
        "minExperienceYears": 4,
        "maxExperienceYears": 12,
        "minSalary": 90000,
        "maxSalary": 140000
    },
    {
        "title": "Electronics Engineer",
        "careerType": "electronics-engineer",
        "description": "Design and develop electronic circuits, components, and systems for various applications.",
        "salaryRange": "$85,000 - $130,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Circuit Design", "PCB Layout", "Analog/Digital Electronics", "Signal Processing", "Embedded Systems"],
        "requiredSoftSkills": ["Problem Solving", "Attention to Detail", "Innovation", "Communication"],
        "companies": ["Intel", "Qualcomm", "Texas Instruments", "Analog Devices", "Broadcom", "NVIDIA"],
        "learningPath": "Electronics Engineering Certification (6-8 months)",
        "relevanceScore": 88,
        "confidenceLevel": 85,
        "matchReasons": ["Electronics expertise", "Circuit design skills"],
        "minExperienceYears": 3,
        "maxExperienceYears": 10,
        "minSalary": 85000,
        "maxSalary": 130000
    },
    {
        "title": "Control Systems Engineer",
        "careerType": "control-systems-engineer",
        "description": "Design and implement automated control systems for industrial processes and manufacturing.",
        "salaryRange": "$90,000 - $135,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["PLC Programming", "SCADA", "Control Theory", "Industrial Automation", "HMI Design"],
        "requiredSoftSkills": ["Problem Solving", "Systems Thinking", "Communication", "Attention to Detail"],
        "companies": ["Rockwell Automation", "Siemens", "Honeywell", "Emerson", "ABB", "Schneider Electric"],
        "learningPath": "Control Systems Engineering (6-8 months)",
        "relevanceScore": 82,
        "confidenceLevel": 80,
        "matchReasons": ["Automation expertise", "Control systems knowledge"],
        "minExperienceYears": 4,
        "maxExperienceYears": 12,
        "minSalary": 90000,
        "maxSalary": 135000
    },
    
    # OTHER ENGINEERING SPECIALIZATIONS
    {
        "title": "Chemical Engineer",
        "careerType": "chemical-engineer",
        "description": "Design chemical processes and equipment for manufacturing pharmaceuticals, chemicals, and materials.",
        "salaryRange": "$95,000 - $145,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Process Design", "Chemical Processes", "Process Safety", "Materials Science", "Process Simulation"],
        "requiredSoftSkills": ["Problem Solving", "Attention to Detail", "Safety Focus", "Communication"],
        "companies": ["Dow Chemical", "DuPont", "ExxonMobil", "BASF", "3M", "Johnson & Johnson"],
        "learningPath": "Chemical Engineering Program (6-8 months)",
        "relevanceScore": 85,
        "confidenceLevel": 82,
        "matchReasons": ["Process engineering", "Chemical knowledge"],
        "minExperienceYears": 4,
        "maxExperienceYears": 12,
        "minSalary": 95000,
        "maxSalary": 145000
    },
    {
        "title": "Aerospace Engineer",
        "careerType": "aerospace-engineer",
        "description": "Design and develop aircraft, spacecraft, satellites, and missiles for aerospace applications.",
        "salaryRange": "$100,000 - $150,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Aerodynamics", "Flight Mechanics", "CAD Design", "Materials Science", "Systems Engineering"],
        "requiredSoftSkills": ["Problem Solving", "Attention to Detail", "Innovation", "Communication"],
        "companies": ["Boeing", "Lockheed Martin", "SpaceX", "NASA", "Northrop Grumman", "Raytheon"],
        "learningPath": "Aerospace Engineering Certification (6-8 months)",
        "relevanceScore": 88,
        "confidenceLevel": 85,
        "matchReasons": ["Aerospace interest", "Advanced engineering"],
        "minExperienceYears": 4,
        "maxExperienceYears": 12,
        "minSalary": 100000,
        "maxSalary": 150000
    },
    {
        "title": "Biomedical Engineer",
        "careerType": "biomedical-engineer",
        "description": "Apply engineering principles to healthcare, designing medical devices and biological systems.",
        "salaryRange": "$85,000 - $130,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Medical Device Design", "Biomaterials", "Biomedical Instrumentation", "FDA Regulations", "CAD Design"],
        "requiredSoftSkills": ["Problem Solving", "Attention to Detail", "Communication", "Empathy"],
        "companies": ["Medtronic", "Johnson & Johnson", "Abbott", "Boston Scientific", "Stryker", "GE Healthcare"],
        "learningPath": "Biomedical Engineering Program (6-8 months)",
        "relevanceScore": 82,
        "confidenceLevel": 80,
        "matchReasons": ["Healthcare interest", "Engineering problem solving"],
        "minExperienceYears": 4,
        "maxExperienceYears": 12,
        "minSalary": 85000,
        "maxSalary": 130000
    },
    
    # EXPANDED PRODUCT MANAGEMENT ROLES
    {
        "title": "Technical Product Manager",
        "careerType": "technical-product-manager",
        "description": "Bridge technical and business teams, manage technical product roadmaps, work closely with engineering.",
        "salaryRange": "$120,000 - $170,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Technical Product Management", "API Design", "System Architecture", "Data Analysis", "Agile/Scrum"],
        "requiredSoftSkills": ["Technical Communication", "Strategic Thinking", "Problem Solving", "Leadership"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Stripe"],
        "learningPath": "Technical Product Management (4-6 months)",
        "relevanceScore": 90,
        "confidenceLevel": 88,
        "matchReasons": ["Technical background", "Product strategy skills"],
        "minExperienceYears": 5,
        "maxExperienceYears": 12,
        "minSalary": 120000,
        "maxSalary": 170000
    },
    {
        "title": "Growth Product Manager",
        "careerType": "growth-product-manager",
        "description": "Focus on user acquisition, retention, and product growth through data-driven experimentation.",
        "salaryRange": "$115,000 - $165,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Growth Hacking", "A/B Testing", "Analytics", "User Acquisition", "Conversion Optimization"],
        "requiredSoftSkills": ["Data-Driven Thinking", "Experimentation", "Communication", "Strategic Thinking"],
        "companies": ["Meta", "Uber", "Airbnb", "Spotify", "Pinterest", "TikTok"],
        "learningPath": "Growth Product Management (4-6 months)",
        "relevanceScore": 85,
        "confidenceLevel": 82,
        "matchReasons": ["Growth focus", "Data-driven approach"],
        "minExperienceYears": 4,
        "maxExperienceYears": 10,
        "minSalary": 115000,
        "maxSalary": 165000
    },
    {
        "title": "Platform Product Manager",
        "careerType": "platform-product-manager",
        "description": "Manage platform products that enable other products and developers, focus on APIs and developer experience.",
        "salaryRange": "$125,000 - $175,000",
        "experienceLevel": "mid",
        "requiredTechnicalSkills": ["Platform Strategy", "API Design", "Developer Experience", "Technical Architecture", "Ecosystem Management"],
        "requiredSoftSkills": ["Strategic Thinking", "Technical Communication", "Partnership Building", "Problem Solving"],
        "companies": ["Google", "Microsoft", "Amazon", "Stripe", "Twilio", "Salesforce"],
        "learningPath": "Platform Product Management (4-6 months)",
        "relevanceScore": 88,
        "confidenceLevel": 85,
        "matchReasons": ["Platform thinking", "Developer focus"],
        "minExperienceYears": 5,
        "maxExperienceYears": 12,
        "minSalary": 125000,
        "maxSalary": 175000
    }
]
COMPREHENSIVE_CAREERS.extend(HEALTHCARE_CAREERS)
COMPREHENSIVE_CAREERS.extend(SKILLED_TRADES_CAREERS)
COMPREHENSIVE_CAREERS.extend(EDUCATION_CAREERS)
COMPREHENSIVE_CAREERS.extend(BUSINESS_FINANCE_CAREERS)
COMPREHENSIVE_CAREERS.extend(LEGAL_LAW_CAREERS)
COMPREHENSIVE_CAREERS.extend(CREATIVE_ARTS_CAREERS)
COMPREHENSIVE_CAREERS.extend(PUBLIC_SERVICE_CAREERS)
COMPREHENSIVE_CAREERS.extend(HOSPITALITY_SERVICE_CAREERS)
COMPREHENSIVE_CAREERS.extend(MANUFACTURING_INDUSTRIAL_CAREERS)
COMPREHENSIVE_CAREERS.extend(AGRICULTURE_ENVIRONMENT_CAREERS)

def get_careers_by_experience_level(experience_years: int) -> list:
    """Filter careers by experience level with more inclusive ranges for better matching"""
    if experience_years >= 15:
        return [c for c in COMPREHENSIVE_CAREERS if c["experienceLevel"] in ["executive", "senior"]]
    elif experience_years >= 10:
        return [c for c in COMPREHENSIVE_CAREERS if c["experienceLevel"] in ["executive", "senior", "mid"]]
    elif experience_years >= 6:  # FIXED: 6+ years now includes senior roles
        return [c for c in COMPREHENSIVE_CAREERS if c["experienceLevel"] in ["senior", "mid"]]
    elif experience_years >= 3:
        return [c for c in COMPREHENSIVE_CAREERS if c["experienceLevel"] in ["mid", "junior"]]
    else:
        return [c for c in COMPREHENSIVE_CAREERS if c["experienceLevel"] == "junior"]

def get_careers_by_salary_range(min_salary: int, max_salary: int) -> list:
    """Filter careers by salary expectations"""
    return [c for c in COMPREHENSIVE_CAREERS 
            if c["maxSalary"] >= min_salary and c["minSalary"] <= max_salary]

def parse_experience_years(experience_str: str) -> int:
    """Parse experience string to years"""
    if not experience_str:
        return 0
    
    experience_lower = experience_str.lower()
    if "20+" in experience_lower or "20 or more" in experience_lower:
        return 20
    elif "15-20" in experience_lower:
        return 17
    elif "10-15" in experience_lower:
        return 12
    elif "5-10" in experience_lower:
        return 7
    elif "3-5" in experience_lower:
        return 4
    elif "1-3" in experience_lower:
        return 2
    elif "less than 1" in experience_lower or "0-1" in experience_lower:
        return 0
    else:
        return 5  # Default

def parse_salary_expectations(salary_str: str) -> tuple:
    """Parse salary string to min/max values with machine-friendly format support"""
    if not salary_str:
        return (50000, 200000)  # Default range
    
    print(f"🔍 Parsing salary: '{salary_str}'")
    
    # Handle machine-friendly format first (e.g., "70000-100000")
    if '-' in salary_str and salary_str.replace('-', '').replace('0', '').isdigit():
        try:
            parts = salary_str.split('-')
            if len(parts) == 2:
                min_val = int(parts[0])
                max_val = int(parts[1])
                print(f"✅ Machine format parsed: min={min_val}, max={max_val}")
                return (min_val, max_val)
        except ValueError:
            pass
    
    # Handle legacy user-friendly formats
    import re
    # Remove commas and extract all numbers
    clean_str = salary_str.replace(',', '')
    numbers = re.findall(r'\d+', clean_str)
    
    print(f"🔍 Legacy parsing: '{salary_str}' -> numbers: {numbers}")
    
    if len(numbers) >= 2:
        # Handle ranges like "150,000 - 250,000" or "150k - 250k"
        min_val = int(numbers[0])  # FIXED: Use index [0] instead of entire list
        max_val = int(numbers[1])  # FIXED: Use index [1] instead of entire list
        
        # Check if values are in thousands (like 150k = 150000)
        if 'k' in salary_str.lower():
            min_val *= 1000
            max_val *= 1000
        
        print(f"✅ Legacy format parsed: min={min_val}, max={max_val}")
        return (min_val, max_val)
    elif len(numbers) == 1:
        # Single number, create a range around it
        val = int(numbers[0])
        if 'k' in salary_str.lower():
            val *= 1000
        print(f"✅ Single value parsed: {val}, creating range")
        return (val - 10000, val + 10000)
    
    # Fallback for special cases
    salary_lower = salary_str.lower()
    if 'flexible' in salary_lower or 'open' in salary_lower:
        print("✅ Flexible salary detected")
        return (0, 999999)  # Very wide range for flexible
    
    print("⚠️ Could not parse salary, using default range")
    return (50000, 200000)  # Default range