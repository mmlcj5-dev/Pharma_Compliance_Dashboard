# streamlit_app.py
from pharma_dashboard.app import *

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

try:
    users = session.query(User.id, User.first_name, User.last_name, User.email).all()
    st.write("RAW USER ROWS:", users)
    st.write("DEBUG: Users section finished")
except Exception as e:
    st.error(f"USER QUERY ERROR: {e}")

st.write("DEBUG: Training Modules section reached")
st.header("Training Modules")

modules = session.query(TrainingModule).all()

st.dataframe(
    [
        {
            "ID": m.id,
            "Title": m.title,
            "Description": m.description,
            "Active": m.active,
        }
        for m in modules
    ]
)

st.header("Training Assignments")
assignments = session.query(TrainingAssignment).all()

st.dataframe(
    [
        {
            "ID": a.id,
            "User ID": a.user_id,
            "Module ID": a.module_id,
            "Assigned At": str(a.assigned_at),
            "Due Date": str(a.due_date),
        }
        for a in assignments
    ]
)

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.write("DEBUG: Heatmap section reached")
st.header("📊 Site Compliance Heatmap")

# Load all data
sites = session.query(Site).all()
modules = session.query(TrainingModule).all()
assignments = session.query(TrainingAssignment).all()
attempts = session.query(TrainingAttempt).all()

# Convert to DataFrames for easier manipulation
df_sites = pd.DataFrame([{"site_id": s.id, "site_name": s.name} for s in sites])
df_modules = pd.DataFrame([{"module_id": m.id, "module_title": m.title} for m in modules])
# Build assignment rows with computed completion
df_assign = []
for a in assignments:
    # Find attempts for this assignment
    a_attempts = [t for t in attempts if t.assignment_id == a.id]

    # Completed if any attempt passed
    completed = any(t.passed for t in a_attempts)

    df_assign.append({
        "site_id": a.site_id,
        "module_id": a.module_id,
        "user_id": a.user_id,
        "completed": 1 if completed else 0,
    })

df_assign = pd.DataFrame(df_assign)

# If no assignments, show message
if df_assign.empty:
    st.info("No training assignments found — cannot generate heatmap yet.")
else:
    # Pivot table: rows = sites, columns = modules, values = % completed
    pivot = (
        df_assign.groupby(["site_id", "module_id"])["completed"]
        .mean()
        .reset_index()
        .pivot(index="site_id", columns="module_id", values="completed")
    )

    # Replace NaN with 0 (no completions)
    pivot = pivot.fillna(0)

    # Convert site_id → site_name
    pivot.index = pivot.index.map(
        lambda sid: df_sites.loc[df_sites["site_id"] == sid, "site_name"].values[0]
    )

    # Convert module_id → module_title
    pivot.columns = pivot.columns.map(
        lambda mid: df_modules.loc[df_modules["module_id"] == mid, "module_title"].values[0]
    )

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(
        pivot,
        annot=True,
        cmap="RdYlGn",
        linewidths=0.5,
        fmt=".0%",
        ax=ax,
    )
    ax.set_title("Training Completion by Site and Module")
    st.pyplot(fig)

