#!/usr/bin/env python3
"""
Check why product roles aren't being included in filtering
"""

from comprehensive_careers import COMPREHENSIVE_CAREERS, get_careers_by_experience_level, get_careers_by_salary_range

def check_product_role_filtering():
    # Check what product roles exist in the database
    product_roles = []
    for career in COMPREHENSIVE_CAREERS:
        title = career.get('title', '')
        if any(keyword in title.lower() for keyword in ['product manager', 'product lead', 'head of product', 'vp product', 'chief product officer', 'director of product']):
            product_roles.append({
                'title': title,
                'experience': career.get('experienceLevel'),
                'salary_min': career.get('minSalary'),
                'salary_max': career.get('maxSalary')
            })

    print(f'Found {len(product_roles)} product roles in database:')
    for role in product_roles:
        print(f'  {role["title"]} - {role["experience"]} - ${role["salary_min"]:,}-${role["salary_max"]:,}')

    print()

    # Check filtering for 7 years experience, 120k-180k salary
    experience_filtered = get_careers_by_experience_level(7)
    salary_filtered = get_careers_by_salary_range(120000, 180000)

    print(f'Experience filtered (7 years): {len(experience_filtered)} careers')
    print(f'Salary filtered (120k-180k): {len(salary_filtered)} careers')

    # Get intersection
    filtered_careers = [career for career in experience_filtered if career in salary_filtered]
    print(f'Both filters: {len(filtered_careers)} careers')

    # Check which product roles pass filtering
    filtered_product_roles = []
    for career in filtered_careers:
        title = career.get('title', '')
        if any(keyword in title.lower() for keyword in ['product manager', 'product lead', 'head of product', 'vp product', 'chief product officer', 'director of product']):
            filtered_product_roles.append(title)

    print(f'Product roles after filtering: {len(filtered_product_roles)}')
    for title in filtered_product_roles:
        print(f'  {title}')

    # Check why other product roles are filtered out
    print('\nProduct roles filtered out:')
    for role in product_roles:
        title = role['title']
        if title not in filtered_product_roles:
            exp_match = any(career.get('title') == title for career in experience_filtered)
            sal_match = any(career.get('title') == title for career in salary_filtered)
            print(f'  {title} - exp_match: {exp_match}, sal_match: {sal_match}')

if __name__ == "__main__":
    check_product_role_filtering()