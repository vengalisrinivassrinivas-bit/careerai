import os
import urllib.request
import pandas as pd

def download_dataset():
    print("Downloading UpdatedResumeDataSet.csv...")
    url = "https://raw.githubusercontent.com/611noorsaeed/Resume-Screening-App/main/UpdatedResumeDataSet.csv"
    os.makedirs("AI_Resume_Screening/data", exist_ok=True)
    target_path = "AI_Resume_Screening/data/UpdatedResumeDataSet.csv"
    
    try:
        # Download file using urllib
        urllib.request.urlretrieve(url, target_path)
        print(f"Successfully downloaded dataset to {target_path}")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        # Fallback empty dataframe creation if download fails, but GitHub raw should work
        raise e

def generate_skills_dataset():
    print("Generating skills_dataset.csv...")
    # Define mapping of category -> required skills
    skills_map = {
        "Data Science": "Python, Machine Learning, Deep Learning, SQL, R, Statistics, Tableau, Pandas, NumPy, Scikit-learn, TensorFlow, Keras, Git",
        "HR": "Human Resources, Recruitment, Employee Relations, Payroll, Performance Management, Onboarding, ATS, HRIS, Communication, Interviewing",
        "Advocate": "Legal Writing, Corporate Law, Litigation, Legal Research, Contract Drafting, Dispute Resolution, Constitutional Law, Negotiation",
        "Arts": "Graphic Design, Adobe Photoshop, Illustrator, Fine Arts, Creative Writing, UI/UX, Photography, Figma, Drawing, Visual Communication",
        "Web Designing": "HTML, CSS, JavaScript, Bootstrap, jQuery, WordPress, UI/UX, Figma, Responsive Design, Adobe XD, Web Design",
        "Mechanical Engineer": "AutoCAD, SolidWorks, Thermodynamics, MATLAB, Fluid Mechanics, CAD, CAM, Project Engineering, Manufacturing, ANSYS",
        "Sales": "Salesforce, Negotiation, Account Management, Business Development, B2B Sales, Cold Calling, CRM, Lead Generation, Customer Relations",
        "Health and fitness": "Nutrition, Personal Training, Wellness, Anatomy, Kinesiology, CPR Certified, Fitness Coaching, Diet Planning, Health Education",
        "Civil Engineer": "AutoCAD, Civil 3D, Structural Analysis, Revit, Project Management, Concrete Design, Estimation, Site Supervision, Surveying",
        "Java Developer": "Java, Spring Boot, Hibernate, SQL, Microservices, Maven, REST APIs, Git, JUnit, Docker, AWS, Multithreading",
        "Business Analyst": "Business Analysis, SQL, Agile, Scrum, Requirements Gathering, Jira, Tableau, Power BI, Excel, UML, Process Mapping",
        "SAP Developer": "SAP ABAP, SAP HANA, SAP ERP, SAP FI/CO, SAP SD, SQL, SAP NetWeaver, Debugging, BAPI, IDoc",
        "Automation Testing": "Selenium, Java, Python, TestNG, Cucumber, Jenkins, Maven, SQL, Automation Testing, Git, QA, API Testing, Postman",
        "Electrical Engineering": "MATLAB, Circuit Design, AutoCAD, PLC Programming, Power Systems, Microcontrollers, LabVIEW, Electrical Wiring, Control Systems",
        "Operations Manager": "Operations Management, Supply Chain, Logistics, Project Management, Process Improvement, Budgeting, Leadership, Vendor Management",
        "Python Developer": "Python, Django, Flask, FastAPI, SQL, PostgreSQL, REST APIs, Git, Docker, Pandas, AWS, Object Oriented Programming",
        "DevOps Engineer": "Docker, Kubernetes, AWS, Jenkins, Linux, CI/CD, Git, Terraform, Ansible, Python, Bash, Shell Scripting, Monitoring",
        "Network Security Engineer": "Cisco, Networking, Firewall, Cybersecurity, TCP/IP, VPN, Wireshark, Information Security, Routing & Switching, Active Directory",
        "PMO": "Project Management, Agile, Scrum, MS Project, Budgeting, Risk Management, PMO Governance, Stakeholder Management, Reporting",
        "Database": "SQL, Oracle Database, SQL Server, MySQL, Database Administration, Performance Tuning, Backup & Recovery, ETL, PL/SQL",
        "Hadoop": "Hadoop, MapReduce, HDFS, Apache Spark, Hive, Pig, Big Data, Scala, Python, NoSQL, Linux",
        "ETL Developer": "ETL, Informatica, SQL, Data Warehousing, SSIS, Talend, PL/SQL, Data Integration, Star Schema, Database Design",
        "DotNet Developer": "C#, .NET Core, ASP.NET MVC, SQL Server, Entity Framework, Web API, JavaScript, Git, IIS, REST APIs",
        "Blockchain": "Blockchain, Solidity, Smart Contracts, Ethereum, Cryptography, Go, Rust, Web3.js, Hyperledger, Node.js",
        "Testing": "Manual Testing, Software Development Life Cycle, Test Cases, Bug Tracking, QA, Jira, Test Planning, Regression Testing"
    }
    
    data = []
    for category, skills in skills_map.items():
        data.append({"Category": category, "Skills": skills})
        
    df = pd.DataFrame(data)
    df.to_csv("AI_Resume_Screening/data/skills_dataset.csv", index=False)
    print("skills_dataset.csv generated successfully.")

