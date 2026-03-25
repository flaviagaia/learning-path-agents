from __future__ import annotations

import json

import pandas as pd

from .config import CATALOG_PATH, RAW_DIR, SAMPLE_PROFILE_PATH


COURSE_CATALOG = [
    {
        "course_id": "C001",
        "title": "Python Foundations for Data Work",
        "track": "data",
        "level": "beginner",
        "duration_hours": 10,
        "skills": "python, syntax, notebooks, debugging",
        "description": "Build confidence with Python fundamentals for analytics and automation.",
    },
    {
        "course_id": "C002",
        "title": "SQL for Analytical Queries",
        "track": "data",
        "level": "beginner",
        "duration_hours": 8,
        "skills": "sql, joins, aggregation, filters",
        "description": "Learn SQL queries for reporting and relational analysis.",
    },
    {
        "course_id": "C003",
        "title": "Statistics for Product Decisions",
        "track": "analytics",
        "level": "intermediate",
        "duration_hours": 12,
        "skills": "statistics, hypothesis testing, variance, confidence intervals",
        "description": "Use descriptive and inferential statistics to support business decisions.",
    },
    {
        "course_id": "C004",
        "title": "A/B Testing in Practice",
        "track": "analytics",
        "level": "intermediate",
        "duration_hours": 9,
        "skills": "ab testing, experimentation, metrics, causal inference",
        "description": "Design and analyze experiments with practical guardrails.",
    },
    {
        "course_id": "C005",
        "title": "PySpark for Large-Scale Pipelines",
        "track": "data engineering",
        "level": "intermediate",
        "duration_hours": 14,
        "skills": "pyspark, spark sql, distributed computing, etl",
        "description": "Build scalable transformations on large tabular datasets.",
    },
    {
        "course_id": "C006",
        "title": "Data Modeling for Analytics",
        "track": "data engineering",
        "level": "intermediate",
        "duration_hours": 10,
        "skills": "star schema, dimensions, facts, data marts",
        "description": "Model data for BI, reporting, and machine learning consumption.",
    },
    {
        "course_id": "C007",
        "title": "Machine Learning Fundamentals",
        "track": "machine learning",
        "level": "beginner",
        "duration_hours": 11,
        "skills": "supervised learning, regression, classification, evaluation",
        "description": "Understand classic ML workflows from features to metrics.",
    },
    {
        "course_id": "C008",
        "title": "Feature Engineering for Tabular Models",
        "track": "machine learning",
        "level": "intermediate",
        "duration_hours": 10,
        "skills": "feature engineering, preprocessing, pipelines, leakage",
        "description": "Create stronger tabular models with thoughtful feature design.",
    },
    {
        "course_id": "C009",
        "title": "MLOps and Model Serving",
        "track": "machine learning",
        "level": "advanced",
        "duration_hours": 13,
        "skills": "mlops, deployment, monitoring, api",
        "description": "Operationalize models with reproducibility, monitoring, and APIs.",
    },
    {
        "course_id": "C010",
        "title": "NLP with Transformers",
        "track": "llm",
        "level": "intermediate",
        "duration_hours": 12,
        "skills": "nlp, transformers, embeddings, tokenization",
        "description": "Work with transformer models for classification and semantic tasks.",
    },
    {
        "course_id": "C011",
        "title": "Prompt Engineering and Evaluation",
        "track": "llm",
        "level": "intermediate",
        "duration_hours": 8,
        "skills": "prompt engineering, evaluation, few-shot, guardrails",
        "description": "Design prompts and evaluate LLM performance rigorously.",
    },
    {
        "course_id": "C012",
        "title": "RAG Systems and Vector Search",
        "track": "llm",
        "level": "advanced",
        "duration_hours": 12,
        "skills": "rag, vector search, chunking, retrieval evaluation",
        "description": "Build retrieval-augmented systems with semantic search.",
    },
    {
        "course_id": "C013",
        "title": "Cloud Basics for Data Teams",
        "track": "cloud",
        "level": "beginner",
        "duration_hours": 9,
        "skills": "cloud, storage, compute, security",
        "description": "Understand core cloud primitives used by data platforms.",
    },
    {
        "course_id": "C014",
        "title": "Databricks Workflows and Lakehouse",
        "track": "cloud",
        "level": "intermediate",
        "duration_hours": 11,
        "skills": "databricks, lakehouse, notebooks, orchestration",
        "description": "Use Databricks concepts for data engineering and collaborative analytics.",
    },
    {
        "course_id": "C015",
        "title": "Data Storytelling for Analysts",
        "track": "communication",
        "level": "beginner",
        "duration_hours": 7,
        "skills": "storytelling, dashboards, executive communication, visualization",
        "description": "Present insights with narrative structure and visual clarity.",
    },
    {
        "course_id": "C016",
        "title": "Stakeholder Management for Technical Projects",
        "track": "communication",
        "level": "intermediate",
        "duration_hours": 6,
        "skills": "stakeholder management, planning, prioritization, negotiation",
        "description": "Navigate trade-offs and communication in cross-functional work.",
    },
    {
        "course_id": "C017",
        "title": "Product Analytics and KPI Design",
        "track": "analytics",
        "level": "intermediate",
        "duration_hours": 10,
        "skills": "kpi, funnels, retention, product analytics",
        "description": "Define metrics and analyze product behavior in business context.",
    },
    {
        "course_id": "C018",
        "title": "Git and Collaborative Workflows",
        "track": "engineering",
        "level": "beginner",
        "duration_hours": 5,
        "skills": "git, branching, pull requests, collaboration",
        "description": "Use Git confidently in day-to-day collaborative projects.",
    },
]

SAMPLE_PROFILE = {
    "name": "Flavia",
    "goal": "I want to transition from analytics into LLM applications for business workflows and build production-ready AI assistants.",
    "current_level": "intermediate",
    "weekly_hours": 8,
    "known_skills": [
        "python",
        "sql",
        "pandas",
        "power bi",
        "statistics",
        "streamlit",
    ],
    "target_role": "Applied AI Engineer",
}


def build_demo_data() -> pd.DataFrame:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    catalog = pd.DataFrame(COURSE_CATALOG)
    catalog.to_csv(CATALOG_PATH, index=False)
    SAMPLE_PROFILE_PATH.write_text(json.dumps(SAMPLE_PROFILE, indent=2), encoding="utf-8")
    return catalog

