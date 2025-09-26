import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { 
  ArrowLeft, 
  Search, 
  Star, 
  Building, 
  DollarSign, 
  TrendingUp, 
  BookOpen, 
  Users, 
  Calendar,
  Coffee,
  Briefcase,
  ExternalLink,
  CheckCircle,
  Clock,
  MapPin,
  Award,
  Lightbulb,
  Network,
  FileText,
  Download,
  Target,
  PlayCircle,
  BookmarkPlus,
  UserPlus,
  Linkedin,
  Mail,
  ChevronRight,
  Globe,
  Zap,
  TrendingDown,
  AlertCircle,
  Home,
  Copy,
  MessageSquare,
  Phone,
  Heart,
  HeartHandshake
} from "lucide-react";
import { showSuccess, showError } from "@/utils/toast";
import { generateCareerRecommendations, type CareerMatch, CAREER_TEMPLATES } from "@/utils/careerMatching";
import jsPDF from 'jspdf';
import { Logo } from "@/components/Logo";

interface User {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  assessmentData?: any;
  profileCompleted?: boolean;
  savedCareers?: string[]; // Track saved careers
}

// COMPREHENSIVE career progression data covering ALL supported job titles
const getCareerProgression = (careerTitle: string): Array<{
  role: string;
  years: string;
  salary: string;
  description: string;
}> => {
  const title = careerTitle.toLowerCase();
  
  // EXECUTIVE PRODUCT LEADERSHIP PROGRESSION
  if (title.includes('vp') && title.includes('product')) {
    return [
      {
        role: "Associate Product Manager",
        years: "0-2",
        salary: "$80K-$110K",
        description: "Support product development and user research"
      },
      {
        role: "Product Manager",
        years: "2-5",
        salary: "$110K-$150K",
        description: "Own product roadmap and work with engineering teams"
      },
      {
        role: "Senior Product Manager",
        years: "5-8",
        salary: "$150K-$200K",
        description: "Lead complex products and mentor junior PMs"
      },
      {
        role: "Principal Product Manager",
        years: "8-12",
        salary: "$200K-$250K",
        description: "Drive product strategy across multiple product lines"
      },
      {
        role: "Director of Product",
        years: "12-15",
        salary: "$250K-$300K",
        description: "Lead product organization and set product vision"
      },
      {
        role: "VP of Product Management",
        years: "15+",
        salary: "$300K-$400K",
        description: "Executive product leadership and strategy"
      }
    ];
  }
  
  // CHIEF PRODUCT OFFICER PROGRESSION
  if (title.includes('chief product officer') || title.includes('cpo')) {
    return [
      {
        role: "Product Manager",
        years: "0-3",
        salary: "$110K-$150K",
        description: "Own product roadmap and work with engineering teams"
      },
      {
        role: "Senior Product Manager",
        years: "3-6",
        salary: "$150K-$200K",
        description: "Lead complex products and mentor junior PMs"
      },
      {
        role: "Principal Product Manager",
        years: "6-10",
        salary: "$200K-$250K",
        description: "Drive product strategy across multiple product lines"
      },
      {
        role: "Director of Product",
        years: "10-13",
        salary: "$250K-$300K",
        description: "Lead product organization and set product vision"
      },
      {
        role: "VP of Product Management",
        years: "13-18",
        salary: "$300K-$400K",
        description: "Executive product leadership and strategy"
      },
      {
        role: "Chief Product Officer (CPO)",
        years: "18+",
        salary: "$400K-$600K",
        description: "C-suite product leadership and organizational strategy"
      }
    ];
  }
  
  // EXECUTIVE UX LEADERSHIP PROGRESSION
  if (title.includes('vp') && (title.includes('user experience') || title.includes('ux'))) {
    return [
      {
        role: "UX Designer",
        years: "0-3",
        salary: "$65K-$95K",
        description: "Create user interfaces and conduct user research"
      },
      {
        role: "Senior UX Designer",
        years: "3-6",
        salary: "$95K-$130K",
        description: "Lead design projects and mentor junior designers"
      },
      {
        role: "Principal UX Designer",
        years: "6-10",
        salary: "$130K-$170K",
        description: "Drive design strategy and cross-functional collaboration"
      },
      {
        role: "Design Manager",
        years: "8-12",
        salary: "$150K-$190K",
        description: "Manage design teams and set design standards"
      },
      {
        role: "Director of Design",
        years: "12-16",
        salary: "$190K-$240K",
        description: "Lead design organization and establish design culture"
      },
      {
        role: "VP of User Experience",
        years: "16+",
        salary: "$240K-$320K",
        description: "Executive UX leadership and design strategy"
      }
    ];
  }
  
  // CHIEF EXPERIENCE OFFICER PROGRESSION
  if (title.includes('chief experience officer') || title.includes('cxo')) {
    return [
      {
        role: "UX Designer",
        years: "0-3",
        salary: "$65K-$95K",
        description: "Create user interfaces and conduct user research"
      },
      {
        role: "Senior UX Designer",
        years: "3-6",
        salary: "$95K-$130K",
        description: "Lead design projects and mentor junior designers"
      },
      {
        role: "Design Manager",
        years: "6-10",
        salary: "$130K-$170K",
        description: "Manage design teams and set design standards"
      },
      {
        role: "Director of Design",
        years: "10-14",
        salary: "$170K-$220K",
        description: "Lead design organization and establish design culture"
      },
      {
        role: "VP of User Experience",
        years: "14-18",
        salary: "$220K-$280K",
        description: "Executive UX leadership and design strategy"
      },
      {
        role: "Chief Experience Officer (CXO)",
        years: "18+",
        salary: "$280K-$400K",
        description: "C-suite experience leadership and customer strategy"
      }
    ];
  }
  
  // STRATEGY CAREER PATH
  if (title.includes('strategy')) {
    return [
      {
        role: "Business Analyst",
        years: "0-2",
        salary: "$55K-$75K",
        description: "Analyze business processes and support strategic initiatives"
      },
      {
        role: "Strategy Analyst",
        years: "2-4",
        salary: "$70K-$95K",
        description: "Conduct market research and competitive analysis"
      },
      {
        role: "Strategy Manager",
        years: "4-7",
        salary: "$95K-$130K",
        description: "Lead strategic planning projects and cross-functional initiatives"
      },
      {
        role: "Senior Strategy Manager",
        years: "7-10",
        salary: "$130K-$170K",
        description: "Drive enterprise-wide strategic initiatives and mentor junior staff"
      },
      {
        role: "Director of Strategy",
        years: "10-15",
        salary: "$170K-$220K",
        description: "Lead strategic planning for business units and report to executives"
      },
      {
        role: "VP of Strategy & Operations",
        years: "15+",
        salary: "$220K-$300K",
        description: "Set organizational strategy and advise C-suite leadership"
      }
    ];
  }
  
  // OPERATIONS CAREER PATH
  if (title.includes('operations') || title.includes('coo')) {
    return [
      {
        role: "Operations Analyst",
        years: "0-2",
        salary: "$50K-$70K",
        description: "Support operational processes and data analysis"
      },
      {
        role: "Operations Manager",
        years: "2-5",
        salary: "$70K-$100K",
        description: "Manage day-to-day operations and process improvements"
      },
      {
        role: "Senior Operations Manager",
        years: "5-8",
        salary: "$100K-$140K",
        description: "Lead operational teams and drive efficiency initiatives"
      },
      {
        role: "Director of Operations",
        years: "8-12",
        salary: "$140K-$180K",
        description: "Oversee multiple operational areas and strategic planning"
      },
      {
        role: "VP of Operations",
        years: "12-18",
        salary: "$180K-$250K",
        description: "Lead enterprise operations and report to C-suite"
      },
      {
        role: "Chief Operating Officer (COO)",
        years: "18+",
        salary: "$250K-$400K",
        description: "Executive leadership of all operational functions"
      }
    ];
  }
  
  // BUSINESS DEVELOPMENT CAREER PATH
  if (title.includes('business development') || title.includes('bizdev')) {
    return [
      {
        role: "Business Development Associate",
        years: "0-2",
        salary: "$60K-$80K",
        description: "Support partnership development and market research"
      },
      {
        role: "Business Development Manager",
        years: "2-5",
        salary: "$80K-$120K",
        description: "Identify and develop strategic partnerships"
      },
      {
        role: "Senior Business Development Manager",
        years: "5-8",
        salary: "$120K-$160K",
        description: "Lead major partnership deals and mentor junior staff"
      },
      {
        role: "Director of Business Development",
        years: "8-12",
        salary: "$160K-$200K",
        description: "Set partnership strategy and manage BD team"
      },
      {
        role: "VP of Business Development",
        years: "12-18",
        salary: "$200K-$280K",
        description: "Lead enterprise partnerships and strategic alliances"
      },
      {
        role: "Chief Business Officer",
        years: "18+",
        salary: "$280K-$400K",
        description: "Executive leadership of business development and strategy"
      }
    ];
  }
  
  // PROJECT MANAGEMENT CAREER PATH
  if (title.includes('project manager')) {
    return [
      {
        role: "Project Coordinator",
        years: "0-2",
        salary: "$45K-$65K",
        description: "Support project activities and coordinate team communications"
      },
      {
        role: "Project Manager",
        years: "2-5",
        salary: "$65K-$95K",
        description: "Lead projects from initiation to completion"
      },
      {
        role: "Senior Project Manager",
        years: "5-8",
        salary: "$95K-$130K",
        description: "Manage complex projects and mentor junior PMs"
      },
      {
        role: "Program Manager",
        years: "8-12",
        salary: "$130K-$170K",
        description: "Oversee multiple related projects and strategic initiatives"
      },
      {
        role: "Director of Project Management",
        years: "12-16",
        salary: "$170K-$220K",
        description: "Lead PMO and establish project management standards"
      },
      {
        role: "VP of Operations",
        years: "16+",
        salary: "$220K-$300K",
        description: "Executive leadership of operational excellence"
      }
    ];
  }
  
  // BUSINESS ANALYST CAREER PATH
  if (title.includes('business analyst') && !title.includes('senior')) {
    return [
      {
        role: "Junior Business Analyst",
        years: "0-2",
        salary: "$50K-$70K",
        description: "Support business analysis and documentation activities"
      },
      {
        role: "Business Analyst",
        years: "2-5",
        salary: "$70K-$95K",
        description: "Analyze business processes and recommend improvements"
      },
      {
        role: "Senior Business Analyst",
        years: "5-8",
        salary: "$95K-$125K",
        description: "Lead complex analysis projects and mentor junior analysts"
      },
      {
        role: "Principal Business Analyst",
        years: "8-12",
        salary: "$125K-$160K",
        description: "Drive business analysis strategy and cross-functional initiatives"
      },
      {
        role: "Manager of Business Analysis",
        years: "12-15",
        salary: "$160K-$200K",
        description: "Lead business analysis teams and establish standards"
      },
      {
        role: "Director of Strategy",
        years: "15+",
        salary: "$200K-$280K",
        description: "Executive leadership of strategic analysis and planning"
      }
    ];
  }
  
  // DATA ANALYST CAREER PATH
  if (title.includes('data analyst') || title.includes('junior data analyst')) {
    return [
      {
        role: "Junior Data Analyst",
        years: "0-2",
        salary: "$50K-$70K",
        description: "Support data analysis and reporting activities"
      },
      {
        role: "Data Analyst",
        years: "2-4",
        salary: "$70K-$95K",
        description: "Analyze data and create insights for business decisions"
      },
      {
        role: "Senior Data Analyst",
        years: "4-7",
        salary: "$95K-$125K",
        description: "Lead complex analysis projects and mentor junior analysts"
      },
      {
        role: "Data Scientist",
        years: "7-10",
        salary: "$125K-$160K",
        description: "Build predictive models and advanced analytics solutions"
      },
      {
        role: "Senior Data Scientist",
        years: "10-14",
        salary: "$160K-$200K",
        description: "Lead data science initiatives and cross-functional projects"
      },
      {
        role: "Director of Analytics",
        years: "14+",
        salary: "$200K-$280K",
        description: "Executive leadership of data and analytics organization"
      }
    ];
  }
  
  // UX DESIGNER CAREER PATH
  if (title.includes('ux designer') || title.includes('junior ux designer')) {
    return [
      {
        role: "Junior UX Designer",
        years: "0-2",
        salary: "$50K-$70K",
        description: "Create wireframes and support design projects under guidance"
      },
      {
        role: "UX Designer",
        years: "2-5",
        salary: "$70K-$100K",
        description: "Lead design projects and conduct user research"
      },
      {
        role: "Senior UX Designer",
        years: "5-8",
        salary: "$100K-$135K",
        description: "Lead complex design initiatives and mentor junior designers"
      },
      {
        role: "Principal UX Designer",
        years: "8-12",
        salary: "$135K-$175K",
        description: "Drive design strategy and cross-functional collaboration"
      },
      {
        role: "Design Manager",
        years: "12-15",
        salary: "$175K-$220K",
        description: "Manage design teams and set design standards"
      },
      {
        role: "Director of Design",
        years: "15+",
        salary: "$220K-$300K",
        description: "Lead design organization and establish design culture"
      }
    ];
  }
  
  // Generic Management Career Path (fallback for any remaining titles)
  return [
    {
      role: "Analyst",
      years: "0-2",
      salary: "$55K-$75K",
      description: "Support business operations and analysis"
    },
    {
      role: "Manager",
      years: "2-5",
      salary: "$75K-$105K",
      description: "Lead projects and manage team members"
    },
    {
      role: "Senior Manager",
      years: "5-8",
      salary: "$105K-$140K",
      description: "Drive strategic initiatives and mentor staff"
    },
    {
      role: "Director",
      years: "8-12",
      salary: "$140K-$180K",
      description: "Lead department and set strategic direction"
    },
    {
      role: "Vice President",
      years: "12-18",
      salary: "$180K-$250K",
      description: "Executive leadership and organizational strategy"
    },
    {
      role: "C-Suite Executive",
      years: "18+",
      salary: "$250K-$400K",
      description: "Senior executive leadership and company strategy"
    }
  ];
};

