# CRITICAL SAFETY GUARDRAILS - DO NOT REMOVE

## ⚠️ IMPORTANT SAFETY NOTICE ⚠️

This document serves as a permanent record of critical safety guardrails implemented in the career recommendation system to prevent dangerous recommendations.

## The Problem That Was Fixed

**Date**: January 2025  
**Issue**: The Adventure Zone algorithm was recommending a Senior Product Manager (Bryan Haas) become a **Nurse Anesthetist (CRNA)** - a role requiring:
- 7+ years of specialized medical training
- RN license + Master's in Nurse Anesthesia
- Responsibility for administering life-saving/life-threatening anesthesia
- Zero tolerance for errors (patient death risk)

**Root Cause**: Adventure Zone algorithm prioritized "work style compatibility" over fundamental job requirements and safety considerations.

## Safety Guardrails Implemented

### File: `frontend/src/utils/careerMatching.ts`

#### 1. Safety-Critical Career Detection
- **Function**: `isSafetyCriticalCareer()` (lines ~1284-1308)
- **Purpose**: Identifies careers requiring specialized licensing/training
- **Covers**: Medical, Legal, Engineering, Aviation, Financial, Licensed professions

#### 2. Relevant Background Verification  
- **Function**: `hasRelevantBackground()` (lines ~1309-1370)
- **Purpose**: Verifies users have appropriate experience for safety-critical careers
- **Checks**: Industry experience, relevant skills, resume keywords, current role

#### 3. Enhanced Adventure Zone Filtering
- **Location**: Lines ~1477-1482
- **Logic**: Safety check is HIGHEST PRIORITY filter - blocks safety-critical careers without relevant background
- **Logging**: `🚨 SAFETY FILTER: Blocked [Career] - requires specialized training/licensing without relevant background`

#### 4. Stricter Scoring for Safety-Critical Careers
- **Skill Matching**: Safety-critical careers with no relevant skills get only 20% score (vs 80% for regular careers)
- **Minimum Scores**: Safety-critical careers require minimum 70% compatibility (vs 35% for regular careers)

## DO NOT MODIFY WITHOUT:

1. **Understanding the Risk**: Removing these guardrails could recommend life-threatening careers to unqualified users
2. **Explicit Approval**: Get approval from system architects and safety reviewers  
3. **Maintaining Protection**: Ensure any changes maintain or strengthen safety protections
4. **Thorough Testing**: Test with safety-critical career scenarios

## Examples of What This Prevents:

❌ **BLOCKED (Dangerous)**:
- Product Manager → Brain Surgeon
- Marketing Manager → Commercial Pilot  
- Sales Rep → Pharmacist
- Designer → Structural Engineer

✅ **ALLOWED (Safe Transitions)**:
- Product Manager → Strategy Consultant
- Marketing Manager → Sales Director
- Sales Rep → Business Development Manager
- Designer → Creative Director

## Key Safety Functions (DO NOT REMOVE):

- `isSafetyCriticalCareer()`: Identifies careers requiring specialized licensing
- `hasRelevantBackground()`: Verifies users have appropriate experience  
- Safety filtering in Adventure Zone filtering logic
- Stricter scoring for safety-critical careers

## Contact for Changes:

Before modifying any safety-related code, contact:
- System Architects
- Safety Review Team  
- Legal/Compliance Team

## Version History:

- **v1.0** (Jan 2025): Initial safety guardrails implemented to fix CRNA recommendation issue