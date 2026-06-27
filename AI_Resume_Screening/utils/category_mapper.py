# Maps raw Kaggle dataset categories to student-friendly and professional titles.

CATEGORY_MAP = {
    "Data Science": "Data Scientist",
    "HR": "Human Resources (HR) Specialist",
    "Advocate": "Legal Counsel / Advocate",
    "Arts": "Graphic Designer / Creative Artist",
    "Web Designing": "Web Designer & Frontend Developer",
    "Mechanical Engineer": "Mechanical Engineer",
    "Sales": "Sales & Business Development Associate",
    "Health and fitness": "Fitness Trainer & Nutrition Consultant",
    "Civil Engineer": "Civil Engineer",
    "Java Developer": "Java Software Engineer",
    "Business Analyst": "Business Analyst",
    "SAP Developer": "SAP Consultant & ABAP Developer",
    "Automation Testing": "QA Automation Engineer",
    "Electrical Engineering": "Electrical Engineer",
    "Operations Manager": "Operations & Supply Chain Manager",
    "Python Developer": "Python Developer",
    "DevOps Engineer": "DevOps & Cloud Engineer",
    "Network Security Engineer": "Network & Cyber Security Engineer",
    "PMO": "Project Management Officer (PMO)",
    "Database": "Database Administrator (DBA)",
    "Hadoop": "Big Data Engineer (Hadoop/Spark)",
    "ETL Developer": "ETL & Data Integration Developer",
    "DotNet Developer": ".NET Software Developer",
    "Blockchain": "Blockchain Developer",
    "Testing": "QA manual Software Tester"
}

def get_clean_category(raw_category: str) -> str:
    """
    Returns the student-friendly display name for a raw dataset category.
    If the category is not mapped, returns it title-cased.
    
    Args:
        raw_category (str): The raw output category from the ML model.
        
    Returns:
        str: User-friendly professional job role title.
    """
    if not isinstance(raw_category, str):
        return "Unknown Role"
    
    # Strip whitespace and check map (case-insensitive key match)
    cleaned_key = raw_category.strip()
    
    # Try direct lookup
    if cleaned_key in CATEGORY_MAP:
        return CATEGORY_MAP[cleaned_key]
        
    # Check case-insensitive key search
    for k, v in CATEGORY_MAP.items():
        if k.lower() == cleaned_key.lower():
            return v
            
    return cleaned_key.title()
