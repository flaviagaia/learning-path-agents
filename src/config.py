from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
ASSETS_DIR = BASE_DIR / "assets"

CATALOG_PATH = RAW_DIR / "course_catalog.csv"
SAMPLE_PROFILE_PATH = RAW_DIR / "sample_profile.json"
PLAN_PATH = PROCESSED_DIR / "learning_plan.json"
COURSE_SELECTION_PATH = PROCESSED_DIR / "selected_courses.csv"
SUMMARY_PATH = PROCESSED_DIR / "summary.json"

DEFAULT_WEEKS = 6

