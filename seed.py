# seed.py
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import text

from pharma_dashboard.db import get_session
from pharma_dashboard.schema import (
    Base,
    User,
    Site,
    UserSite,
    TrainingModule,
    TrainingAssignment,
    TrainingAttempt,
)

# ------------------------------------------------------------
# Load environment variables from .env
# ------------------------------------------------------------
load_dotenv()

print("\n=== PHARMA COMPLIANCE DATABASE SEEDER ===\n")

# ------------------------------------------------------------
# Connect to DB
# ------------------------------------------------------------
session = get_session()
engine = session.get_bind()

# ------------------------------------------------------------
# 1. DROP TABLES SAFELY (raw SQL avoids Supabase locks)
# ------------------------------------------------------------
print("Dropping tables...")

drop_statements = [
    text("DROP TABLE IF EXISTS training_attempts CASCADE;"),
    text("DROP TABLE IF EXISTS training_assignments CASCADE;"),
    text("DROP TABLE IF EXISTS user_sites CASCADE;"),
    text("DROP TABLE IF EXISTS training_modules CASCADE;"),
    text("DROP TABLE IF EXISTS users CASCADE;"),
    text("DROP TABLE IF EXISTS sites CASCADE;"),
]

for stmt in drop_statements:
    session.execute(stmt)

session.commit()
print("Tables dropped successfully.\n")

# ------------------------------------------------------------
# 2. RECREATE TABLES USING SQLAlchemy
# ------------------------------------------------------------
print("Recreating tables...")
Base.metadata.create_all(engine)
print("Tables created.\n")

# ------------------------------------------------------------
# 3. SEED SITES
# ------------------------------------------------------------
print("Seeding sites...")

sites = [
    Site(name="Dallas Clinic", code="DAL-001", city="Dallas", state="TX", country="USA"),
    Site(name="Fort Worth Manufacturing", code="FWM-002", city="Fort Worth", state="TX", country="USA"),
    Site(name="Austin Research Center", code="AUS-003", city="Austin", state="TX", country="USA"),
    Site(name="Houston Packaging Facility", code="HOU-004", city="Houston", state="TX", country="USA"),
]

session.add_all(sites)
session.commit()
print("Sites seeded.\n")

# ------------------------------------------------------------
# 4. SEED USERS
# ------------------------------------------------------------
print("Seeding users...")

users = [
    User(first_name="Emily", last_name="Turner", email="emily.turner@pharmaco.com", role="Technician"),
    User(first_name="James", last_name="Holloway", email="james.holloway@pharmaco.com", role="QA Specialist"),
    User(first_name="Priya", last_name="Desai", email="priya.desai@pharmaco.com", role="Lab Analyst"),
    User(first_name="Marcus", last_name="Reed", email="marcus.reed@pharmaco.com", role="Warehouse Operator"),
    User(first_name="Sofia", last_name="Martinez", email="sofia.martinez@pharmaco.com", role="Clinical Coordinator"),
    User(first_name="Daniel", last_name="Kim", email="daniel.kim@pharmaco.com", role="Technician"),
    User(first_name="Hannah", last_name="Brooks", email="hannah.brooks@pharmaco.com", role="QA Specialist"),
    User(first_name="Omar", last_name="Rahman", email="omar.rahman@pharmaco.com", role="Aseptic Operator"),
]

session.add_all(users)
session.commit()
print("Users seeded.\n")

# ------------------------------------------------------------
# 5. MAP USERS TO SITES
# ------------------------------------------------------------
print("Mapping users to sites...")

user_sites = [
    UserSite(user_id=1, site_id=1, role_at_site="Manufacturing Tech"),
    UserSite(user_id=2, site_id=1, role_at_site="QA Specialist"),
    UserSite(user_id=3, site_id=2, role_at_site="Lab Analyst"),
    UserSite(user_id=4, site_id=2, role_at_site="Warehouse Operator"),
    UserSite(user_id=5, site_id=3, role_at_site="Clinical Coordinator"),
    UserSite(user_id=6, site_id=3, role_at_site="Manufacturing Tech"),
    UserSite(user_id=7, site_id=4, role_at_site="QA Specialist"),
    UserSite(user_id=8, site_id=4, role_at_site="Aseptic Operator"),
]

