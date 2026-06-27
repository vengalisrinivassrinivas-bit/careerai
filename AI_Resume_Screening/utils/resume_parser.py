import re
from typing import Dict, List, Any

# Define lists of common skills for dictionary lookup
TECHNICAL_SKILL_POOL = [
    # Programming Languages
    "python", "java", "c++", "c#", "javascript", "typescript", "ruby", "golang", "rust", "php", "swift", "kotlin", "scala", "r language", "perl", "bash", "shell", "sql", "pl/sql", "nosql",
    # Libraries / Frameworks
    "django", "flask", "fastapi", "spring boot", "hibernate", "react", "angular", "vue", "nodejs", "express", "jquery", "bootstrap", "tailwind", "laravel", "dotnet", "asp.net", "entity framework",
    # Data Science / ML
    "machine learning", "deep learning", "nlp", "natural language processing", "computer vision", "neural networks", "statistics", "probability", "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch", "opencv", "nltk", "spacy", "matplotlib", "seaborn", "tableau", "power bi", "excel", "data analysis", "data science",
    # Big Data / ETL
    "hadoop", "spark", "apache spark", "hive", "pig", "hdfs", "etl", "informatica", "talend", "data warehousing", "dbt",
    # DevOps / Cloud
    "docker", "kubernetes", "aws", "amazon web services", "azure", "gcp", "google cloud", "jenkins", "git", "github", "gitlab", "terraform", "ansible", "ci/cd", "linux", "unix", "bash scripting", "prometheus", "grafana", "nginx",
    # Security / Networking
    "firewall", "cybersecurity", "information security", "vpn", "cisco", "wireshark", "cryptography", "active directory", "dns", "dhcp",
    # Other Tools / Concepts
    "jira", "confluence", "scrum", "agile", "sap", "abap", "salesforce", "crm", "figma", "ui/ux", "wordpress", "smart contracts", "solidity", "ethereum", "blockchain"
]

SOFT_SKILL_POOL = [
    "communication", "leadership", "teamwork", "collaboration", "problem solving", "time management", 
    "adaptability", "critical thinking", "creativity", "interpersonal skills", "emotional intelligence", 
    "negotiation", "presentation", "organization", "active listening", "decision making", "conflict resolution",
    "work ethic", "public speaking", "project management"
]

