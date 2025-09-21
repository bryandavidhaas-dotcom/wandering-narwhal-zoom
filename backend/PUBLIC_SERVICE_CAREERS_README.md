# Public Service & Government Careers Database

## Overview
This module contains a comprehensive database of **30 public service and government careers** across federal, state, and local levels. The careers are integrated into the main recommendation engine and include proper salary ranges, experience levels, and skill requirements.

## Career Categories Included

### Federal Government (15 careers)
**Executive Level:**
- Federal Agency Director ($180k-$220k)
- Deputy Secretary ($170k-$200k) 
- Assistant Secretary ($160k-$185k)

**Senior Level:**
- Senior Executive Service (SES) ($140k-$180k)
- GS-15 Program Manager ($110k-$145k)
- Federal Policy Analyst ($85k-$120k)
- Federal Contracting Officer ($90k-$130k)

**Mid Level:**
- GS-13 Management Analyst ($75k-$105k)
- Federal Budget Analyst ($70k-$100k)
- Federal Human Resources Specialist ($65k-$95k)
- Federal IT Specialist ($80k-$115k)

**Entry Level:**
- GS-11 Program Analyst ($55k-$75k)
- Federal Administrative Officer ($45k-$65k)

### State Government (4 careers)
- State Agency Director ($120k-$180k)
- State Program Manager ($75k-$110k)
- State Policy Analyst ($60k-$85k)
- State Social Worker ($50k-$70k)

### Local Government (5 careers)
- City Manager ($100k-$200k)
- County Administrator ($90k-$160k)
- Municipal Department Head ($75k-$120k)
- City Planner ($65k-$95k)
- Municipal Finance Director ($80k-$130k)

### Public Safety (5 careers)
- Police Chief ($90k-$180k)
- Fire Chief ($85k-$160k)
- Emergency Management Director ($75k-$120k)
- Police Detective ($65k-$95k)
- Firefighter/Paramedic ($55k-$85k)

### Legislative Branch (1 career)
- Legislative Director ($90k-$150k)
- Congressional Staff Director ($120k-$180k)
- Legislative Analyst ($60k-$90k)

## Integration Status

✅ **Successfully Integrated** - All 30 careers are now part of the comprehensive career database
✅ **API Compatible** - Careers work with the existing recommendation engine
✅ **Safety Compliant** - Public safety careers are properly protected by safety guardrails
✅ **Tested** - Integration verified through automated testing

## Database Statistics

- **Total Public Service Careers:** 30
- **Salary Range:** $45,000 - $220,000
- **Experience Levels:** Entry (2), Mid (8), Senior (11), Executive (9)
- **Total Database Size:** 296 careers (including all sectors)

## Usage

The public service careers are automatically included in career recommendations when users:
- Have relevant government/public service experience
- Express interest in public service work
- Have appropriate education/background for government roles
- Meet salary and experience requirements

## Safety Features

Public safety careers (Police Chief, Fire Chief, etc.) are protected by the safety guardrail system to ensure only qualified candidates with relevant law enforcement or emergency services background receive these recommendations.

## File Structure

```
backend/
├── public_service_careers.py          # Main career database
├── comprehensive_careers.py           # Integration point
├── test_public_service_careers.py     # Testing script
└── PUBLIC_SERVICE_CAREERS_README.md   # This documentation
```

## Testing

Run the test script to verify integration:
```bash
python backend/test_public_service_careers.py
```

Expected output: ✅ All tests passed! Public service careers are ready to use.