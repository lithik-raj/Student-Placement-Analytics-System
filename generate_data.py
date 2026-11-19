import os
import sqlite3
import random

def generate_1200_database(db_path):
    random.seed(42)
    if os.path.exists(db_path):
        os.remove(db_path)

    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Schema
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        department TEXT NOT NULL,
        year TEXT NOT NULL,
        cgpa REAL NOT NULL,
        gender TEXT NOT NULL,
        readiness_score REAL NOT NULL,
        readiness_status TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        industry TEXT NOT NULL,
        package_lpa REAL NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS placements (
        placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        company_id INTEGER,
        placement_status TEXT NOT NULL,
        placement_date TEXT,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (company_id) REFERENCES companies(company_id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT NOT NULL UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_skills (
        student_id INTEGER NOT NULL,
        skill_id INTEGER NOT NULL,
        proficiency TEXT NOT NULL,
        PRIMARY KEY (student_id, skill_id),
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
    )
    """)

    # Indexes for ultra-fast query execution
    cur.execute("CREATE INDEX IF NOT EXISTS idx_students_dept ON students(department)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_students_cgpa ON students(cgpa)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_placements_student ON placements(student_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_placements_company ON placements(company_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_student_skills_student ON student_skills(student_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_student_skills_skill ON student_skills(skill_id)")

    # 1. Companies
    companies_data = [
        (1, "Google", "Technology & Cloud", 32.5),
        (2, "Microsoft", "Software & Cloud Services", 28.0),
        (3, "Amazon", "E-Commerce & AWS", 24.0),
        (4, "Adobe", "Creative Software & Media", 22.5),
        (5, "Oracle", "Database & Enterprise Cloud", 18.0),
        (6, "Cisco", "Networking & Cyber Security", 16.5),
        (7, "JPMorgan Chase", "FinTech & Investment Banking", 14.0),
        (8, "Zoho Corporation", "SaaS & Enterprise Cloud", 12.0),
        (9, "Deloitte", "Technology Consulting", 9.0),
        (10, "Accenture", "Digital & Cloud Transformation", 8.5),
        (11, "Tata Consultancy Services (TCS)", "IT Services & Consulting", 7.5),
        (12, "Infosys", "Digital Services & Platforms", 6.5),
        (13, "L&T Technology Services", "Engineering & R&D", 6.2),
        (14, "Wipro", "IT & Business Solutions", 6.0),
        (15, "Cognizant", "Digital Solutions & Cloud", 5.8)
    ]
    cur.executemany("INSERT INTO companies (company_id, company_name, industry, package_lpa) VALUES (?, ?, ?, ?)", companies_data)

    # 2. Skills
    skills_list = [
        (1, "Python"),
        (2, "Machine Learning"),
        (3, "SQL & Database Design"),
        (4, "Deep Learning"),
        (5, "Data Structures & Algorithms"),
        (6, "React.js & Frontend"),
        (7, "Flask & REST APIs"),
        (8, "AWS & Cloud Computing"),
        (9, "Computer Vision"),
        (10, "Natural Language Processing (NLP)"),
        (11, "Docker & DevOps"),
        (12, "Java Programming"),
        (13, "C++ System Programming"),
        (14, "Cyber Security"),
        (15, "Data Analytics & PowerBI"),
        (16, "System Design")
    ]
    cur.executemany("INSERT INTO skills (skill_id, skill_name) VALUES (?, ?)", skills_list)

    # 3. Generate 1,200 Students
    first_names = [
        'Aarav', 'Aditi', 'Advait', 'Aishwarya', 'Akash', 'Amrita', 'Anand', 'Ananya', 'Aniket', 'Anjali',
        'Arjun', 'Arun', 'Arya', 'Ashwin', 'Bhavna', 'Chetan', 'Deepak', 'Devi', 'Dhruv', 'Divya',
        'Gaurav', 'Gayathri', 'Harish', 'Harini', 'Ishaan', 'Isha', 'Kalyan', 'Karthik', 'Kavya', 'Krish',
        'Lakshmi', 'Madhav', 'Manish', 'Meera', 'Manoj', 'Neha', 'Nikhil', 'Nisha', 'Nitin', 'Pallavi',
        'Pooja', 'Pranav', 'Prashant', 'Praveen', 'Preeti', 'Priya', 'Rahul', 'Rajesh', 'Rakesh', 'Ram',
        'Ramesh', 'Rhea', 'Rishi', 'Rohan', 'Rohit', 'Sanjay', 'Santosh', 'Saravanan', 'Shalini', 'Shankar',
        'Shreya', 'Shruti', 'Siddharth', 'Sneha', 'Sowmya', 'Sridhar', 'Suresh', 'Surya', 'Swathi', 'Tanvi',
        'Tarun', 'Tejas', 'Uma', 'Varun', 'Venkatesh', 'Vidyut', 'Vignesh', 'Vijay', 'Vikram', 'Vinay'
    ]

    last_names = [
        'Agarwal', 'Balaji', 'Bose', 'Chandran', 'Chawla', 'Das', 'Deshmukh', 'Dutta', 'Ganesan', 'Gupta',
        'Iyer', 'Jain', 'Joshi', 'Kapoor', 'Khan', 'Kishore', 'Krishnan', 'Kumar', 'Menon', 'Mishra',
        'Mukherjee', 'Nair', 'Nambiar', 'Patel', 'Patil', 'Pillai', 'Prasad', 'Raman', 'Rao', 'Reddy',
        'Roy', 'Saha', 'Sarin', 'Sen', 'Sethi', 'Sharma', 'Shetty', 'Singh', 'Srinivasan', 'Subramanian',
        'Sundaram', 'Thakur', 'Tripathi', 'Varma', 'Venkatesan', 'Verma', 'Yadav'
    ]

    departments = [
        ("Artificial Intelligence & Data Science", 0.22),
        ("Computer Science & Engineering", 0.28),
        ("Information Technology", 0.20),
        ("Electronics & Communication Engineering", 0.16),
        ("Electrical & Electronics Engineering", 0.08),
        ("Mechanical Engineering", 0.06)
    ]
    dept_choices = [d[0] for d in departments]
    dept_weights = [d[1] for d in departments]

    proficiencies = ["Beginner", "Intermediate", "Advanced", "Expert"]
    proficiency_weights_high = [0.05, 0.20, 0.45, 0.30]
    proficiency_weights_mid = [0.15, 0.45, 0.30, 0.10]
    proficiency_weights_low = [0.35, 0.45, 0.15, 0.05]

    prof_score_map = {
        "Beginner": 3,
        "Intermediate": 5,
        "Advanced": 8,
        "Expert": 10
    }

    students_rows = []
    placements_rows = []
    student_skills_rows = []

    # Student 1 is Lithik Raj B G
    student_1 = (
        1,
        "Lithik Raj B G",
        "lithikportal@gmail.com",
        "Artificial Intelligence & Data Science",
        "4th Year",
        9.15,
        "Male",
        98.0,
        "Elite Ready"
    )
    students_rows.append(student_1)
    placements_rows.append((1, 1, 1, "PLACED", "2026-10-15"))

    lithik_skills = [
        (1, 1, "Expert"),
        (1, 2, "Expert"),
        (1, 3, "Advanced"),
        (1, 4, "Advanced"),
        (1, 7, "Expert"),
        (1, 8, "Advanced")
    ]
    student_skills_rows.extend(lithik_skills)

    # Generate remaining 1,199 students
    generated_names = set(["Lithik Raj B G"])
    placement_id_counter = 2

    for student_id in range(2, 1201):
        while True:
            fn = random.choice(first_names)
            ln = random.choice(last_names)
            candidate = f"{fn} {ln}"
            if candidate not in generated_names:
                generated_names.add(candidate)
                name = candidate
                break

        gender = "Female" if random.random() < 0.42 else "Male"
        dept = random.choices(dept_choices, weights=dept_weights)[0]
        year = random.choice(["4th Year", "4th Year", "4th Year", "3rd Year"])
        
        # CGPA distribution: centered around 8.1, bounded between 6.0 and 9.95
        base_cgpa = random.gauss(8.15, 0.72)
        cgpa = round(max(6.10, min(9.95, base_cgpa)), 2)

        email = f"{fn.lower()}.{ln.lower()}{random.randint(10, 99)}@example.com"

        # Determine Placement probability based on CGPA and Department
        dept_placement_boost = 0.12 if "Computer" in dept or "Intelligence" in dept or "Information" in dept else 0.0
        placement_prob = min(0.96, max(0.20, ((cgpa - 6.0) / 4.0) * 0.75 + 0.20 + dept_placement_boost))
        is_placed = random.random() < placement_prob

        # Assign Company if placed
        if is_placed:
            # Super dream > 8.8, Dream 8.0-8.8, Regular 7.0-8.0, Core < 7.0
            if cgpa >= 8.85:
                # Top tech
                comp = random.choices(companies_data[:6], weights=[0.25, 0.25, 0.20, 0.15, 0.10, 0.05])[0]
            elif cgpa >= 8.10:
                comp = random.choices(companies_data[3:10], weights=[0.15, 0.20, 0.20, 0.20, 0.15, 0.05, 0.05])[0]
            elif cgpa >= 7.20:
                comp = random.choices(companies_data[7:13], weights=[0.15, 0.20, 0.25, 0.25, 0.10, 0.05])[0]
            else:
                comp = random.choices(companies_data[10:], weights=[0.25, 0.25, 0.20, 0.15, 0.15])[0]

            placement_status = "PLACED"
            month = random.randint(8, 11)
            day = random.randint(1, 28)
            placement_date = f"2026-{month:02d}-{day:02d}"
            placements_rows.append((placement_id_counter, student_id, comp[0], placement_status, placement_date))
            placement_id_counter += 1
        else:
            placement_status = "NOT PLACED"

        # Assign 3 to 6 Skills
        num_skills = random.randint(3, 6)
        if "Intelligence" in dept:
            dept_favored_skills = [1, 2, 4, 9, 10, 3, 5, 7, 15]
        elif "Computer" in dept or "Information" in dept:
            dept_favored_skills = [1, 5, 6, 7, 3, 8, 11, 12, 16]
        elif "Electronics" in dept or "Electrical" in dept:
            dept_favored_skills = [1, 13, 14, 3, 5, 8, 12, 15]
        else:
            dept_favored_skills = [1, 3, 5, 12, 15, 8, 11]

        chosen_skill_ids = random.sample(dept_favored_skills, min(num_skills, len(dept_favored_skills)))

        skill_points = 0
        for sid in chosen_skill_ids:
            if cgpa >= 8.7:
                prof = random.choices(proficiencies, weights=proficiency_weights_high)[0]
            elif cgpa >= 7.5:
                prof = random.choices(proficiencies, weights=proficiency_weights_mid)[0]
            else:
                prof = random.choices(proficiencies, weights=proficiency_weights_low)[0]

            student_skills_rows.append((student_id, sid, prof))
            skill_points += prof_score_map[prof]

        # Calculate Readiness Score: (CGPA * 4) + (min(40, skill_points)) + (20 if placed else 10)
        cgpa_score = (cgpa / 10.0) * 40.0
        norm_skill_score = min(40.0, (skill_points / 45.0) * 40.0)
        status_score = 20.0 if is_placed else 10.0
        total_readiness = round(min(100.0, cgpa_score + norm_skill_score + status_score), 1)

        if total_readiness >= 85.0:
            readiness_status = "Elite Ready"
        elif total_readiness >= 72.0:
            readiness_status = "Job Ready"
        elif total_readiness >= 55.0:
            readiness_status = "Developing"
        else:
            readiness_status = "Needs Upskilling"

        students_rows.append((
            student_id,
            name,
            email,
            dept,
            year,
            cgpa,
            gender,
            total_readiness,
            readiness_status
        ))

    # Bulk insert
    cur.executemany("""
    INSERT INTO students (student_id, name, email, department, year, cgpa, gender, readiness_score, readiness_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, students_rows)

    cur.executemany("""
    INSERT INTO placements (placement_id, student_id, company_id, placement_status, placement_date)
    VALUES (?, ?, ?, ?, ?)
    """, placements_rows)

    cur.executemany("""
    INSERT INTO student_skills (student_id, skill_id, proficiency)
    VALUES (?, ?, ?)
    """, student_skills_rows)

    conn.commit()
    conn.close()
    print(f"Successfully generated database at {db_path} with {len(students_rows)} students, {len(placements_rows)} placements, and {len(student_skills_rows)} skill mappings.")

if __name__ == "__main__":
    db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "placement_analytics.db")
    generate_1200_database(db_file)
