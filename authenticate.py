from pathlib import Path
from ml_pipeline import authenticate
from llm_explainer import explain_decision

# get project root safely
PROJECT_ROOT = Path(__file__).resolve().parent

UNKNOWN_DIR = PROJECT_ROOT / "data" / "real_world" / "raw" / "unknown"

print("Looking for unknown data at:")
print(UNKNOWN_DIR)

result = authenticate(UNKNOWN_DIR)
explanation = explain_decision(result)

print("\n--- AUTHENTICATION RESULT ---")
for k, v in result.items():
    print(f"{k}: {v}")

print("\n--- LLM EXPLANATION ---")
print(explanation)