// FIXED: Generate career-specific day in life content with improved matching logic
const getCareerSpecificDayInLife = (careerTitle: string): string => {
  const title = careerTitle.toLowerCase();
  
  console.log('🔍 Generating day-in-life for career title:', careerTitle);
  console.log('🔍 Lowercase title for matching:', title);
  
  // EXECUTIVE PRODUCT LEADERSHIP ROLES
  if ((title.includes('vp') || title.includes('vice president')) && title.includes('product')) {
    console.log('✅ Matched: VP of Product Management');
    return "Start your day at 8:30 AM reviewing overnight product metrics and user feedback from global markets. Your morning begins with a strategic product portfolio review meeting with your senior product managers, discussing quarterly OKRs and roadmap priorities. At 10:00 AM, you lead a cross-functional leadership session with engineering, design, and marketing VPs to align on upcoming product launches. Mid-morning involves one-on-one mentoring sessions with senior product managers, helping them navigate complex stakeholder relationships and strategic decisions. Lunch is often a working session with C-suite executives, presenting product vision updates and discussing market expansion opportunities. Your afternoon focuses on product strategy deep-dives, reviewing competitive analysis, and making key decisions about resource allocation across product lines. You spend time in user research sessions, staying connected to customer needs and market trends. The day concludes with strategic planning for upcoming board presentations and reviewing product performance dashboards that will inform tomorrow's strategic decisions.";
  }
  
  if (title.includes('chief product officer') || title.includes('cpo')) {
    console.log('✅ Matched: Chief Product Officer');
    return "Your day begins at 8:00 AM with a comprehensive review of global product performance metrics and market intelligence reports. Morning starts with C-suite strategy meetings where you present product vision alignment with overall business objectives and discuss quarterly board presentation materials. At 9:30 AM, you lead organizational leadership sessions with VP-level product leaders, setting strategic direction and ensuring product portfolio coherence across all business units. Mid-morning involves strategic decision-making sessions with the CEO and board members about product innovation roadmaps and market expansion strategies. You spend significant time in product vision setting activities, working with design and engineering leadership to ensure technical feasibility of strategic initiatives. Lunch often includes external meetings with key enterprise customers or strategic partners to understand market needs and validate product direction. Your afternoon focuses on organizational development, mentoring VP-level product leaders and driving product culture transformation across the company. You review and approve major product investment decisions, analyze competitive positioning, and work on long-term product strategy that will define the company's future. The day ends with preparation for board meetings and strategic planning sessions that will shape the organization's product direction for the next quarter.";
  }
  
  // EXECUTIVE UX/DESIGN LEADERSHIP ROLES
  if ((title.includes('vp') || title.includes('vice president')) && (title.includes('user experience') || title.includes('ux') || title.includes('design'))) {
    console.log('✅ Matched: VP of User Experience');
    return "Begin your day at 8:30 AM reviewing user experience metrics, usability testing results, and design system adoption rates across all product teams. Your morning starts with design leadership meetings where you review the design portfolio with senior UX managers and discuss design strategy initiatives that align with business objectives. At 10:00 AM, you facilitate cross-functional collaboration sessions with product, engineering, and research teams to ensure design excellence across all user touchpoints. Mid-morning involves design vision alignment activities, working with design directors to establish design principles and ensure consistency across the entire product ecosystem. You spend time mentoring senior UX designers and design managers, helping them develop their strategic thinking and leadership capabilities. Lunch often includes design critique sessions with the broader design team, fostering a culture of design excellence and continuous improvement. Your afternoon focuses on design strategy evolution, reviewing user research insights and translating them into actionable design system improvements. You work closely with engineering leadership to ensure design implementation quality and advocate for user-centered design practices across the organization. The day concludes with stakeholder meetings about user experience strategy, design team performance reviews, and planning for design organization growth and development.";
  }
  
  if (title.includes('chief experience officer') || title.includes('cxo')) {
    console.log('✅ Matched: Chief Experience Officer');
    return "Your day starts at 8:00 AM with a comprehensive review of customer experience metrics, user satisfaction scores, and experience analytics from all customer touchpoints. Morning begins with C-suite strategy meetings where you present customer experience insights and their impact on business performance, working closely with the CEO on experience-driven business strategy. At 9:30 AM, you lead experience strategy sessions with cross-functional leadership teams, ensuring that customer experience excellence is embedded in every aspect of the business. Mid-morning involves customer insights analysis, reviewing journey mapping data and identifying opportunities for experience innovation across all customer interactions. You spend significant time in experience vision setting, working with design, product, marketing, and operations teams to create cohesive customer experiences. Lunch frequently includes meetings with key customers or experience research sessions to stay directly connected to customer needs and pain points. Your afternoon focuses on experience transformation initiatives, mentoring VP-level experience leaders and driving organizational change toward customer-centricity. You review and approve major experience investment decisions, analyze competitive experience positioning, and work on long-term experience strategy that differentiates the company in the market. The day ends with strategic decision-making about customer experience innovation and planning for experience optimization programs that will define the company's competitive advantage.";
  }
  
  // STRATEGY ROLES
  if (title.includes('strategy') && (title.includes('vp') || title.includes('vice president') || title.includes('director'))) {
    console.log('✅ Matched: Senior Strategy Role');
    return "Start your day at 8:30 AM reviewing overnight market intelligence reports, competitive analysis updates, and strategic initiative progress dashboards. Your morning begins with executive strategy sessions where you present strategic recommendations to C-suite leadership and facilitate strategic planning discussions. At 9:30 AM, you lead cross-functional strategic planning meetings with department heads, ensuring strategic alignment across all business units and driving strategic initiative execution. Mid-morning involves deep strategic analysis work, reviewing market data, financial models, and competitive positioning to identify new business opportunities and strategic threats. You spend time mentoring strategy managers and analysts, helping them develop strategic thinking capabilities and analytical skills. Lunch often includes external meetings with industry experts, consultants, or strategic partners to gather market insights and validate strategic assumptions. Your afternoon focuses on strategic workshop facilitation, working with various departments to develop implementation plans for strategic initiatives. You collaborate extensively with finance, operations, and business development teams to ensure strategic plans are financially viable and operationally feasible. The day concludes with strategic roadmap updates, executive briefing preparation, and strategic performance review sessions that will inform tomorrow's strategic decisions and long-term planning activities.";
  }
  
  if (title.includes('strategy') && (title.includes('manager') || title.includes('senior'))) {
    console.log('✅ Matched: Strategy Manager');
    return "Begin your day at 9:00 AM by reviewing strategic project dashboards and checking progress on key strategic initiatives across multiple business units. Your morning starts with strategic analysis work, diving deep into market research data, competitive intelligence, and financial modeling to support strategic decision-making. At 10:30 AM, you facilitate strategic planning sessions with cross-functional teams, helping them align their activities with overall strategic objectives. Mid-morning involves stakeholder meetings with department leaders, presenting strategic insights and recommendations that will guide their operational decisions. You spend significant time on strategic research and analysis, using various analytical frameworks to evaluate business opportunities and strategic options. Lunch is often a working session with strategy team members, collaborating on strategic presentations and discussing analytical findings. Your afternoon focuses on strategic project management, coordinating strategic initiatives across multiple departments and ensuring timely execution of strategic plans. You work closely with senior leadership to prepare strategic briefings and board presentation materials. The day ends with strategic documentation updates, team coordination activities, and preparation for tomorrow's strategic analysis work and stakeholder meetings.";
  }
  
  // OPERATIONS ROLES
  if (title.includes('operations') && (title.includes('vp') || title.includes('vice president') || title.includes('coo') || title.includes('chief operating'))) {
    console.log('✅ Matched: Senior Operations Role');
    return "Your day begins at 8:00 AM with a comprehensive review of operational KPIs, performance metrics, and overnight operational reports from all business units. Morning starts with operational leadership meetings where you review operational excellence initiatives and discuss process improvement opportunities with department heads. At 9:30 AM, you lead cross-departmental coordination sessions, ensuring seamless operational alignment between supply chain, manufacturing, customer service, and logistics teams. Mid-morning involves operational strategy sessions, working with senior managers to optimize operational efficiency and implement operational excellence programs. You spend time on operational problem-solving, addressing complex operational challenges and making strategic decisions about resource allocation and process improvements. Lunch often includes operational review meetings with key stakeholders, discussing operational performance and planning operational scaling initiatives. Your afternoon focuses on operational transformation projects, driving operational innovation and implementing new operational technologies and processes. You work closely with finance and HR teams to ensure operational plans are properly resourced and staffed. The day concludes with operational reporting activities, team leadership sessions, and strategic planning for operational excellence initiatives that will improve overall business performance and operational efficiency.";
  }
  
  if (title.includes('operations') && (title.includes('manager') || title.includes('senior'))) {
    console.log('✅ Matched: Operations Manager');
    return "Start your day at 8:30 AM reviewing operational dashboards, checking overnight operational metrics, and identifying any operational issues that need immediate attention. Your morning begins with team standup meetings where you coordinate daily operational activities and ensure all team members are aligned on operational priorities. At 10:00 AM, you facilitate operational improvement sessions, working with your team to identify process inefficiencies and implement operational enhancements. Mid-morning involves cross-departmental coordination meetings, collaborating with other operational teams to ensure smooth operational flow and resolve any operational bottlenecks. You spend significant time on operational problem-solving, addressing day-to-day operational challenges and implementing solutions that improve operational performance. Lunch is often a working session with operational team members, discussing operational procedures and planning operational improvements. Your afternoon focuses on operational monitoring and control, ensuring operational standards are maintained and operational targets are achieved. You work on operational reporting, preparing operational performance summaries for senior leadership. The day ends with operational planning activities, team performance reviews, and preparation for tomorrow's operational activities and operational improvement initiatives.";
  }
  
  // BUSINESS DEVELOPMENT ROLES
  if (title.includes('business development') || title.includes('bizdev')) {
    console.log('✅ Matched: Business Development Role');
    return "Begin your day at 8:30 AM reviewing your partnership pipeline, checking overnight responses from potential partners, and analyzing partnership opportunity metrics. Your morning starts with partnership strategy sessions, identifying new partnership opportunities and developing partnership approaches for target companies. At 10:00 AM, you conduct partnership discovery calls with potential strategic partners, exploring mutual value propositions and partnership structures. Mid-morning involves partnership proposal development, creating compelling partnership presentations and negotiating partnership terms with key stakeholders. You spend time on market research activities, identifying emerging partnership trends and competitive partnership landscapes. Lunch often includes partnership meetings with existing partners or potential new partners, building relationships and exploring partnership expansion opportunities. Your afternoon focuses on partnership negotiation and deal structuring, working with legal and finance teams to finalize partnership agreements. You collaborate extensively with sales and marketing teams to ensure partnership opportunities are properly leveraged for business growth. The day concludes with partnership pipeline management, partnership performance analysis, and strategic planning for partnership development activities that will drive business growth and market expansion.";
  }
  
  // PROJECT MANAGEMENT ROLES
  if (title.includes('project manager') || title.includes('program manager')) {
    console.log('✅ Matched: Project Manager');
    return "Start your day at 8:30 AM reviewing project dashboards, checking project status updates, and identifying any project risks or issues that need immediate attention. Your morning begins with team standup meetings where you coordinate daily project activities and ensure all team members are aligned on project deliverables and timelines. At 10:00 AM, you facilitate stakeholder meetings, providing project updates and managing stakeholder expectations about project progress and upcoming milestones. Mid-morning involves project planning and resource coordination, working with various teams to ensure project resources are properly allocated and project timelines are achievable. You spend significant time on project risk management, identifying potential project obstacles and developing mitigation strategies to keep projects on track. Lunch is often a working session with project team members, discussing project challenges and collaborating on project solutions. Your afternoon focuses on project monitoring and control, tracking project progress against project plans and making necessary adjustments to ensure project success. You work on project documentation and reporting, preparing project status reports for senior leadership and project stakeholders. The day ends with project planning activities, team coordination sessions, and preparation for tomorrow's project activities and project milestone reviews.";
  }
  
  // BUSINESS ANALYST ROLES
  if (title.includes('business analyst')) {
    console.log('✅ Matched: Business Analyst');
    return "Begin your day at 9:00 AM reviewing business requirements documentation and checking for any updates or changes from stakeholders. Your morning starts with stakeholder interviews and requirements gathering sessions, working closely with business users to understand their needs and document business processes. At 10:30 AM, you conduct business process analysis, mapping current state processes and identifying opportunities for business process improvements. Mid-morning involves data analysis activities, analyzing business data to identify trends, patterns, and insights that support business decision-making. You spend time on business documentation, creating detailed business requirements documents and process flow diagrams. Lunch often includes collaborative sessions with technical teams, translating business requirements into technical specifications and ensuring technical solutions meet business needs. Your afternoon focuses on business solution design, working with stakeholders to develop business solutions that address identified business challenges. You facilitate requirements workshops and validation sessions, ensuring business requirements are complete and accurate. The day ends with business analysis reporting, stakeholder communication, and preparation for tomorrow's business analysis activities and stakeholder meetings.";
  }
  
  // DATA ANALYST ROLES
  if (title.includes('data analyst') || title.includes('junior data analyst')) {
    console.log('✅ Matched: Data Analyst');
    return "Start your day at 9:00 AM by reviewing overnight data processing jobs and checking data quality reports to ensure data integrity. Your morning begins with data extraction and preparation activities, writing SQL queries to pull relevant datasets and cleaning data for analysis. At 10:30 AM, you conduct statistical analysis and data exploration, using analytical tools to identify trends, patterns, and insights in the data. Mid-morning involves data visualization creation, building charts, graphs, and dashboards that communicate data insights effectively to stakeholders. You spend time on analytical reporting, preparing data analysis summaries and presenting findings to business stakeholders. Lunch is often a learning session where you explore new analytical techniques or attend training sessions on advanced analytics tools. Your afternoon focuses on collaborative analysis work, partnering with business teams to understand their analytical needs and provide data-driven insights that support business decisions. You work on data documentation and methodology documentation, ensuring your analytical work is reproducible and well-documented. The day ends with data analysis planning, preparing for tomorrow's analytical projects, and staying current with new analytical tools and techniques that can improve your analytical capabilities.";
  }
  
  // UX DESIGNER ROLES
  if (title.includes('ux designer') || title.includes('junior ux designer') || (title.includes('user experience') && title.includes('designer'))) {
    console.log('✅ Matched: UX Designer');
    return "Begin your day at 9:00 AM reviewing user research insights and checking overnight user feedback from recent design releases. Your morning starts with design exploration and wireframing activities, creating user interface concepts and exploring different design solutions for user experience challenges. At 10:30 AM, you conduct user research sessions, interviewing users or facilitating usability testing to understand user needs and validate design decisions. Mid-morning involves design collaboration sessions, working closely with product managers and engineers to ensure design feasibility and alignment with product requirements. You spend time on design system work, creating and maintaining design components that ensure design consistency across products. Lunch often includes design critique sessions with other designers, sharing design work and receiving feedback to improve design quality. Your afternoon focuses on design iteration and refinement, incorporating user feedback and stakeholder input into design improvements. You work on design documentation and specification creation, preparing detailed design specifications that guide engineering implementation. The day ends with design planning activities, preparing for tomorrow's design work, and staying current with design trends and user experience best practices that can enhance your design capabilities.";
  }
  
  // ENHANCED FALLBACK: More specific based on career type patterns
  console.log('⚠️ Using enhanced fallback for career title:', careerTitle);
  
  // Check for leadership/management roles
  if (title.includes('director') || title.includes('head of') || title.includes('lead')) {
    return `As a ${careerTitle}, your day starts at 8:30 AM with leadership team meetings and strategic planning sessions. Your morning involves reviewing team performance metrics, conducting one-on-one meetings with direct reports, and making strategic decisions that impact your department's direction. Mid-morning includes cross-functional collaboration with other department leaders and stakeholder meetings to align on organizational priorities. You spend significant time on team development and mentoring, helping your team members grow their skills and advance their careers. Lunch often includes strategic discussions with senior leadership or external partners. Your afternoon focuses on strategic project oversight, resource planning, and performance management activities. You work on organizational development initiatives and process improvements that enhance team effectiveness. The day concludes with strategic planning for upcoming initiatives, team performance reviews, and preparation for tomorrow's leadership activities and strategic decisions.`;
  }
  
  // Check for senior individual contributor roles
  if (title.includes('senior') || title.includes('principal') || title.includes('staff')) {
    return `As a ${careerTitle}, you begin your day at 9:00 AM by reviewing complex technical or analytical work and planning your approach to challenging projects. Your morning involves deep focus work on high-impact initiatives, leveraging your expertise to solve complex problems and deliver high-quality results. Mid-morning includes collaboration with cross-functional teams, sharing your expertise and providing technical or strategic guidance to colleagues. You spend time mentoring junior team members, helping them develop their skills and learn from your experience. Lunch often includes knowledge-sharing sessions or professional development activities. Your afternoon focuses on advanced project work, innovation initiatives, and contributing to strategic decisions within your area of expertise. You work on thought leadership activities, staying current with industry trends and best practices. The day ends with project planning, documentation of your work, and preparation for tomorrow's complex challenges and strategic contributions.`;
  }
  
  // Generic professional role fallback
  return `As a ${careerTitle}, you start your day at 9:00 AM by reviewing your priorities and checking in with your team members or stakeholders. Your morning typically involves focused work on your core responsibilities, whether that's analysis, project coordination, client interaction, or strategic planning. Mid-morning includes collaborative sessions with colleagues, participating in meetings, and contributing to team objectives. You spend time on professional development, learning new skills or staying current with industry trends relevant to your role. Lunch provides an opportunity for networking or informal collaboration with colleagues. Your afternoon focuses on project execution, problem-solving, and delivering results that contribute to your team's success. You work on communication and documentation, ensuring stakeholders are informed and your work is properly recorded. The day concludes with planning for tomorrow's activities, reflecting on progress made, and preparing for upcoming challenges and opportunities in your professional role.`;
};

