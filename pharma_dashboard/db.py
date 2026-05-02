import os
from dotenv import load_dotenv
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Try to get from Streamlit secrets if env vars not set
if not SUPABASE_URL and "SUPABASE_URL" in st.secrets:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
if not SUPABASE_KEY and "SUPABASE_KEY" in st.secrets:
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
if not DATABASE_URL and "DATABASE_URL" in st.secrets:
    DATABASE_URL = st.secrets["DATABASE_URL"]

if not DATABASE_URL:
    if not SUPABASE_URL:
        st.error("❌ Missing SUPABASE_URL")
        st.stop()
    # Extract project ref from SUPABASE_URL
    # Assuming SUPABASE_URL is https://xxxxx.supabase.co
    project_ref = SUPABASE_URL.replace("https://", "").replace("http://", "").split(".")[0]
    host = f"{project_ref}.supabase.co"
    # For Supabase, database password is needed, not the anon key
    # SUPABASE_KEY is anon key, we need database password
    db_password = os.getenv("SUPABASE_DB_PASSWORD") or st.secrets.get("SUPABASE_DB_PASSWORD")
    if not db_password:
        st.error("❌ Missing database password. Set SUPABASE_DB_PASSWORD in secrets or env vars.")
        st.info("Get the database password from Supabase Dashboard > Settings > Database")
        st.stop()
    DATABASE_URL = f"postgresql+psycopg2://postgres:{db_password}@{host}:5432/postgres"

STATEMENT_TIMEOUT_MS = os.getenv("STATEMENT_TIMEOUT_MS", "60000")

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": f"-c statement_timeout={STATEMENT_TIMEOUT_MS}"},
)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()