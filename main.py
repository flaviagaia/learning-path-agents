import json

from src.pipeline import run_pipeline


if __name__ == "__main__":
    summary = run_pipeline()
    print("Learning Path Agents")
    print("-" * 34)
    print(json.dumps(summary, indent=2))

