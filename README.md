# Pharma Compliance Dashboard

A Streamlit-based **training compliance intelligence dashboard** designed for pharmaceutical and regulated environments.  
This package provides real-time visibility into overdue training, upcoming deadlines, site-level performance, and user-level drilldowns — all powered by a Supabase backend.

---

## 🚀 Features

### 🔥 Executive-Level Compliance Insights
- Site-level compliance heatmaps  
- Overdue training alerts  
- Due-soon tracker with urgency indicators  
- User drill-down profiles  
- Real-time KPIs and charts  

### 📬 Automated Email Notifications
- One-click overdue alerts  
- One-click due-soon reminders  
- Secure SMTP integration (Gmail, Outlook, etc.)  

### 🧱 Modular Architecture
- `app.py` — Streamlit UI  
- `db.py` — secure database connection  
- `schema.py` — SQLAlchemy ORM models  
- `utils.py` — email + formatting helpers  

### 🔐 Secure by Design
- No secrets stored in code  
- `.env` file for credentials  
- `.env.example` included for safe distribution  

---

## 📦 Installation

### 1. Install the package

After building the wheel:

```bash
pip install pharma_compliance_dashboard-0.1.0-py3-none-any.whl