def generate_projects_dataset():
    print("Generating projects_dataset.csv...")
    projects_list = [
        # Data Science
        ("Data Science", "Customer Churn Prediction", "Predict client churn risk using Logistic Regression, Pandas, and Scikit-Learn.", "Medium"),
        ("Data Science", "Movie Recommendation Engine", "Collaborative and content-based recommendation system using Cosine Similarity.", "Medium"),
        ("Data Science", "Heart Disease Classification", "Classify cardiac health indicators utilizing Random Forest classifier.", "Hard"),
        # HR
        ("HR", "Automated Employee Onboarding Portal", "System to streamline documents and onboarding flows for HR.", "Medium"),
        ("HR", "Performance Appraisal Dashboard", "Interactive dashboard to record, visualize, and track employee performance KPIs.", "Easy"),
        ("HR", "Candidate ATS Pipeline tracker", "Tool to manage recruitment stages and filter resumes by keywords.", "Medium"),
        # Advocate
        ("Advocate", "Legal Case Management System", "Tracks court dates, client briefs, and case documents.", "Medium"),
        ("Advocate", "Contract Lifecycle Analyzer", "Automated document parser to search and flag specific clauses in legal agreements.", "Hard"),
        # Arts
        ("Arts", "Digital Portfolio Web Application", "Highly responsive, visual portfolio builder to show art work.", "Easy"),
        ("Arts", "Interactive Typography Guide", "Web educational tool demonstrating historical typography styles.", "Medium"),
        # Web Designing
        ("Web Designing", "E-commerce Front-end Dashboard", "A fully responsive glassmorphic checkout UI and product grid.", "Medium"),
        ("Web Designing", "Personal Branding Portfolio Portal", "Premium, interactive dark-mode portfolio utilizing CSS animations.", "Easy"),
        # Mechanical Engineer
        ("Mechanical Engineer", "CAD Heat Sink Simulator", "Simulate heat dissipation of electronic components in Autodesk/SolidWorks.", "Hard"),
        ("Mechanical Engineer", "3D Printing Tolerance Calculator", "App to calculate mechanical fit tolerances based on print temperature.", "Medium"),
        # Sales
        ("Sales", "Sales CRM & Pipeline Tracker", "Visual dashboard showing lead scoring, conversion funnels, and CRM records.", "Medium"),
        ("Sales", "Automated Email Follow-up Bot", "Sends sequential emails based on lead actions.", "Easy"),
        # Health and fitness
        ("Health and fitness", "Macro Nutrition Planner", "Calculates body fat, BMR, and constructs diet sheets.", "Easy"),
        ("Health and fitness", "Gym Workout Tracking App", "Saves workout templates, counts sets/reps, and shows progress graphs.", "Medium"),
        # Civil Engineer
        ("Civil Engineer", "Beam Deflection Calculator", "Calculates structural load distribution on concrete beams.", "Medium"),
        ("Civil Engineer", "Construction Project Estimator", "App to estimate bill of materials (BOM) based on blueprints.", "Easy"),
        # Java Developer
        ("Java Developer", "Secure Banking REST API", "Spring Boot microservice with JWT authentication and MySQL backend.", "Hard"),
        ("Java Developer", "Task Management Microservice", "Containerized Java Spring application with Docker and Postgres.", "Medium"),
        ("Java Developer", "Inventory Management System", "Java Swing desktop application using JDBC to connect to database.", "Easy"),
        # Business Analyst
        ("Business Analyst", "Market Trend Dashboard", "Tableau/Power BI mockup analyzing customer retention patterns.", "Easy"),
        ("Business Analyst", "Agile Velocity Calculator", "Saves sprint metrics and predicts project delivery timelines.", "Medium"),
        # SAP Developer
        ("SAP Developer", "ABAP Report Generator", "Custom SAP report extracting billing records with specific transaction codes.", "Medium"),
        ("SAP Developer", "BAPI Purchase Order Creator", "Module integrating external purchases with SAP core ERP.", "Hard"),
        # Automation Testing
        ("Automation Testing", "E-Commerce E2E Selenium Suite", "Automation testing suite verifying search-to-checkout flows.", "Medium"),
        ("Automation Testing", "REST API Automated Test Suite", "Postman / RestAssured test pipeline checking status codes and payloads.", "Easy"),
        # Electrical Engineering
        ("Electrical Engineering", "Solar Power Grid Optimizer", "MATLAB simulation optimizing solar cell angle and storage levels.", "Hard"),
        ("Electrical Engineering", "Arduino Smart Home System", "Microcontroller-based automation controlling lights and temp sensors.", "Medium"),
        # Operations Manager
        ("Operations Manager", "Supply Chain Inventory Tracker", "Warehouse dashboard displaying safety stock thresholds and EOQ.", "Medium"),
        ("Operations Manager", "Vendor Scorecard Evaluator", "Records vendor delivery times, quality rates, and calculates rating.", "Easy"),
        # Python Developer
        ("Python Developer", "Real-time Weather Dashboard", "FastAPI app querying external APIs and serving a frontend with visual charts.", "Medium"),
        ("Python Developer", "Asynchronous Web Scraper", "Scrapes e-commerce sites using HTTPX and BeautifulSoup, saving to PostgreSQL.", "Hard"),
        ("Python Developer", "CLI Task Manager", "Simple CRUD application saving lists to JSON files using argparse.", "Easy"),
        # DevOps Engineer
        ("DevOps Engineer", "Multi-stage CI/CD Jenkins Pipeline", "Deploys Python application to AWS ECS with unit tests and lint checks.", "Hard"),
        ("DevOps Engineer", "Terraform Infrastructure as Code", "Provisions VPC, Subnets, and EC2 instances on AWS cloud dynamically.", "Medium"),
        ("DevOps Engineer", "Kubernetes Local Cluster Setup", "Configures Minikube clusters with Ingress Controller and Persistent Volumes.", "Hard"),
        # Network Security Engineer
        ("Network Security Engineer", "Intrusion Detection System (IDS)", "Python-based network packet sniffer detecting SQL injection attempts.", "Hard"),
        ("Network Security Engineer", "Automated Network Port Scanner", "Scans local ports using Nmap wrapper and generates HTML report.", "Medium"),
        # PMO
        ("PMO", "Sprint Resource Planner", "Calculates team bandwidth and capacity during sprint scheduling.", "Easy"),
        ("PMO", "Project Risk Assessment Matrix", "Maps likelihood vs impact of project risks with mitigation logs.", "Medium"),
        # Database
        ("Database", "Database Schema Migrator Tool", "Custom SQL Server/MySQL schema comparison and migration script.", "Hard"),
        ("Database", "Database Slow Query Analyzer", "Extracts, parses, and formats query execution logs for indexing.", "Medium"),
        # Hadoop
        ("Hadoop", "Log File Sentiment Spark Job", "HDFS batch job calculating message sentiment from cluster logs.", "Hard"),
        ("Hadoop", "MapReduce Word Frequency Counter", "Classic Big Data batch processor counting word frequencies on HDFS.", "Medium"),
        # ETL Developer
        ("ETL Developer", "CSV to Redshift Pipeline", "AWS Glue job extracting files, transformations, loading to warehouse.", "Hard"),
        ("ETL Developer", "API Data Integration Script", "Extracts JSON responses daily and saves as structured parquet files.", "Medium"),
        # DotNet Developer
        ("DotNet Developer", "ASP.NET Core Web API", "Web service with JWT auth, Entity Framework Core, and SQL Server.", "Medium"),
        ("DotNet Developer", "Real-time Chat App using SignalR", "Websocket communication service built with .NET Core and HTML.", "Hard"),
        # Blockchain
        ("Blockchain", "ERC20 Token Smart Contract", "Solidity contract deployed on Ethereum local network with unit tests.", "Medium"),
        ("Blockchain", "Decentralized Voting DApp", "React frontend talking to Solidity smart contracts via Web3.js.", "Hard"),
        # Testing
        ("Testing", "Manual Regression Test Library", "Structured spreadsheet-to-web test plan tracking cases and results.", "Easy"),
        ("Testing", "API Payload Schema Validator", "Python script validating JSON response schema matching definition.", "Medium")
    ]
    
    # Fill in any missing categories with default projects
    all_categories = [
        "Data Science", "HR", "Advocate", "Arts", "Web Designing", "Mechanical Engineer", "Sales",
        "Health and fitness", "Civil Engineer", "Java Developer", "Business Analyst", "SAP Developer",
        "Automation Testing", "Electrical Engineering", "Operations Manager", "Python Developer",
        "DevOps Engineer", "Network Security Engineer", "PMO", "Database", "Hadoop", "ETL Developer",
        "DotNet Developer", "Blockchain", "Testing"
    ]
    
    existing_categories = set(p[0] for p in projects_list)
    for cat in all_categories:
        if cat not in existing_categories:
            projects_list.append((cat, f"{cat} Automation System", f"Custom automated tool for managing {cat} pipelines.", "Medium"))
            projects_list.append((cat, f"{cat} Web Portal", f"Information portal detailing {cat} principles and guidelines.", "Easy"))
            projects_list.append((cat, f"{cat} Analytics Dashboard", f"Power BI/Tableau dashboard analyzing industry trends.", "Hard"))
            
    df = pd.DataFrame(projects_list, columns=["Category", "Project_Name", "Description", "Difficulty"])
    df.to_csv("AI_Resume_Screening/data/projects_dataset.csv", index=False)
    print("projects_dataset.csv generated successfully.")

