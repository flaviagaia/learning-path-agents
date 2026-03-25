from __future__ import annotations

import json
from typing import Any

import pandas as pd

from .agents import CoachAgent, CurriculumAgent, DiagnosticAgent, SchedulerAgent
from .config import COURSE_SELECTION_PATH, PLAN_PATH, PROCESSED_DIR, SUMMARY_PATH
from .data_generation import SAMPLE_PROFILE, build_demo_data


def run_pipeline(profile: dict[str, Any] | None = None) -> dict:
    catalog = build_demo_data()
    user_profile = profile or SAMPLE_PROFILE

    diagnosis = DiagnosticAgent().run(user_profile, catalog)
    selected_courses = CurriculumAgent().run(diagnosis, catalog)
    weekly_plan = SchedulerAgent().run(user_profile, selected_courses)
    coach_notes = CoachAgent().run(diagnosis, selected_courses, weekly_plan)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    selected_courses.to_csv(COURSE_SELECTION_PATH, index=False)
    PLAN_PATH.write_text(
        json.dumps(
            {
                "profile": user_profile,
                "diagnosis": diagnosis,
                "weekly_plan": weekly_plan,
                "coach_notes": coach_notes,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    summary = {
        "courses_in_catalog": int(len(catalog)),
        "selected_courses": int(len(selected_courses)),
        "weeks_planned": int(len(weekly_plan)),
        "target_role": diagnosis["target_role"],
        "skill_gaps": diagnosis["skill_gaps"],
        "top_course": selected_courses.iloc[0]["title"] if not selected_courses.empty else None,
        "total_planned_hours": int(sum(item["hours"] for item in weekly_plan)),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary

