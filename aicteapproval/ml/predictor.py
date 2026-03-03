import os
import joblib
import numpy as np
import pandas as pd

from .feature_builder import build_features

# -----------------------------------------------------------------------------
# Safe base directory (works both in Django and standalone)
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------------------------------------------------------
# Feature names (MUST match training + feature_builder order)
# -----------------------------------------------------------------------------
FEATURE_COLUMNS = [
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

# -----------------------------------------------------------------------------
# Lazy model loading (prevents repeated disk reads)
# -----------------------------------------------------------------------------
_risk_model = None
_approval_model = None
_faculty_model = None


def _load_models():
    """Load models once per process."""
    global _risk_model, _approval_model, _faculty_model

    if _risk_model is None:
        _risk_model = joblib.load(os.path.join(BASE_DIR, "risk_model.pkl"))

    if _approval_model is None:
        _approval_model = joblib.load(os.path.join(BASE_DIR, "approval_model.pkl"))

    if _faculty_model is None:
        _faculty_model = joblib.load(os.path.join(BASE_DIR, "faculty_model.pkl"))


# -----------------------------------------------------------------------------
# Main ML pipeline
# -----------------------------------------------------------------------------
def run_ml_pipeline(inst):
    """
    Runs full ML inference pipeline.

    Parameters
    ----------
    inst : Institution-like object
        Must contain `.data`

    Returns
    -------
    dict
    """

    try:
        _load_models()

        # ------------------------------------------------------------------
        # Build features
        # ------------------------------------------------------------------
        features_list = build_features(inst)

        # 🔹 Use DataFrame to avoid sklearn warning
        features_df = pd.DataFrame([features_list], columns=FEATURE_COLUMNS)

        # ------------------------------------------------------------------
        # Predictions
        # ------------------------------------------------------------------
        risk_score_raw = float(_risk_model.predict(features_df)[0])
        approval_prob = float(_approval_model.predict_proba(features_df)[0][1])
        faculty_shortage_pred = float(_faculty_model.predict(features_df)[0])

        # ------------------------------------------------------------------
        # Normalize risk score
        # ------------------------------------------------------------------
        risk_score = int(max(0, min(100, risk_score_raw)))

        if risk_score >= 60:
            risk_level = "High"
        elif risk_score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        # ------------------------------------------------------------------
        # Safe faculty ratio extraction (index must match feature_builder)
        # ------------------------------------------------------------------
        faculty_ratio = 0.0
        try:
            faculty_ratio = float(features_list[13])
        except Exception:
            pass

        # ------------------------------------------------------------------
        # Final response
        # ------------------------------------------------------------------
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "approval_probability": round(approval_prob * 100, 2),
            "faculty_shortage_pred": faculty_shortage_pred,
            "compliance_pct": max(0, 100 - risk_score),
            "faculty_shortage": faculty_shortage_pred > 0,
            "infra_deficit": risk_score >= 40,
            "expired_certs": False,
            "faculty_ratio": round(faculty_ratio, 2),
            "risk_factors": [],
            "suggestions": [],
            "section_scores": {},
        }

    except Exception as e:
        # 🔴 Never break production flow
        return {
            "risk_score": 0,
            "risk_level": "Unknown",
            "approval_probability": 0,
            "faculty_shortage_pred": 0,
            "compliance_pct": 0,
            "faculty_shortage": False,
            "infra_deficit": False,
            "expired_certs": False,
            "faculty_ratio": 0,
            "risk_factors": [f"ML pipeline error: {str(e)}"],
            "suggestions": ["Check ML model files and feature builder."],
            "section_scores": {},
        }