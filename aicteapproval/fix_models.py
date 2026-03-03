import joblib
import os

BASE = os.path.join("ml")

print("Loading old models...")

risk = joblib.load(os.path.join(BASE, "risk_model.pkl"))
approval = joblib.load(os.path.join(BASE, "approval_model.pkl"))
faculty = joblib.load(os.path.join(BASE, "faculty_model.pkl"))

print("Re-saving models with current XGBoost...")

joblib.dump(risk, os.path.join(BASE, "risk_model.pkl"))
joblib.dump(approval, os.path.join(BASE, "approval_model.pkl"))
joblib.dump(faculty, os.path.join(BASE, "faculty_model.pkl"))

print("Done.")