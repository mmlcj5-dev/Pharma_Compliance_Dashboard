import os
import logging
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Reduce SQLAlchemy noise
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# ------------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ------------------------------------------------------------
load_dotenv()  # Local development

def get_supabase_credentials():
    """
    Load Supabase credentials from Streamlit Cloud (st.secrets)
    or from local .env when running locally.
    """
    # Streamlit Cloud
    if "SUPABASE_URL" in st.secrets:
        return (
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"]
        )

    # Local development
    return (
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )

# ------------------------------------------------------------
# BUILD DATABASE URL
# ------------------------------------------------------------
def get_database_url():
    SUPABASE_URL, SUPABASE_KEY = get_supabase_credentials()

    if not SUPABASE_URL or not SUPABASE_KEY:
        # Return None instead of crashing — prevents Streamlit Cloud hang
        return None

    # pg8000 driver
    return (
        f"postgresql+pg8000://postgres:{SUPABASE_KEY}"
        "@aws-1-us-west-2.pooler.supabase.com:5432/postgres"
        "?sslmode=require"
    )

# ------------------------------------------------------------
# CREATE ENGINE (cached so Streamlit doesn't recreate it)
# ------------------------------------------------------------
@st.cache_resource
def get_engine():
    db_url = get_database_url()
    if not db_url:
        return None  # App will show a friendly message instead of hanging
    return create_engine(db_url, echo=False)

# ------------------------------------------------------------
# SESSION FACTORY
# ------------------------------------------------------------
def get_session():
    engine = get_engine()
    if engine is None:
        return None
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()

# ------------------------------------------------------------
# IMPORT MODELS (AFTER engine exists)
# ------------------------------------------------------------
from pharma_dashboard.models import Base
