from __future__ import annotations

import json
from dataclasses import dataclass

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .config import DEFAULT_WEEKS


LEVEL_ORDER = {"beginner": 1, "intermediate": 2, "advanced": 3}

ROLE_HINTS = {
    "Applied AI Engineer": ["llm", "rag", "mlops", "api", "evaluation", "embeddings"],
    "Data Scientist": ["statistics", "machine learning", "feature engineering", "ab testing"],
    "Data Engineer": ["pyspark", "etl", "databricks", "data modeling", "cloud"],
}


@dataclass
class DiagnosticAgent:
    name: str = "diagnostic_agent"

    def run(self, profile: dict, catalog: pd.DataFrame) -> dict:
        known_skills = {skill.lower() for skill in profile.get("known_skills", [])}
        target_role = profile.get("target_role", "Applied AI Engineer")
        role_skills = ROLE_HINTS.get(target_role, ROLE_HINTS["Applied AI Engineer"])

        catalog_skill_pool: list[str] = []
        for skills in catalog["skills"]:
            catalog_skill_pool.extend([item.strip().lower() for item in skills.split(",")])

        recommended_focus = []
        for skill in role_skills:
            if skill not in known_skills and skill in catalog_skill_pool:
                recommended_focus.append(skill)

        level = profile.get("current_level", "beginner").lower()
        weekly_hours = int(profile.get("weekly_hours", 6))
        intensity = "balanced"
        if weekly_hours <= 4:
            intensity = "light"
        elif weekly_hours >= 10:
            intensity = "accelerated"

        return {
            "goal_summary": profile["goal"],
            "current_level": level,
            "weekly_hours": weekly_hours,
            "intensity": intensity,
            "target_role": target_role,
            "known_skills": sorted(known_skills),
            "skill_gaps": recommended_focus,
        }


@dataclass
class CurriculumAgent:
    name: str = "curriculum_agent"
    top_k: int = 6

    def run(self, diagnosis: dict, catalog: pd.DataFrame) -> pd.DataFrame:
        query_parts = [
            diagnosis["goal_summary"],
            diagnosis["target_role"],
            " ".join(diagnosis["skill_gaps"]),
        ]
        query = " ".join(part for part in query_parts if part)
        corpus = (catalog["title"] + " " + catalog["description"] + " " + catalog["skills"]).tolist()

        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vectorizer.fit_transform(corpus + [query])
        similarities = cosine_similarity(matrix[-1], matrix[:-1]).flatten()

        ranked = catalog.copy()
        ranked["match_score"] = similarities
        ranked["level_score"] = ranked["level"].map(LEVEL_ORDER)
        current_level_score = LEVEL_ORDER.get(diagnosis["current_level"], 1)
        ranked["level_penalty"] = (ranked["level_score"] - current_level_score).abs()
        ranked["final_score"] = ranked["match_score"] - (ranked["level_penalty"] * 0.05)

        selected = (
            ranked.sort_values(["final_score", "duration_hours"], ascending=[False, True])
            .head(self.top_k)
            .reset_index(drop=True)
        )
        return selected[
            [
                "course_id",
                "title",
                "track",
                "level",
                "duration_hours",
                "skills",
                "match_score",
                "final_score",
            ]
        ]


@dataclass
class SchedulerAgent:
    name: str = "scheduler_agent"
    weeks: int = DEFAULT_WEEKS

    def run(self, profile: dict, selected_courses: pd.DataFrame) -> list[dict]:
        weekly_hours = int(profile.get("weekly_hours", 6))
        course_queue = selected_courses.copy().to_dict(orient="records")
        plan: list[dict] = []

        for week in range(1, self.weeks + 1):
            remaining_hours = weekly_hours
            week_courses: list[dict] = []
            while remaining_hours > 0 and course_queue:
                current = course_queue[0]
                remaining_course = current.get("remaining_hours", current["duration_hours"])
                allocated = min(remaining_hours, remaining_course)
                week_courses.append(
                    {
                        "course_id": current["course_id"],
                        "title": current["title"],
                        "allocated_hours": allocated,
                    }
                )
                remaining_hours -= allocated
                remaining_course -= allocated
                if remaining_course <= 0:
                    course_queue.pop(0)
                else:
                    course_queue[0]["remaining_hours"] = remaining_course
            plan.append(
                {
                    "week": week,
                    "focus": week_courses[0]["title"] if week_courses else "Review and practice",
                    "hours": weekly_hours - remaining_hours,
                    "activities": week_courses,
                }
            )
        return plan


@dataclass
class CoachAgent:
    name: str = "coach_agent"

    def run(self, diagnosis: dict, selected_courses: pd.DataFrame, plan: list[dict]) -> dict:
        top_tracks = selected_courses["track"].value_counts().head(3).index.tolist()
        risks = []
        if diagnosis["weekly_hours"] <= 4:
            risks.append("Low weekly availability may slow skill consolidation.")
        if diagnosis["current_level"] == "beginner" and any(selected_courses["level"] == "advanced"):
            risks.append("There are advanced courses in the plan; add extra practice blocks.")
        if "llm" in diagnosis["skill_gaps"] or "rag" in diagnosis["skill_gaps"]:
            risks.append("Reserve time for experimentation, not only theory.")

        return {
            "narrative": (
                f"This path prioritizes {', '.join(top_tracks)} to support the transition into "
                f"{diagnosis['target_role']}. The sequence starts with high-match content and spreads the workload across "
                f"{len(plan)} weeks."
            ),
            "risks": risks or ["No major pacing risks detected for the selected workload."],
            "success_signals": [
                "Complete the first two courses within the first half of the plan.",
                "Build one portfolio artifact by week 4.",
                "Review progress weekly and rebalance hours if one course drags behind.",
            ],
        }


def plan_to_markdown(plan: list[dict]) -> str:
    lines: list[str] = []
    for week in plan:
        lines.append(f"Week {week['week']}: {week['focus']} ({week['hours']}h)")
        for activity in week["activities"]:
            lines.append(f"- {activity['title']} [{activity['allocated_hours']}h]")
    return "\n".join(lines)


def profile_to_json(profile: dict) -> str:
    return json.dumps(profile, indent=2)

