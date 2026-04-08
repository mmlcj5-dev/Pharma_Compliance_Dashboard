import os
from dotenv import load_dotenv
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials.")

DATABASE_URL = (
    f"postgresql+psycopg2://postgres:{SUPABASE_KEY}"
    "@db.gdkzizmehfvfokwdeapi.supabase.co:5432/postgres"
    "?sslmode=require"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()