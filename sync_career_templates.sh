#!/bin/bash

# Career Template Synchronization Script
# This script automates the process of keeping career templates up-to-date
# by extracting career types, finding missing templates, and generating placeholders.

set -e  # Exit on any error

echo "🚀 Starting Career Template Synchronization Process..."
echo "=================================================="

# Step 1: Extract career types from the backend
echo "📊 Step 1: Extracting career types from backend..."
python extract_career_types.py
if [ $? -eq 0 ]; then
    echo "✅ Career types extracted successfully"
else
    echo "❌ Failed to extract career types"
    exit 1
fi

echo ""

# Step 2: Find missing templates by comparing extracted types with existing templates
echo "🔍 Step 2: Finding missing career templates..."
cd scripts
npx ts-node find_missing_templates.ts
if [ $? -eq 0 ]; then
    echo "✅ Missing templates identified successfully"
else
    echo "❌ Failed to identify missing templates"
    exit 1
fi

echo ""

# Step 3: Generate placeholder templates for any missing career types
echo "🏗️  Step 3: Generating placeholder templates..."
npx ts-node generate_placeholder_templates.ts
if [ $? -eq 0 ]; then
    echo "✅ Placeholder templates generated successfully"
else
    echo "❌ Failed to generate placeholder templates"
    exit 1
fi

# Return to root directory
cd ..

echo ""
echo "🎉 Career Template Synchronization Complete!"
echo "============================================="
echo "All career templates are now up-to-date."
echo ""
echo "Summary of actions performed:"
echo "1. ✅ Extracted latest career types from backend"
echo "2. ✅ Identified missing career templates"
echo "3. ✅ Generated placeholder templates for missing careers"
echo ""
echo "You can now review the generated templates and customize them as needed."