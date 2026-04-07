import streamlit as st
from pharma_dashboard.db import get_session
from pharma_dashboard.schema import (
    User,
    Site,
    UserSite,
    TrainingModule,
    TrainingAssignment,
    TrainingAttempt,
)

# ------------------------------------------------------------
# PAGE SETUP
# ------------------------------------------------------------
st.set_page_config(
    page_title="Pharma Compliance Dashboard",
    layout="wide"
)

st.title("📊 Pharma Compliance Dashboard")
st.write("Connected to Supabase and ready to display data.")


# ------------------------------------------------------------
# DATABASE SESSION
# ------------------------------------------------------------
session = get_session()


# ------------------------------------------------------------
# SIMPLE METRICS
# ------------------------------------------------------------
total_users = session.query(User).count()
total_sites = session.query(Site).count()
total_modules = session.query(TrainingModule).count()
total_assignments = session.query(TrainingAssignment).count()
total_attempts = session.query(TrainingAttempt).count()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Users", total_users)
col2.metric("Sites", total_sites)
col3.metric("Modules", total_modules)
col4.metric("Assignments", total_assignments)
col5.metric("Attempts", total_attempts)


# ------------------------------------------------------------
# USER TABLE
# ------------------------------------------------------------
st.subheader("👥 Users")

users = session.query(User).all()

if users:
    st.dataframe(
        [
            {
                "ID": u.id,
                "Name": f"{u.first_name} {u.last_name}",
                "Email": u.email,
                "Role": u.role,
                "Active": u.is_active,
                "Created": u.created_at,
            }
            for u in users
        ]
    )
else:
    st.info("No users found in the database.")
