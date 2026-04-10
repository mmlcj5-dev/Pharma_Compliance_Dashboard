# Dashboard layoout inspired by MWH and Lucy.

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

# ------------------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to:",
    [
        "Dashboard",
        "Users",
        "Sites",
        "Modules",
        "Assignments",
        "Heatmap",
    ]
)

st.title("📊 Pharma Compliance Dashboard")
# st.write("Connected to Supabase and ready to display data.")


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
from sqlalchemy import text

if page == "Users":
    st.header("👥 Users")

    # --- USERS TABLE ---
    users = session.query(User).all()
    user_rows = [{"ID": u.id, "First Name": u.first_name, "Last Name": u.last_name, "Email": u.email} for u in users]
    st.dataframe(user_rows)

    # --- USER DRILL-DOWN ---
    st.subheader("👤 User Detail")

    user_options = {f"{u.first_name} {u.last_name} (ID {u.id})": u.id for u in users}

    selected_label = st.selectbox(
        "Select a user to view details:",
        options=list(user_options.keys()),
    )

    selected_user_id = user_options[selected_label]
    selected_user = next((u for u in users if u.id == selected_user_id), None)

    if selected_user:
        # Build user-site mapping
        user_sites = session.query(UserSite).all()
        user_site_map = {}
        for us in user_sites:
            if us.user_id not in user_site_map:
                user_site_map[us.user_id] = []
            site = session.query(Site).filter(Site.id == us.site_id).first()
            if site:
                user_site_map[us.user_id].append(site.name)
        
        selected_sites = user_site_map.get(selected_user.id, [])

        st.markdown(f"**Name:** {selected_user.first_name} {selected_user.last_name}")
        st.markdown(f"**Email:** {selected_user.email}")
        st.markdown(f"**Sites:** {', '.join(selected_sites) if selected_sites else 'None'}")

        assignments = session.query(TrainingAssignment).all()
        attempts = session.query(TrainingAttempt).all()
        user_assignments = [a for a in assignments if a.user_id == selected_user.id]

        if not user_assignments:
            st.info("This user has no training assignments yet.")
        else:
            rows = []
            for a in user_assignments:
                a_attempts = [t for t in attempts if t.assignment_id == a.id]
                completed = any(t.passed for t in a_attempts)
                last_attempt = max(a_attempts, key=lambda t: t.completed_at) if a_attempts else None

                rows.append({
                    "Assignment ID": a.id,
                    "Module ID": a.module_id,
                    "Site ID": a.site_id,
                    "Due Date": a.due_date,
                    "Completed": "Yes" if completed else "No",
                    "Last Attempt At": getattr(last_attempt, "completed_at", None),
                })

            st.markdown("**Training Assignments**")
            st.dataframe(rows)

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

if page == "Heatmap":
    # st.write("DEBUG: Heatmap section reached") For debugging purposes, indicate that the heatmap section has been reached
    st.header("📊 Site Compliance Heatmap")

    # Load all data
    modules = session.query(TrainingModule).all()
    sites = session.query(Site).all()
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

