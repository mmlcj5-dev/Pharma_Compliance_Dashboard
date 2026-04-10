import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

import os
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

# 2. Load Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials.")

# 3. Build DATABASE_URL
DATABASE_URL = (
    f"postgresql+psycopg2://postgres.kjscibctzfiyhcokqtcl:{SUPABASE_KEY}"
    "@aws-1-us-west-2.pooler.supabase.com:5432/postgres"
    "?sslmode=require"
)

# 4. Create engine
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL, echo=False)

# 5. Import ALL models BEFORE create_all()
from pharma_dashboard.models import (
    Base,
    User,
    Site,
    UserSite,
    Training,
    TrainingModule,
    TrainingRecord,
    UserCredential,
    TrainingAssignment,
    TrainingAttempt
)

# 6. Create all tables
print(">>> CREATING TABLES NOW <<<")
Base.metadata.create_all(engine)

# 7. Create session
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()