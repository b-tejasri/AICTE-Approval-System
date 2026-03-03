import os
import joblib
import pandas as pd
import numpy as np

from xgboost import XGBRegressor, XGBClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(os.path.dirname(BASE_DIR), "aicte_synthetic_dataset.csv")

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

# ------------------------------------------------------------------
# Feature engineering (must match feature_builder)
# ------------------------------------------------------------------

NAAC_MAP = {
    "A++": 6,
    "A+": 5,
    "A": 4,
    "B++": 3,
    "B+": 2,
    "B": 1,
    "": 0,
}

print("Engineering features...")

# Encode NAAC
df["naac_encoded"] = df["naac_grade"].map(NAAC_MAP).fillna(0)

# Count NBA programs properly
df["nba_count"] = df["nba_programs"].fillna("").apply(
    lambda x: len([p for p in str(x).split(",") if p.strip()])
)

# ------------------------------------------------------------------
# Feature columns (must match feature_builder order)
# ------------------------------------------------------------------

FEATURE_COLS = [
    "total_faculty",
    "required_faculty",
    "faculty_phd_count",
    "total_students",
    "total_labs",
    "total_classrooms",
    "computer_count",
    "library_books",
    "total_area_sqft",
    "hostel_capacity",
    "annual_budget",
    "iso_certified",
    "nba_count",
    "faculty_ratio",
    "phd_percentage",
    "area_per_student",
    "computer_student_ratio",
    "naac_encoded",
]

X = df[FEATURE_COLS]

# ------------------------------------------------------------------
# Targets (aligned with your dataset)
# ------------------------------------------------------------------

y_risk = df["risk_score"]
y_approval = df["approved"]  # ✅ FIXED
y_faculty_gap = df["faculty_shortage_amt"]  # ✅ FIXED

# ------------------------------------------------------------------
# Split
# ------------------------------------------------------------------

X_train, X_test, yr_train, yr_test = train_test_split(
    X, y_risk, test_size=0.2, random_state=42
)

_, _, ya_train, ya_test = train_test_split(
    X, y_approval, test_size=0.2, random_state=42
)

_, _, yf_train, yf_test = train_test_split(
    X, y_faculty_gap, test_size=0.2, random_state=42
)

print("Training models...")

# ------------------------------------------------------------------
# Risk model
# ------------------------------------------------------------------

risk_model = XGBRegressor(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    tree_method="hist",
)

risk_model.fit(X_train, yr_train)

# ------------------------------------------------------------------
# Approval model
# ------------------------------------------------------------------

approval_model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    tree_method="hist",
    eval_metric="logloss",
)

approval_model.fit(X_train, ya_train)

# ------------------------------------------------------------------
# Faculty model
# ------------------------------------------------------------------

faculty_model = LinearRegression()
faculty_model.fit(X_train, yf_train)

print("Saving models...")

joblib.dump(risk_model, os.path.join(BASE_DIR, "risk_model.pkl"))
joblib.dump(approval_model, os.path.join(BASE_DIR, "approval_model.pkl"))
joblib.dump(faculty_model, os.path.join(BASE_DIR, "faculty_model.pkl"))

print("✅ Models retrained and saved successfully.")