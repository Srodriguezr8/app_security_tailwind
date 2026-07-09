## 🏥 Clinic Management System

## 📌 Description
A comprehensive clinic management system designed to streamline healthcare operations. This web application facilitates secure user role-based access, efficient management of doctors, patients, appointments, and medical examinations. Built with modern web technologies to provide a responsive and intuitive interface.

## ✨ Key Features
- 🔒 **Role-based user authentication** (Admin, Doctors, Staff)
- 👨‍⚕️ **Doctor management and scheduling**
- 🏥 **Patient records and history tracking**
- 📅 **Appointment scheduling system**
- 🧪 **Medical examination management**
- 📊 **Reporting and analytics dashboard**

## 🛠️ Technology Stack
- **Backend:** Django (Python)
- **Frontend:** Tailwind CSS
- **Database:** SQLite (for development)
- **Deployment:** Ready for production environments

## 👨‍💻 Development Team
- Juan Taday (Developer)
- Adrian Avila (Developer)
- Damian Solari (Developer)
## 📁 Project Structure

```plaintext
API_SEQUENT_XALUMIND/
├── applications/
│   Django apps
├── proxy_dimco/
│   Proxy configurations
├── static/
│   Static files
├── templates/
│   HTML templates
├── theme/
│   Custom themes
├── verv/
│   Version control
├── db.sqlite3
│   Database file
├── dependencies.txt
│   Project dependencies
├── manage.py
│   Django management script
├── README.md
│   Project documentation
└── tailwin4.config.js
```

## 🚀 Installation

1. **Clone the repository**

```bash
git clone https://your-repository-url.git
cd API_SEQUENT_XALUMIND
```

2. **Create virtual environment**

```bash
python -m venv .venv
```

3. **Activate virtual environment (Windows PowerShell)**

```powershell
.\.venv\Scripts\Activate.ps1
```

> Si PowerShell bloquea la ejecución, usa:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

4. **Install dependencies**

```bash
pip install -r dependencies.txt
```

5. **Run migrations**

```bash
python manage.py migrate
```

6. **Start the development server**

```bash
python manage.py runserver
```

---
# 🎓 Academic Practice Context

This repository was forked and used as the base project for the practical assignment **Software Security and Change Management**.

The objective of this practice was to simulate a collaborative software development workflow using modern software engineering practices, including:

- Git and GitHub version control
- Feature branches and Pull Requests
- Continuous Integration (CI) with GitHub Actions
- Static security analysis with Bandit
- Release management with GitHub Releases

## 👥 Team Members

| Member | Professional Role |
|---|---|
| Juan Taday | Release Manager |
| Erick Villavicencio | QA Engineer |
| Santiago Rodriguez | Frontend Developer |
| Daniel Palma | Security Engineer |

## 📌 Academic Purpose

This fork was used exclusively for educational and experimental purposes related to software security, version management, continuous integration, and collaborative development workflows.


## 📄 License
This project is proprietary software. All rights reserved by the development team.

