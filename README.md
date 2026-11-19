# Student Placement Analytics System

<div align="center">

[![Vercel Live Demo](https://img.shields.io/badge/Vercel-Live_Demo-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://student-placement-analytics-system.vercel.app/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Zero_Config-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Status](https://img.shields.io/badge/Status-Live_%26_Production_Ready-brightgreen?style=for-the-badge)]()

<br/>

**A full-stack, enterprise-grade placement analytics and student career readiness tracking platform built with Python Flask, Chart.js, and modern cyberpunk dashboard UI.**

[🚀 Explore Live Demo](https://student-placement-analytics-system.vercel.app/) • [✨ Deploy to Vercel](#-deploy-to-vercel-in-1-click) • [📖 Documentation](#-system-workflow)

---

</div>

## 🌐 Live Demo & Instant Access

The application is deployed live on Vercel and ready for instant evaluation:

* **Live Demo URL:** [https://student-placement-analytics-system.vercel.app/](https://student-placement-analytics-system.vercel.app/)
* **Default Admin Credentials:**
  * **Email / ID:** `lithikportal@gmail.com`
  * **Password:** `lithik@123`

> [!NOTE]
> The cloud deployment features an automatic dual-database engine. When running on serverless cloud platforms like Vercel, it uses an embedded, pre-seeded high-performance database engine so that all dashboard statistics, student profiles, charts, and admin CRUD updates function seamlessly with zero external database configuration required. When hosted on-premise or configured with cloud MySQL, it seamlessly connects to your MySQL cluster.

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

* **Interactive Analytics Dashboard:** Real-time metrics on total students, placement ratios, active recruiters, and department-wise performance.
* **Student-Wise Deep Dive:** Dedicated student profile cards showing CGPA, department, placement status, package (LPA), and skills.
* **Skills & Readiness Matrix:** Categorized proficiency tracking (Beginner, Intermediate, Advanced, Expert) for top technical domains.
* **Instant Search & Filter:** Client-side real-time filtering by student name or department without page reloads.
* **Role-Based Admin Management:** Secure session-based authentication enabling administrators to update student records, modify placement packages, and adjust skill proficiency.
* **Dual Database Architecture:** Native support for MySQL relational databases with seamless automated SQLite fallback for serverless deployments.
* **Cyberpunk Neon UI:** Responsive, high-contrast dark theme with glowing neon accents, smooth animations, and optimized mobile layouts.

---

## 📊 Dashboard Modules

### 🎓 Academic Analytics
* Comprehensive student profiles (Name, ID, Department, Year, CGPA, Gender)
* Department-wise enrollment and placement distribution visualization
* Real-time CGPA tracking and academic performance badges

### 💼 Placement Analytics
* Real-time status indicators (`PLACED` vs `NOT PLACED`)
* Recruiter details (Company Name, Industry Sector, Package in LPA)
* Placement date tracking and historical placement log

### 🧠 Skills & Career Readiness
* Technical skill inventory (Python, Machine Learning, Deep Learning, SQL, React, etc.)
* Multi-tier proficiency ratings:
  * 🟢 **Expert**
  * 🔵 **Advanced**
  * 🟡 **Intermediate**
  * ⚪ **Beginner**
* Direct career readiness evaluation based on skillset matches

---

## 🛠️ Tech Stack & Architecture

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3 (Modern Neon/Dark Grid), JavaScript (ES6+), Chart.js |
| **Backend** | Python 3.11+, Flask 3.x, WSGI Serverless Adapter |
| **Database** | MySQL 8.x / SQLite Dual-Engine with Automatic Schema Seeding |
| **Deployment** | Vercel Serverless Functions (`@vercel/python`), CDN Edge Caching |
| **Version Control** | Git, GitHub |

---

## 📁 Project Structure

```text
Student-Placement-Analytics-System/
├── api/
│   └── index.py            # Vercel Serverless Function entrypoint
├── static/
│   ├── script.js           # Client-side dynamic search and interactions
│   └── style.css           # Modern neon/cyberpunk dashboard styling
├── templates/
│   ├── index.html          # Main placement analytics dashboard
│   ├── login.html          # Administrator login portal
│   ├── result.html         # Detailed student analytics view
│   └── edit_student.html   # Admin student update & skills editor
├── .gitignore              # Git ignored files & environments
├── .vercelignore           # Vercel deployment exclusions
├── app.py                  # Core Flask application & routing logic
├── db.py                   # Resilient dual-backend database manager
├── my_sql.py               # Local MySQL connection validator script
├── README.md               # Project documentation & live links
├── requirements.txt        # Production dependencies
└── vercel.json             # Vercel serverless routing configuration
```

---

## 🔄 System Workflow

```text
┌──────────────────────────────────────────────┐
│           Main Dashboard (Home)              │
│   • Placement Rate  • Department Analytics   │
│   • Quick Search    • Student Grid Cards     │
└───────────────────────┬──────────────────────┘
                        │
                        ▼ Select Student
┌──────────────────────────────────────────────┐
│          Student Analytics Dashboard         │
│   ┌────────────────────┬─────────────────┐   │
│   │ Academic Summary   │ Placement Info  │   │
│   ├────────────────────┼─────────────────┤   │
│   │ Technical Skills   │ Career Readiness│   │
│   └────────────────────┴─────────────────┘   │
└───────────────────────┬──────────────────────┘
                        │
                        ▼ Click "Update Student"
┌──────────────────────────────────────────────┐
│           Admin Authentication (Login)       │
│   • ID: lithikportal@gmail.com               │
│   • Password: lithik@123                     │
└───────────────────────┬──────────────────────┘
                        │
                        ▼ Authenticated
┌──────────────────────────────────────────────┐
│            Admin Management Portal           │
│   • Edit Academic Data (CGPA, Year, Dept)    │
│   • Update Placements (Company, LPA, Date)   │
│   • Assign & Adjust Skill Proficiencies      │
└──────────────────────────────────────────────┘
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

### 4. Configure Database (Optional)
* **Out-of-the-box (Default):** Runs immediately with zero configuration using the embedded SQLite engine and pre-seeded realistic data.
* **With MySQL:** Set environment variables or configure your MySQL server:
```bash
export MYSQL_HOST="localhost"
export MYSQL_USER="root"
export MYSQL_PASSWORD="your_password"
export MYSQL_DATABASE="placement_analytics"
export MYSQL_PORT=3306
```

### 5. Run the Application
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🔐 Admin Authentication Credentials

| Role | Username / Email | Password |
|---|---|---|
| **Primary Administrator** | `lithikportal@gmail.com` | `lithik@123` |

*(Credentials can also be customized via `ADMIN_USERNAME` and `ADMIN_PASSWORD` environment variables)*

---

## 🔮 Future Enhancements

* [ ] Machine Learning-based placement probability scoring
* [ ] Automated resume parsing and skill-gap recommendations
* [ ] Recruiter-specific hiring trend forecasting
* [ ] Automated PDF placement performance report generation
* [ ] Multi-tenant role management (Student, Staff, Recruiter, Admin)

---

## 👨‍💻 Author

**Lithik Raj B G**  
*B.Tech – Artificial Intelligence and Data Science*  
* GitHub: [@lithik-raj](https://github.com/lithik-raj)
* Project: [Student Placement Analytics System](https://github.com/lithik-raj/Student-Placement-Analytics-System)