session.add_all(user_sites)
session.commit()
print("User-site mappings seeded.\n")

# ------------------------------------------------------------
# 6. SEED TRAINING MODULES
# ------------------------------------------------------------
print("Seeding training modules...")

modules = [
    TrainingModule(title="GMP Annual Certification", description="Good Manufacturing Practices annual certification."),
    TrainingModule(title="GxP Data Integrity", description="ALCOA+ principles and data integrity."),
    TrainingModule(title="21 CFR Part 11 Compliance", description="Electronic records and signatures."),
    TrainingModule(title="Deviation & CAPA Fundamentals", description="Deviation handling and CAPA."),
    TrainingModule(title="Aseptic Technique Certification", description="Sterile operations and contamination control."),
    TrainingModule(title="Hazardous Materials Handling", description="OSHA/DOT hazmat training."),
    TrainingModule(title="HIPAA Privacy & Security", description="Patient data privacy."),
    TrainingModule(title="Cleaning Validation Basics", description="Cleaning validation procedures."),
]

session.add_all(modules)
session.commit()
print("Training modules seeded.\n")

# ------------------------------------------------------------
# 7. SEED TRAINING ASSIGNMENTS
# ------------------------------------------------------------
print("Seeding training assignments...")

assignments = [
    TrainingAssignment(user_id=1, module_id=1, site_id=1, due_date=datetime.now() + timedelta(days=30)),
    TrainingAssignment(user_id=1, module_id=5, site_id=1, due_date=datetime.now() + timedelta(days=45)),
    TrainingAssignment(user_id=2, module_id=2, site_id=1, due_date=datetime.now() + timedelta(days=20)),
    TrainingAssignment(user_id=2, module_id=4, site_id=1, due_date=datetime.now() + timedelta(days=25)),
    TrainingAssignment(user_id=3, module_id=7, site_id=2, due_date=datetime.now() + timedelta(days=15)),
    TrainingAssignment(user_id=3, module_id=3, site_id=2, due_date=datetime.now() + timedelta(days=40)),
    TrainingAssignment(user_id=4, module_id=6, site_id=2, due_date=datetime.now() + timedelta(days=10)),
    TrainingAssignment(user_id=5, module_id=7, site_id=3, due_date=datetime.now() + timedelta(days=35)),
    TrainingAssignment(user_id=6, module_id=1, site_id=3, due_date=datetime.now() + timedelta(days=30)),
    TrainingAssignment(user_id=7, module_id=2, site_id=4, due_date=datetime.now() + timedelta(days=20)),
    TrainingAssignment(user_id=8, module_id=5, site_id=4, due_date=datetime.now() + timedelta(days=25)),
]

session.add_all(assignments)
session.commit()
print("Training assignments seeded.\n")

# ------------------------------------------------------------
# 8. SEED TRAINING ATTEMPTS
# ------------------------------------------------------------
print("Seeding training attempts...")

attempts = [
    TrainingAttempt(assignment_id=1, user_id=1, passed=True, completed_at=datetime.now() - timedelta(days=1)),
    TrainingAttempt(assignment_id=3, user_id=2, passed=True, completed_at=datetime.now() - timedelta(days=2)),
    TrainingAttempt(assignment_id=5, user_id=3, passed=True, completed_at=datetime.now() - timedelta(days=3)),
    TrainingAttempt(assignment_id=7, user_id=4, passed=False, completed_at=datetime.now() - timedelta(days=1)),
    TrainingAttempt(assignment_id=10, user_id=7, passed=True, completed_at=datetime.now() - timedelta(days=4)),
]

session.add_all(attempts)
session.commit()
print("Training attempts seeded.\n")

print("=== DATABASE SEEDING COMPLETE ===\n")