// Generate professional PDF career guide
const generateCareerGuide = (career: CareerMatch, user: User) => {
  const doc = new jsPDF();
  let yPosition = 20;
  const pageWidth = doc.internal.pageSize.width;
  const margin = 20;

  // Header
  doc.setFillColor(59, 130, 246);
  doc.rect(0, 0, pageWidth, 35, 'F');
  
  doc.setTextColor(255, 255, 255);
  doc.setFontSize(20);
  doc.setFont('helvetica', 'bold');
  doc.text(`${career.title} Career Guide`, pageWidth / 2, 20, { align: 'center' });
  
  doc.setFontSize(10);
  doc.text(`Personalized for ${user.firstName} ${user.lastName}`, pageWidth / 2, 28, { align: 'center' });

  yPosition = 50;

  // Career Overview
  doc.setTextColor(0, 0, 0);
  doc.setFontSize(16);
  doc.setFont('helvetica', 'bold');
  doc.text('Career Overview', margin, yPosition);
  yPosition += 15;

  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  const description = doc.splitTextToSize(career.description, pageWidth - (margin * 2));
  doc.text(description, margin, yPosition);
  yPosition += description.length * 5 + 10;

  // Key Information
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.text('Key Information', margin, yPosition);
  yPosition += 10;

  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  doc.text(`Salary Range: ${career.salaryRange}`, margin, yPosition);
  yPosition += 8;
  doc.text(`Experience Level: ${career.experienceLevel}`, margin, yPosition);
  yPosition += 8;
  doc.text(`Learning Path: ${career.learningPath}`, margin, yPosition);
  yPosition += 8;
  doc.text(`Match Score: ${career.relevanceScore}%`, margin, yPosition);
  yPosition += 15;

  // Required Skills
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.text('Required Skills', margin, yPosition);
  yPosition += 10;

  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  doc.text('Technical Skills:', margin, yPosition);
  yPosition += 6;
  career.requiredTechnicalSkills?.forEach(skill => {
    doc.text(`• ${skill}`, margin + 10, yPosition);
    yPosition += 5;
  });
  yPosition += 5;

  doc.text('Soft Skills:', margin, yPosition);
  yPosition += 6;
  career.requiredSoftSkills?.forEach(skill => {
    doc.text(`• ${skill}`, margin + 10, yPosition);
    yPosition += 5;
  });
  yPosition += 10;

  // Top Companies
  if (career.companies && career.companies.length > 0) {
    doc.setFontSize(14);
    doc.setFont('helvetica', 'bold');
    doc.text('Top Employers', margin, yPosition);
    yPosition += 10;

    doc.setFontSize(10);
    doc.setFont('helvetica', 'normal');
    career.companies.slice(0, 10).forEach(company => {
      doc.text(`• ${company}`, margin, yPosition);
      yPosition += 5;
    });
  }

  // Save the PDF
  doc.save(`${career.title.replace(/\s+/g, '_')}_Career_Guide.pdf`);
};

