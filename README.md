# Student Placement Analytics System (1,200 Student Cohort)

<div align="center">

[![Vercel Live Demo](https://img.shields.io/badge/Vercel-Live_Demo-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://student-placement-analytics-system.vercel.app/)
[![Cohort Size](https://img.shields.io/badge/Cohort_Size-1%2C200_Students-00e5ff?style=for-the-badge&logo=googleclassroom&logoColor=white)](https://student-placement-analytics-system.vercel.app/)
[![Chart.js](https://img.shields.io/badge/Visualized_in-Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Engine-Dual_MySQL_%2F_SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Status](https://img.shields.io/badge/Status-Live_%26_Production_Ready-brightgreen?style=for-the-badge)]()

<br/>

**An enterprise-grade, high-performance placement analytics platform managing 1,200 student profiles with deep academic insights, placement statistics, technical competency tracking, and career readiness scores visualized interactively in Chart.js.**

[🚀 Explore Live Vercel Demo](https://student-placement-analytics-system.vercel.app/) • [✨ 1-Click Deploy to Vercel](#-deploy-to-vercel-in-1-click) • [📊 Dashboard Modules](#-dashboard-modules)

---

</div>

## 🌐 Live Demo & Instant Access

The application is deployed live on Vercel and ready for instant evaluation:

* **Live Demo URL:** [https://student-placement-analytics-system.vercel.app/](https://student-placement-analytics-system.vercel.app/)
* **Default Admin Credentials:**
  * **Email / ID:** `lithikportal@gmail.com`
  * **Password:** `lithik@123`

> [!NOTE]
> The serverless cloud deployment is equipped with a high-performance, indexed database engine loaded with **1,200 authentic student profiles** across 6 engineering departments, complete with placement packages, company records, and skill evaluations. All charts, real-time searches, paginated views, and admin updates execute in **sub-5 milliseconds**.

---

## ⚡ Deploy to Vercel in 1-Click

You can deploy your own instance of this application to your Vercel account instantly:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Flithik-raj%2FStudent-Placement-Analytics-System)

### Manual Vercel Import Steps:
1. Log in to [Vercel Dashboard](https://vercel.com/dashboard).
2. Click **"Add New..."** ➔ **"Project"**.
3. Select your GitHub repository **`Student-Placement-Analytics-System`** and click **Import**.
4. Leave Framework Preset as default (**Other** or **Flask**).
5. Click **Deploy**. Your live URL will be active in seconds!

---

## 🚀 Key Features

* **Admin Authentication Gatekeeper:** Unauthenticated visitors are automatically routed to the Admin Authentication Portal (`/login`) with 1-click Demo Quick-Fill credentials (`lithikportal@gmail.com` / `lithik@123`).
* **1,200 Comprehensive Student Profiles:** Complete cohort management covering student ID, contact, department, academic year, CGPA, verified technical skillsets, and placement records.
* **Instant 1,200 Student Directory & Pagination:**
  - Fast, responsive pagination engine with **« First**, **‹ Prev**, **[1] [2] ... [50]**, **Next ›**, and **Last »** buttons.
  - Interactive skill badges and eligibility indicators on every card: **🏆 Super Dream (>20 LPA)**, **💼 Dream (10-20 LPA)**, **⚡ Core & IT (6-10 LPA)**.
  - Sub-millisecond instant search by student name, email, or ID with department, placement status, and career readiness filters.
* **Official Performance Completion Certificate:**
  - Dedicated printable and downloadable Certificate of Performance Completion (`/student/<id>/certificate`) for every one of the 1,200 students.
  - Features official autonomous board seal, verification ID, verified competencies, CGPA standing, placement milestone, and executive signatures.
* **Admin Profile Registration (Add Student):**
  - Integrated portal (`/student/add`) for administrators to enroll new students with name, email, department, academic year, CGPA, recruitment offer, and multi-skill proficiency matrices.
  - Automatic real-time computation of Career Readiness score and readiness tier.
* **Interactive Chart.js Visualizations:**
  1. **Department Placement Distribution:** Grouped bar chart comparing enrolled vs. placed students per department.
  2. **Placement Ratio Doughnut:** Real-time breakdown of Placed vs. In-Preparation cohorts.
  3. **Salary Package Tiers (LPA):** Super Dream (>20 LPA), Dream (10-20 LPA), Regular (6-10 LPA), Core (<6 LPA).
  4. **Top Recruiting Partners:** Horizontal bar chart analyzing offers per recruiter (Google, Microsoft, Amazon, Adobe, Oracle, Zoho, etc.).
  5. **Academic CGPA Spread:** Trend distribution across grade brackets.
  6. **Technical Skills Radar:** Frequency analysis of high-demand industry skills across all 1,200 students.
  7. **Student Mastery Radar:** Individual skill competency radar on every student's dedicated profile page.
* **Automated Career Readiness Scoring:**
  - Scientific formula combining academic CGPA (40%), verified skills & proficiencies (40%), and placement status (20%).
  - Categorized into: **Elite Ready (≥85%)**, **Job Ready (72-84%)**, **Developing (55-71%)**, and **Needs Upskilling (<55%)**.
* **Role-Based Admin Management:** Secure session-based authentication enabling administrators to update student records, modify placement packages, and adjust skill proficiency levels.
* **Dual Database Architecture:** Native support for MySQL relational databases with seamless automated SQLite fallback for serverless deployments.

---

## 📊 Dashboard Modules

### 🎓 1. Academic Performance Intelligence
* Cohort-wide CGPA distribution and department-level academic averages.
* Benchmarking individual student CGPA against Department Mean and Campus Mean.

### 💼 2. Placement & Recruitment Analytics
* Real-time status indicators (`PLACED` vs `NOT PLACED`).
* Tier-1 recruiters: Google, Microsoft, Amazon, Adobe, Oracle, Cisco, JPMorgan Chase, Zoho, TCS, Infosys, and more.
* Salary metrics: Maximum package (**32.5 LPA**), Average package (**15.31 LPA**).

### 🧠 3. Technical Skills & Career Readiness Matrix
* Inventory of 16 industry-demanded skills (Python, Machine Learning, Deep Learning, SQL, DSA, React.js, Flask, AWS Cloud, Docker, System Design, etc.).
* 4-Tier Proficiency Ratings: **Expert**, **Advanced**, **Intermediate**, **Beginner**.
* Student-specific skill radar charts rendered dynamically via Chart.js.

---

## 🛠️ Tech Stack & Architecture

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3 (Modern Neon Cyberpunk Theme), JavaScript (ES6+), Chart.js |
| **Backend** | Python 3.11+, Flask 3.x, WSGI Serverless Adapter (`PrefixMiddleware`) |
| **Database** | Dual-Engine: MySQL 8.x / SQLite with 1,200 pre-seeded profiles and b-tree indexes |
| **Deployment** | Vercel Serverless Functions (`@vercel/python`), CDN Edge Caching |
| **Version Control** | Git, GitHub |

---

## 📁 Project Structure

```text
Student-Placement-Analytics-System/
├── api/
│   └── index.py            # Vercel Serverless Function entrypoint with WSGI prefix handling
├── static/
│   ├── script.js           # Chart.js visualization engine & instant 1,200 search/filter
│   └── style.css           # Modern neon cyberpunk responsive dashboard styling
├── templates/
│   ├── index.html          # Main 1,200 student analytics dashboard & Chart.js grid
│   ├── login.html          # Administrator login portal (Gatekeeper authentication)
│   ├── result.html         # Detailed student analytics & individual skill radar chart
│   ├── certificate.html    # Official Performance Completion Certificate (View & Print PDF)
│   ├── add_student.html    # Admin student registration with skills & placement scoring
│   └── edit_student.html   # Admin student update & skills editor
├── .gitignore              # Git ignored files & environments
├── .vercelignore           # Vercel deployment exclusions
├── app.py                  # Core Flask application, API endpoints & routing logic
├── db.py                   # Resilient dual-backend database manager with 1,200 seed engine
├── generate_data.py        # High-accuracy 1,200 student dataset generator
├── my_sql.py               # Local MySQL connection validator script
├── placement_analytics.db  # Pre-generated, indexed 1,200 student SQLite database (643 KB)
├── README.md               # Project documentation & live links
├── requirements.txt        # Production dependencies (Flask, mysql-connector-python)
└── vercel.json             # Vercel serverless routing configuration
```

---

## 💻 Local Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/lithik-raj/Student-Placement-Analytics-System.git
cd Student-Placement-Analytics-System
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🔐 Admin Authentication Credentials

| Role | Username / Email | Password |
|---|---|---|
| **Primary Administrator** | `lithikportal@gmail.com` | `lithik@123` |

---

## 👨‍💻 Author

**Lithik Raj B G**  
*B.Tech – Artificial Intelligence and Data Science*  
* GitHub: [@lithik-raj](https://github.com/lithik-raj)
* Project: [Student Placement Analytics System](https://github.com/lithik-raj/Student-Placement-Analytics-System)