def parse_resume(text: str) -> Dict[str, Any]:
    """
    Parses resume text using regular expressions and dictionary matching to extract candidate info.
    
    Args:
        text (str): Raw text extracted from the PDF resume.
        
    Returns:
        Dict[str, Any]: Dictionary containing Name, Email, Phone, Education, Experience,
                        Certifications, Projects, Tech Skills, Soft Skills, and All Skills.
    """
    parsed_info = {
        "name": "Not Found",
        "email": "Not Found",
        "phone": "Not Found",
        "education": [],
        "experience": [],
        "certifications": [],
        "projects": [],
        "tech_skills": [],
        "soft_skills": [],
        "all_skills": []
    }
    
    if not text:
        return parsed_info
        
    # Split text into lines for line-by-line processing
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # 1. Email Extraction
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    if emails:
        parsed_info["email"] = emails[0]
        
    # 2. Phone Number Extraction
    phone_pattern = r'(?:\+?\d{1,3}[\s-]?)?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{4}'
    phones = re.findall(phone_pattern, text)
    if phones:
        # Avoid matching years like 2018-2022 as phone numbers
        valid_phones = [p for p in phones if len(re.sub(r'\D', '', p)) >= 10]
        if valid_phones:
            parsed_info["phone"] = valid_phones[0]
            
    # 3. Name Extraction Heuristics
    # Look at the first 5 lines of the resume. Name is usually in the first few lines.
    ignored_keywords = ["resume", "curriculum", "vitae", "cv", "contact", "email", "phone", "profile", "summary", "address", "portfolio"]
    name_found = False
    for line in lines[:5]:
        # Ignore lines with digits, emails, URLs, or specific ignored keywords
        if (re.search(r'\d', line) or 
            "@" in line or 
            "http" in line or 
            "/" in line or
            any(kw in line.lower() for kw in ignored_keywords)):
            continue
            
        # Clean potential prefix like "Name:" or "Candidate:"
        cleaned_line = re.sub(r'^(name|candidate|fullname|full name)\s*:\s*', '', line, flags=re.IGNORECASE).strip()
        
        # A name usually consists of 2-3 words, capitalized
        words = cleaned_line.split()
        if 2 <= len(words) <= 4 and all(w[0].isupper() if w[0].isalpha() else True for w in words):
            parsed_info["name"] = cleaned_line
            name_found = True
            break
            
    # Fallback name extraction from email if not found
    if not name_found and parsed_info["email"] != "Not Found":
        email_prefix = parsed_info["email"].split('@')[0]
        # E.g. john.doe -> John Doe
        cleaned_email_name = email_prefix.replace('.', ' ').replace('_', ' ').title()
        # Remove digits from name
        cleaned_email_name = re.sub(r'\d+', '', cleaned_email_name).strip()
        if len(cleaned_email_name) > 3:
            parsed_info["name"] = cleaned_email_name
            
    # 4. Skills Extraction (Lookup via pools)
    text_lower = text.lower()
    
    # Extract Technical Skills
    found_tech = []
    for skill in TECHNICAL_SKILL_POOL:
        # Match using word boundaries. Handle special symbols like C++, C#, .NET
        escaped_skill = re.escape(skill)
        # Custom boundaries for C++, C#, .NET
        if skill in ["c++", "c#", ".net"]:
            pattern = r'(?:\b|(?<=\s))' + escaped_skill + r'(?:\b|(?=\s))'
        else:
            pattern = r'\b' + escaped_skill + r'\b'
            
        if re.search(pattern, text_lower):
            # Format nicely
            display_name = skill.upper() if len(skill) <= 4 else skill.title()
            # Custom mappings for better formatting
            custom_formats = {
                "C++": "C++", "C#": "C#", "Sql": "SQL", "Nosql": "NoSQL", 
                "Django": "Django", "Flask": "Flask", "Fastapi": "FastAPI",
                "Spring Boot": "Spring Boot", "Nodejs": "Node.js", "Dotnet": ".NET", 
                "Asp.net": "ASP.NET", "Nlp": "NLP", "Ui/ux": "UI/UX", "Aws": "AWS", 
                "Gcp": "GCP", "Etl": "ETL", "Crm": "CRM", "Hdfs": "HDFS",
                "Api": "API", "Html": "HTML", "Css": "CSS", "Xml": "XML", "Js": "JavaScript"
            }
            formatted_skill = custom_formats.get(display_name, display_name)
            found_tech.append(formatted_skill)
            
    parsed_info["tech_skills"] = sorted(list(set(found_tech)))
    
    # Extract Soft Skills
    found_soft = []
    for skill in SOFT_SKILL_POOL:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_soft.append(skill.title())
            
    parsed_info["soft_skills"] = sorted(list(set(found_soft)))
    
    parsed_info["all_skills"] = sorted(list(set(parsed_info["tech_skills"] + parsed_info["soft_skills"])))
    
    # 5. Section Extraction (Education, Experience, Certifications, Projects)
    # Define keywords for section identification
    section_keywords = {
        "education": ["education", "academic profile", "qualification", "academic background", "scholastic"],
        "experience": ["experience", "work history", "employment", "professional background", "internship", "work experience"],
        "certifications": ["certification", "certifications", "credentials", "licenses", "courses"],
        "projects": ["project", "projects", "academic projects", "personal projects", "key projects"]
    }
    
    # Categorize lines based on containing keywords
    current_section = None
    for line in lines:
        line_lower = line.lower()
        
        # Check if line marks a section header
        header_detected = False
        for sec, keywords in section_keywords.items():
            # Section headers are usually short (under 4 words)
            if len(line.split()) <= 4 and any(re.search(r'\b' + re.escape(kw) + r'\b', line_lower) for kw in keywords):
                current_section = sec
                header_detected = True
                break
                
        if header_detected:
            continue
            
        # Add content lines to the active section
        if current_section:
            # Clean formatting symbols (bullets, hyphens)
            cleaned_val = re.sub(r'^[\s\-\*•o➢]+', '', line).strip()
            # Only add lines of reasonable length and content
            if cleaned_val and len(cleaned_val) > 10:
                parsed_info[current_section].append(cleaned_val)
                
    # Deduplicate section arrays and limit length for clean UI presentation
    for sec in ["education", "experience", "certifications", "projects"]:
        parsed_info[sec] = list(dict.fromkeys(parsed_info[sec]))[:10]  # Max 10 entries to prevent overflow
        
    return parsed_info