const CareerDetail = () => {
  const navigate = useNavigate();
  const { careerType } = useParams();
  const [user, setUser] = useState<User | null>(null);
  const [activeTab, setActiveTab] = useState("overview");
  const [career, setCareer] = useState<CareerMatch | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [connectionsDialogOpen, setConnectionsDialogOpen] = useState(false);
  const [isSaving, setIsSaving] = useState(false); // NEW: Track saving state

  // FIXED: Load user data and find the specific career directly from templates
  useEffect(() => {
    const fetchCareerData = async () => {
      console.log('🔍 CareerDetail loading for careerType:', careerType);
      
      try {
        const currentUser = localStorage.getItem('currentUser');
        if (!currentUser) {
          console.log('❌ No user found, redirecting to auth');
          navigate('/auth');
          return;
        }
        
        const userData = JSON.parse(currentUser);
        console.log('👤 User loaded:', userData.firstName, userData.lastName);
        
        if (!userData.profileCompleted || !userData.assessmentData) {
          console.log('❌ Profile incomplete, redirecting to assessment');
          navigate('/assessment');
          return;
        }
        
        setUser(userData);

        const response = await fetch(`http://localhost:8002/api/career/${careerType}`);
        if (!response.ok) {
          throw new Error(`API request failed: ${response.status}`);
        }
        const careerData = await response.json();
        
        if (careerData) {
          console.log('✅ Career found:', careerData.title);
          
          // Convert template to CareerMatch format with default values
          const careerMatch: CareerMatch = {
            ...careerData,
            relevanceScore: 85, // Default score for direct template access
            confidenceLevel: 80,
            matchReasons: ['Direct career exploration', 'Matches your profile interests']
          };
          
          setCareer(careerMatch);
          console.log('✅ Career set successfully');
        } else {
          console.log('❌ Career not found');
          setError(`Career "${careerType}" not found in our database`);
        }
        
        setLoading(false);
      } catch (err) {
        console.error('❌ Error loading career data:', err);
        setError('Failed to load career information');
        setLoading(false);
      }
    };

    fetchCareerData();
  }, [navigate, careerType]);

  // FIXED: Enhanced save career functionality with comprehensive error handling and debugging
  const handleSaveCareer = async () => {
    if (!career || !user) {
      showError('Unable to save career - missing data');
      return;
    }
    
    console.log('💾 Starting save career process...');
    console.log('👤 User ID:', user.id);
    console.log('🎯 Career Type:', career.careerType);
    console.log('📋 Current saved careers:', user.savedCareers);
    
    setIsSaving(true);
    
    try {
      // Get current saved careers array
      const currentSavedCareers = user.savedCareers || [];
      console.log('📊 Current saved careers count:', currentSavedCareers.length);
      
      // Check if already saved
      if (currentSavedCareers.includes(career.careerType)) {
        console.log('⚠️ Career already saved');
        showSuccess(`${career.title} is already in your favorites!`);
        setIsSaving(false);
        return;
      }
      
      // Add to saved careers
      const updatedSavedCareers = [...currentSavedCareers, career.careerType];
      console.log('✅ Updated saved careers:', updatedSavedCareers);
      
      // Update user object
      const updatedUser = {
        ...user,
        savedCareers: updatedSavedCareers,
        lastSavedCareer: career.careerType,
        lastSavedAt: new Date().toISOString()
      };
      
      console.log('💾 Saving to localStorage...');
      
      // Update current user in localStorage
      localStorage.setItem('currentUser', JSON.stringify(updatedUser));
      console.log('✅ Current user updated in localStorage');
      
      // Update users array in localStorage
      const usersData = localStorage.getItem('users');
      if (usersData) {
        try {
          const users = JSON.parse(usersData);
          const userIndex = users.findIndex((u: any) => u.id === user.id);
          
          if (userIndex !== -1) {
            users[userIndex] = updatedUser;
            localStorage.setItem('users', JSON.stringify(users));
            console.log('✅ Users array updated in localStorage');
          } else {
            console.error('❌ User not found in users array');
            showError('Error updating user data');
            setIsSaving(false);
            return;
          }
        } catch (parseError) {
          console.error('❌ Error parsing users data:', parseError);
          showError('Error accessing user data');
          setIsSaving(false);
          return;
        }
      } else {
        console.error('❌ No users data found in localStorage');
        showError('Error accessing user database');
        setIsSaving(false);
        return;
      }
      
      // Update local state
      setUser(updatedUser);
      
      // Verify the save worked
      const verifyUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
      if (verifyUser.savedCareers && verifyUser.savedCareers.includes(career.careerType)) {
        console.log('✅ Save verification successful');
        showSuccess(`🎉 ${career.title} saved to your favorites! Check the Saved tab in your dashboard.`);
      } else {
        console.error('❌ Save verification failed');
        showError('Career save verification failed');
      }
      
    } catch (error) {
      console.error('❌ Error saving career:', error);
      showError('Failed to save career. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  // FIXED: Navigate to Dashboard Learning tab using React Router state
  const handleStartLearning = () => {
    if (!career) return;
    
    // Navigate to dashboard with state to open learning tab
    navigate('/dashboard', { 
      state: { 
        activeTab: 'learning',
        fromCareer: career.title 
      } 
    });
    
    showSuccess(`Opening learning resources for ${career.title}!`);
  };

  const handleFindConnections = () => {
    if (!career) return;
    
    setConnectionsDialogOpen(true);
    showSuccess('Opening networking opportunities...');
  };

  const handleDownloadGuide = () => {
    if (!career || !user) return;
    
    try {
      generateCareerGuide(career, user);
      showSuccess(`Career guide for ${career.title} downloaded!`);
    } catch (error) {
      showError('Failed to generate career guide. Please try again.');
    }
  };

  // FIXED: Logo navigation
  const handleLogoClick = () => {
    navigate('/');
  };

  // Networking functions
  const handleLinkedInSearch = () => {
    if (!career) return;
    
    const searchQuery = `"${career.title}" AND "${user?.assessmentData?.location || 'United States'}"`;
    const linkedinUrl = `https://www.linkedin.com/search/results/people/?keywords=${encodeURIComponent(searchQuery)}`;
    window.open(linkedinUrl, '_blank', 'noopener,noreferrer');
    showSuccess('Opening LinkedIn search in new tab');
  };

  const handleCopyMessage = (message: string) => {
    navigator.clipboard.writeText(message).then(() => {
      showSuccess('Message template copied to clipboard!');
    }).catch(() => {
      showSuccess('Template ready to copy manually');
    });
  };

  const handleViewOpenings = (companyName: string) => {
    if (!career) return;
    
    // Construct LinkedIn jobs search URL with job title and company name
    const searchQuery = `${career.title} ${companyName}`;
    const linkedinJobsUrl = `https://www.linkedin.com/jobs/search/?keywords=${encodeURIComponent(searchQuery)}`;
    
    window.open(linkedinJobsUrl, '_blank', 'noopener,noreferrer');
    showSuccess(`Opening job search for ${career.title} at ${companyName}`);
  };

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading career details...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error || !career) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-600 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">Career Not Found</h2>
          <p className="text-gray-600 mb-4">
            {error || "The career you're looking for doesn't exist or you don't have access."}
          </p>
          <div className="space-y-2 mb-4">
            <p className="text-sm text-gray-500">Requested career type: <code>{careerType}</code></p>
            <p className="text-sm text-gray-500">Available careers: {CAREER_TEMPLATES.length}</p>
          </div>
          <Button onClick={() => navigate('/dashboard')}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  // Check if career is already saved
  const isCareerSaved = user?.savedCareers?.includes(career.careerType) || false;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <Button variant="ghost" onClick={() => navigate('/dashboard')}>
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Dashboard
              </Button>
              <div className="cursor-pointer" onClick={handleLogoClick}>
                <Logo size="lg" />
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <Button variant="ghost" onClick={handleLogoClick}>
                <Home className="h-4 w-4 mr-2" />
                Home
              </Button>
              <Avatar>
                <AvatarFallback>
                  {user?.firstName?.[0] || 'U'}{user?.lastName?.[0] || 'U'}
                </AvatarFallback>
              </Avatar>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Career Header */}
        <div className="bg-white rounded-lg shadow-sm border p-8 mb-8">
          <div className="flex justify-between items-start mb-6">
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-4">
                <h1 className="text-4xl font-bold text-gray-900">{career.title}</h1>
                <Badge variant="secondary" className="bg-green-100 text-green-800 font-semibold px-3 py-1">
                  {career.relevanceScore}% match
                </Badge>
                <Badge variant="outline" className="text-sm">
                  {career.experienceLevel}
                </Badge>
                {isCareerSaved && (
                  <Badge variant="secondary" className="bg-pink-100 text-pink-800 font-semibold px-3 py-1">
                    <Heart className="h-3 w-3 mr-1 fill-current" />
                    Saved
                  </Badge>
                )}
              </div>
              <p className="text-xl text-gray-600 leading-relaxed mb-6">
                {career.description}
              </p>
              
              {/* Key Metrics Grid */}
              <div className="grid md:grid-cols-4 gap-6">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <DollarSign className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                  <div className="font-semibold text-gray-900">{career.salaryRange}</div>
                  <div className="text-sm text-gray-600">Salary Range</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <TrendingUp className="h-8 w-8 text-green-600 mx-auto mb-2" />
                  <div className="font-semibold text-gray-900">High Growth</div>
                  <div className="text-sm text-gray-600">Job Market</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <Clock className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                  <div className="font-semibold text-gray-900">{career.learningPath}</div>
                  <div className="text-sm text-gray-600">Learning Time</div>
                </div>
                <div className="text-center p-4 bg-orange-50 rounded-lg">
                  <MapPin className="h-8 w-8 text-orange-600 mx-auto mb-2" />
                  <div className="font-semibold text-gray-900">{career.remoteOptions || 'Flexible'}</div>
                  <div className="text-sm text-gray-600">Remote Options</div>
                </div>
              </div>
            </div>
          </div>
          
          {/* FIXED: Enhanced Action Buttons with save state management */}
          <div className="flex flex-wrap gap-4">
            <Button 
              size="lg" 
              onClick={handleSaveCareer}
              disabled={isSaving || isCareerSaved}
              className={isCareerSaved ? "bg-pink-600 hover:bg-pink-700" : ""}
            >
              {isSaving ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Saving...
                </>
              ) : isCareerSaved ? (
                <>
                  <HeartHandshake className="h-4 w-4 mr-2" />
                  Saved to Favorites
                </>
              ) : (
                <>
                  <Star className="h-4 w-4 mr-2" />
                  Save Career
                </>
              )}
            </Button>
            <Button variant="outline" size="lg" onClick={handleStartLearning}>
              <BookOpen className="h-4 w-4 mr-2" />
              Start Learning Path
            </Button>
            <Button variant="outline" size="lg" onClick={handleFindConnections}>
              <Users className="h-4 w-4 mr-2" />
              Find Connections
            </Button>
            <Button variant="outline" size="lg" onClick={handleDownloadGuide}>
              <Download className="h-4 w-4 mr-2" />
              Download Guide
            </Button>
          </div>
        </div>

        {/* Detailed Content Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger
              value="overview"
              className="hover:bg-blue-50 hover:text-blue-700 transition-colors duration-200"
            >
              Overview
            </TabsTrigger>
            {/* COMMENTED OUT: Day in Life section - currently generic */}
            {/* <TabsTrigger
              value="day-in-life"
              className="hover:bg-green-50 hover:text-green-700 transition-colors duration-200"
            >
              Day in Life
            </TabsTrigger> */}
            <TabsTrigger
              value="skills"
              className="hover:bg-purple-50 hover:text-purple-700 transition-colors duration-200"
            >
              Skills & Learning
            </TabsTrigger>
            <TabsTrigger
              value="companies"
              className="hover:bg-orange-50 hover:text-orange-700 transition-colors duration-200"
            >
              Companies
            </TabsTrigger>
            <TabsTrigger
              value="progression"
              className="hover:bg-indigo-50 hover:text-indigo-700 transition-colors duration-200"
            >
              Career Path
            </TabsTrigger>
            <TabsTrigger
              value="networking"
              className="hover:bg-pink-50 hover:text-pink-700 transition-colors duration-200"
            >
              Networking
            </TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Briefcase className="h-5 w-5 mr-2" />
                    Why This Matches You
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium">Overall Match</span>
                        <span className="text-sm text-gray-600">{career.relevanceScore}%</span>
                      </div>
                      <Progress value={career.relevanceScore} className="h-2" />
                    </div>
                    
                    <div className="space-y-3">
                      <h4 className="font-medium text-green-700">✓ Match Reasons</h4>
                      <div className="space-y-2">
                        {career.matchReasons.map((reason, idx) => (
                          <div key={idx} className="flex items-start space-x-2">
                            <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                            <span className="text-sm text-gray-700">{reason}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Target className="h-5 w-5 mr-2" />
                    Key Information
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Experience Level</span>
                      <Badge variant="outline">{career.experienceLevel}</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Salary Range</span>
                      <span className="font-medium">{career.salaryRange}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Learning Path</span>
                      <span className="font-medium">{career.learningPath}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Remote Work</span>
                      <span className="font-medium">{career.remoteOptions || 'Available'}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Required Skills */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Lightbulb className="h-5 w-5 mr-2" />
                  Required Skills
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-medium mb-3">Technical Skills</h4>
                    <div className="flex flex-wrap gap-2">
                      {career.requiredTechnicalSkills?.map((skill, idx) => (
                        <Badge key={idx} variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  <div>
                    
                    <h4 className="font-medium mb-3">Soft Skills</h4>
                    <div className="flex flex-wrap gap-2">
                      {career.requiredSoftSkills?.map((skill, idx) => (
                        <Badge key={idx} variant="outline" className="bg-green-50 text-green-700 border-green-200">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* COMMENTED OUT: Day in Life content - currently generic */}
          {/* <TabsContent value="day-in-life" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Coffee className="h-5 w-5 mr-2" />
                  A Typical Day as a {career.title}
                </CardTitle>
                <CardDescription>
                  Here's what your daily routine might look like in this role
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="prose max-w-none">
                  <p className="text-gray-700 leading-relaxed text-lg">
                    {career.dayInLife}
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent> */}

          {/* Skills & Learning Tab */}
          <TabsContent value="skills" className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Lightbulb className="h-5 w-5 mr-2" />
                    Skills You'll Need
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {[...career.requiredTechnicalSkills, ...career.requiredSoftSkills].slice(0, 6).map((skill, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <span className="font-medium">{skill}</span>
                        <Badge variant="outline">Required</Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <BookOpen className="h-5 w-5 mr-2" />
                    Recommended Learning Path
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="p-4 bg-blue-50 rounded-lg">
                      <h4 className="font-semibold text-blue-900 mb-2">{career.learningPath}</h4>
                      <p className="text-blue-800 text-sm mb-3">
                        Comprehensive program designed to get you job-ready
                      </p>
                      <Button className="w-full" onClick={handleStartLearning}>
                        Start Learning Path
                        <ExternalLink className="h-4 w-4 ml-2" />
                      </Button>
                    </div>
                    
                    <div className="space-y-2">
                      <h4 className="font-medium">Learning Resources</h4>
                      <ul className="space-y-2 text-sm text-gray-600">
                        <li className="flex items-center space-x-2">
                          <PlayCircle className="h-4 w-4" />
                          <span>Online courses and certifications</span>
                        </li>
                        <li className="flex items-center space-x-2">
                          <BookOpen className="h-4 w-4" />
                          <span>Practice projects and portfolios</span>
                        </li>
                        <li className="flex items-center space-x-2">
                          <Users className="h-4 w-4" />
                          <span>Industry communities and forums</span>
                        </li>
                        <li className="flex items-center space-x-2">
                          <Award className="h-4 w-4" />
                          <span>Professional certifications</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Companies Tab */}
          <TabsContent value="companies" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Building className="h-5 w-5 mr-2" />
                  Top Employers for {career.title}
                </CardTitle>
                <CardDescription>
                  Companies actively hiring for this role
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {career.companies?.map((company, index) => (
                    <div key={index} className="p-4 border rounded-lg hover:shadow-md transition-shadow">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                            <Building className="h-5 w-5 text-blue-600" />
                          </div>
                          <div>
                            <h4 className="font-semibold">{company}</h4>
                            <p className="text-sm text-gray-600">Top employer</p>
                          </div>
                        </div>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleViewOpenings(company)}
                          className="ml-2"
                        >
                          <ExternalLink className="h-4 w-4 mr-1" />
                          View Openings
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Industry Insights */}
                <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
                  <h4 className="font-semibold mb-3">Industry Insights</h4>
                  <div className="grid md:grid-cols-3 gap-4">
                    <div className="text-center">
                      <TrendingUp className="h-8 w-8 text-green-600 mx-auto mb-2" />
                      <div className="font-semibold">Growing Field</div>
                      <div className="text-sm text-gray-600">High demand</div>
                    </div>
                    <div className="text-center">
                      <Globe className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                      <div className="font-semibold">Global Opportunities</div>
                      <div className="text-sm text-gray-600">Worldwide roles</div>
                    </div>
                    <div className="text-center">
                      <Zap className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                      <div className="font-semibold">Innovation Focus</div>
                      <div className="text-sm text-gray-600">Cutting-edge work</div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Career Progression Tab - COMPREHENSIVE coverage for ALL job titles */}
          <TabsContent value="progression" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <TrendingUp className="h-5 w-5 mr-2" />
                  Career Progression Path
                </CardTitle>
                <CardDescription>
                  How your career could evolve over time based on real corporate hierarchies
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {/* COMPREHENSIVE: Real career progression for ALL supported job titles */}
                  {getCareerProgression(career.title).map((stage, index) => (
                    <div key={index} className="flex items-center space-x-4 p-4 border rounded-lg">
                      <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center font-semibold text-blue-600">
                        {index + 1}
                      </div>
                      <div className="flex-1">
                        <h4 className="font-semibold">{stage.role}</h4>
                        <p className="text-sm text-gray-600 mb-1">{stage.description}</p>
                        <p className="text-xs text-gray-500">{stage.years} years experience</p>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold">{stage.salary}</p>
                        <p className="text-sm text-gray-600">Salary Range</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Networking Tab */}
          <TabsContent value="networking" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Network className="h-5 w-5 mr-2" />
                  Networking Opportunities
                </CardTitle>
                <CardDescription>
                  Connect with professionals in this field
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h4 className="font-semibold text-blue-900 mb-2">AI-Powered Connection Matching</h4>
                    <p className="text-blue-800 text-sm mb-3">
                      Find {career.title} professionals in your network and get personalized outreach strategies.
                    </p>
                    <Button className="w-full" onClick={handleFindConnections}>
                      Find Connections
                      <Users className="h-4 w-4 ml-2" />
                    </Button>
                  </div>
                  
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center space-x-2 mb-2">
                        <Linkedin className="h-5 w-5 text-blue-600" />
                        <h4 className="font-semibold">LinkedIn Strategy</h4>
                      </div>
                      <p className="text-sm text-gray-600 mb-3">
                        Optimize your profile and connect with {career.title} professionals.
                      </p>
                      <Button variant="outline" size="sm" className="w-full" onClick={handleLinkedInSearch}>
                        Search LinkedIn
                        <ExternalLink className="h-4 w-4 ml-2" />
                      </Button>
                    </div>
                    
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center space-x-2 mb-2">
                        <Calendar className="h-5 w-5 text-green-600" />
                        <h4 className="font-semibold">Industry Events</h4>
                      </div>
                      <p className="text-sm text-gray-600 mb-3">
                        Find networking events and conferences in your area.
                      </p>
                      <Button variant="outline" size="sm" className="w-full">
                        Find Events
                      </Button>
                    </div>
                  </div>

                  {/* Professional Communities */}
                  <div className="mt-6">
                    <h4 className="font-semibold mb-3">Professional Communities</h4>
                    <div className="grid md:grid-cols-2 gap-3">
                      {[
                        "Industry-specific LinkedIn groups",
                        "Professional associations",
                        "Local meetup groups",
                        "Online forums and communities",
                        "Alumni networks",
                        "Slack communities"
                      ].map((community, idx) => (
                        <div key={idx} className="flex items-center space-x-2 p-2 bg-gray-50 rounded">
                          <CheckCircle className="h-4 w-4 text-green-600" />
                          <span className="text-sm">{community}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Bottom CTA */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-8 text-white text-center mt-8">
          <h2 className="text-2xl font-bold mb-4">Ready to Start Your Journey?</h2>
          <p className="text-lg mb-6 opacity-90">
            Take the next step toward becoming a {career.title}
          </p>
          <div className="flex justify-center space-x-4">
            <Button size="lg" variant="secondary" onClick={handleStartLearning}>
              <BookOpen className="h-4 w-4 mr-2" />
              Start Learning Path
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              className="bg-transparent text-white border-white hover:bg-white hover:text-blue-600 transition-colors duration-200" 
              onClick={handleDownloadGuide}
            >
              <FileText className="h-4 w-4 mr-2" />
              Download Career Guide
            </Button>
          </div>
        </div>
      </div>

      {/* Networking Connections Dialog */}
      <Dialog open={connectionsDialogOpen} onOpenChange={setConnectionsDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center space-x-2">
              <Network className="h-5 w-5 text-blue-600" />
              <span>Networking Strategy for {career.title}</span>
            </DialogTitle>
            <DialogDescription>
              Here are personalized networking strategies to help you connect with professionals in this field.
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4">
            {/* LinkedIn Strategy */}
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2 mb-3">
                  <Linkedin className="h-5 w-5 text-blue-600" />
                  <h3 className="font-semibold">LinkedIn Networking</h3>
                </div>
                
                <div className="space-y-3">
                  <div>
                    <p className="text-sm font-medium text-gray-700 mb-1">Search Query:</p>
                    <div className="flex items-center space-x-2">
                      <code className="text-xs bg-gray-100 p-2 rounded flex-1">
                        "{career.title}" AND "{user?.assessmentData?.location || 'United States'}"
                      </code>
                      <Button size="sm" variant="outline" onClick={() => handleCopyMessage(`"${career.title}" AND "${user?.assessmentData?.location || 'United States'}"`)}>
                        <Copy className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  
                  <div>
                    <p className="text-sm font-medium text-gray-700 mb-1">Message Template:</p>
                    <div className="bg-gray-50 p-3 rounded text-sm">
                      <p className="mb-2">
                        "Hi [Name], I noticed your experience as a {career.title} and would love to connect. 
                        I'm currently transitioning into this field and would appreciate any insights you might 
                        share about the industry. Thank you!"
                      </p>
                      <Button size="sm" variant="outline" onClick={() => handleCopyMessage(`Hi [Name], I noticed your experience as a ${career.title} and would love to connect. I'm currently transitioning into this field and would appreciate any insights you might share about the industry. Thank you!`)}>
                        <Copy className="h-4 w-4 mr-1" />
                        Copy Template
                      </Button>
                    </div>
                  </div>
                  
                  <Button className="w-full" onClick={handleLinkedInSearch}>
                    <ExternalLink className="h-4 w-4 mr-2" />
                    Search LinkedIn Now
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Professional Tips */}
            <Card>
              <CardContent className="p-4">
                <h3 className="font-semibold mb-3">Networking Tips</h3>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                    <span>Personalize each message with something specific from their profile</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                    <span>Keep initial messages short and professional</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                    <span>Follow up with a thank you message after connecting</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                    <span>Aim for 20-30% connection acceptance rate with personalized messages</span>
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default CareerDetail;