def generate_interview_questions_dataset():
    print("Generating interview_questions.csv...")
    questions = []
    
    # Template bank for categories
    qa_templates = {
        "Data Science": [
            ("Technical", "Easy", "What is the difference between supervised and unsupervised learning?"),
            ("Technical", "Medium", "What is overfitting and how can you prevent it?"),
            ("Technical", "Hard", "Explain how the Transformer architecture and Self-Attention mechanism work."),
            ("Coding", "Easy", "Write a Python function to reverse a string without using built-in reverse functions."),
            ("Coding", "Medium", "Write a function to find the duplicate elements in an array in O(N) time."),
            ("Coding", "Hard", "Write code to implement a K-Means clustering algorithm from scratch in Python."),
            ("HR", "Easy", "Why did you choose Data Science as a career choice?"),
            ("HR", "Medium", "Describe a time when you had to explain a complex ML model to a non-technical stakeholder.")
        ],
        "Python Developer": [
            ("Technical", "Easy", "What are PEP 8 guidelines and why are they important?"),
            ("Technical", "Medium", "What is the difference between lists and tuples in Python? Explain memory layout."),
            ("Technical", "Hard", "How does Python's Global Interpreter Lock (GIL) work and how do you bypass it?"),
            ("Coding", "Easy", "Write a Python list comprehension that filters even numbers from a list."),
            ("Coding", "Medium", "Implement a Python decorator that logs the execution time of any function."),
            ("Coding", "Hard", "Write a custom generator to yield prime numbers infinitely, optimized using Sieve of Eratosthenes."),
            ("HR", "Easy", "What interests you about Python web development or automation?"),
            ("HR", "Medium", "How do you keep yourself updated with the latest Python features and pep guidelines?")
        ],
        "Java Developer": [
            ("Technical", "Easy", "What are the OOP principles in Java?"),
            ("Technical", "Medium", "Explain Java Garbage Collection and memory management (Heap vs Stack)."),
            ("Technical", "Hard", "What is the difference between Synchronized blocks and Lock API in multithreading?"),
            ("Coding", "Easy", "Write a Java program to reverse a linked list."),
            ("Coding", "Medium", "Write a Java program to find the second largest element in an array using Streams."),
            ("Coding", "Hard", "Implement a thread-safe Singleton class in Java without using synchronized keyword on method."),
            ("HR", "Easy", "What Java frameworks (Spring Boot, Hibernate) are you most comfortable with?"),
            ("HR", "Medium", "How do you handle disagreement with a tech lead on application architecture?")
        ],
        "DevOps Engineer": [
            ("Technical", "Easy", "What is CI/CD and why is it important in software development?"),
            ("Technical", "Medium", "Explain the difference between virtual machines and Docker containers."),
            ("Technical", "Hard", "How does Kubernetes handle self-healing of containers? Explain pod lifecycle."),
            ("Coding", "Easy", "Write a Bash script to backup a folder and email a status report if it fails."),
            ("Coding", "Medium", "Write a Python script to monitor CPU utilization and raise an alert if it exceeds 90%."),
            ("Coding", "Hard", "Write a complete declarative Jenkins pipeline that builds, tests, and deploys a Docker image."),
            ("HR", "Easy", "What challenges do you enjoy solving in automated infrastructure management?"),
            ("HR", "Medium", "How do you manage production downtime during a release deployment failure?")
        ],
        "Network Security Engineer": [
            ("Technical", "Easy", "What is the difference between HTTP and HTTPS?"),
            ("Technical", "Medium", "Explain how a 3-way TCP handshake works during a connection request."),
            ("Technical", "Hard", "How does a Man-in-the-Middle (MITM) attack intercept SSL traffic, and how does HSTS mitigate it?"),
            ("Coding", "Easy", "Write a Python script using socket to check if port 80 is open on a target host."),
            ("Coding", "Medium", "Write a regular expression to validate an IPv4 address string."),
            ("Coding", "Hard", "Write a Python packet sniffer using scapy to count incoming SYN packets to detect scan attacks."),
            ("HR", "Easy", "Why are you interested in cyber and network security?"),
            ("HR", "Medium", "How do you balance user experience/speed with strict network security policies?")
        ]
    }
    
    # Generic templates to fallback for other categories
    generic_templates = [
        ("Technical", "Easy", "What is the primary objective of your role in this domain?"),
        ("Technical", "Medium", "What tools and frameworks do you use daily in this domain?"),
        ("Technical", "Hard", "What are the common bottleneck issues in this field and how do you solve them?"),
        ("Coding", "Easy", "Write a simple program/script to parse a config file in this domain."),
        ("Coding", "Medium", "Write an algorithm to sort elements according to domain metadata metrics."),
        ("Coding", "Hard", "Write a secure token validation script to authorize API clients in this domain."),
        ("HR", "Easy", "Tell me about yourself and your background in this domain."),
        ("HR", "Medium", "Describe a challenging project you did in this category and how you resolved the hurdles.")
    ]
    
    all_categories = [
        "Data Science", "HR", "Advocate", "Arts", "Web Designing", "Mechanical Engineer", "Sales",
        "Health and fitness", "Civil Engineer", "Java Developer", "Business Analyst", "SAP Developer",
        "Automation Testing", "Electrical Engineering", "Operations Manager", "Python Developer",
        "DevOps Engineer", "Network Security Engineer", "PMO", "Database", "Hadoop", "ETL Developer",
        "DotNet Developer", "Blockchain", "Testing"
    ]
    
    for category in all_categories:
        templates = qa_templates.get(category, generic_templates)
        # Duplicate or adjust template list if it's too short, ensuring we get plenty of questions
        for q_type, difficulty, question in templates:
            questions.append({
                "Category": category,
                "Question_Type": q_type,
                "Difficulty": difficulty,
                "Question": question
            })
            
    df = pd.DataFrame(questions)
    df.to_csv("AI_Resume_Screening/data/interview_questions.csv", index=False)
    print("interview_questions.csv generated successfully.")

if __name__ == "__main__":
    download_dataset()
    generate_skills_dataset()
    generate_projects_dataset()
    generate_interview_questions_dataset()
    print("All datasets set up successfully!")
