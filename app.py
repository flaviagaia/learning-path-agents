from __future__ import annotations

import json

import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import COURSE_SELECTION_PATH, PLAN_PATH, SUMMARY_PATH
from src.pipeline import run_pipeline


def _load_outputs(profile: dict | None = None) -> tuple[dict, pd.DataFrame, dict]:
    try:
        summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
        courses = pd.read_csv(COURSE_SELECTION_PATH)
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
        if courses.empty or "title" not in courses.columns:
            raise ValueError("selected courses missing")
        if "weekly_plan" not in plan or "coach_notes" not in plan:
            raise ValueError("plan missing")
        return summary, courses, plan
    except Exception:
        summary = run_pipeline(profile)
        courses = pd.read_csv(COURSE_SELECTION_PATH)
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
        return summary, courses, plan


st.set_page_config(page_title="Learning Path Agents", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background: #07111f; color: #e8edf5; }
    .hero {
        background: linear-gradient(135deg, rgba(12, 23, 40, 0.95), rgba(16, 38, 66, 0.92));
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 24px;
        padding: 1.4rem;
        margin-bottom: 1rem;
    }
    .hero h1, .hero p { color: #e8edf5; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>Learning Path Agents</h1>
        <p>Multi-agent workspace to diagnose skills, curate courses, build a weekly study plan, and coach a professional transition.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Learner Profile")
    name = st.text_input("Name", value="Flavia")
    target_role = st.selectbox(
        "Target role",
        options=["Applied AI Engineer", "Data Scientist", "Data Engineer"],
        index=0,
    )
    level = st.selectbox("Current level", options=["beginner", "intermediate", "advanced"], index=1)
    weekly_hours = st.slider("Weekly hours", min_value=3, max_value=15, value=8)
    goal = st.text_area(
        "Goal",
        value="I want to transition from analytics into LLM applications for business workflows and build production-ready AI assistants.",
        height=120,
    )
    skills_raw = st.text_area(
        "Known skills",
        value="python, sql, pandas, power bi, statistics, streamlit",
        height=100,
    )
    profile = {
        "name": name,
        "goal": goal,
        "current_level": level,
        "weekly_hours": weekly_hours,
        "known_skills": [item.strip() for item in skills_raw.split(",") if item.strip()],
        "target_role": target_role,
    }
    refresh = st.button("Generate study path")

if refresh:
    run_pipeline(profile)

summary, courses, plan = _load_outputs(profile)
diagnosis = plan["diagnosis"]
weekly_plan = plan["weekly_plan"]
coach_notes = plan["coach_notes"]

metrics = st.columns(5)
metrics[0].metric("Catalog courses", summary["courses_in_catalog"])
metrics[1].metric("Selected courses", summary["selected_courses"])
metrics[2].metric("Weeks", summary["weeks_planned"])
metrics[3].metric("Total hours", summary["total_planned_hours"])
metrics[4].metric("Top recommendation", summary["top_course"])

tab_path, tab_courses, tab_coach = st.tabs(["Learning Path", "Recommended Courses", "Coach Notes"])

with tab_path:
    schedule_df = pd.DataFrame(
        [
            {"week": item["week"], "focus": item["focus"], "hours": item["hours"]}
            for item in weekly_plan
        ]
    )
    st.plotly_chart(
        px.bar(schedule_df, x="week", y="hours", color="focus", title="Weekly study allocation"),
        use_container_width=True,
    )
    for item in weekly_plan:
        with st.expander(f"Week {item['week']} - {item['focus']}"):
            for activity in item["activities"]:
                st.write(f"- {activity['title']} ({activity['allocated_hours']}h)")

with tab_courses:
    st.subheader("Diagnosis")
    st.write(f"Target role: `{diagnosis['target_role']}`")
    st.write(f"Intensity: `{diagnosis['intensity']}`")
    st.write("Skill gaps:", ", ".join(diagnosis["skill_gaps"]) if diagnosis["skill_gaps"] else "No critical gaps detected")
    st.dataframe(courses, use_container_width=True, hide_index=True)

with tab_coach:
    st.subheader("Coach Narrative")
    st.write(coach_notes["narrative"])
    st.subheader("Risks")
    for risk in coach_notes["risks"]:
        st.write(f"- {risk}")
    st.subheader("Success Signals")
    for signal in coach_notes["success_signals"]:
        st.write(f"- {signal}")

