import numpy as np

NAAC_MAP = {
    "A++": 6,
    "A+": 5,
    "A": 4,
    "B++": 3,
    "B+": 2,
    "B": 1,
    "": 0,
    None: 0,
}

def build_features(inst):
    try:
        d = inst.data
    except Exception:
        return [0] * 18

    total_faculty = d.total_faculty or 0
    total_students = d.total_students or 0
    computer_count = d.computer_count or 0

    faculty_ratio = (
        total_students / total_faculty
        if total_faculty > 0 else 0
    )

    phd_percentage = (
        d.faculty_phd_count / total_faculty
        if total_faculty > 0 else 0
    )

    area_per_student = (
        d.total_area_sqft / total_students
        if total_students > 0 else 0
    )

    computer_student_ratio = (
        total_students / computer_count
        if computer_count > 0 else 0
    )

    naac_encoded = NAAC_MAP.get(d.naac_grade, 0)

    nba_count = len(d.nba_programs or "")

    return [
        total_faculty,
        d.required_faculty or 0,
        d.faculty_phd_count or 0,
        total_students,
        d.total_labs or 0,
        d.total_classrooms or 0,
        computer_count,
        d.library_books or 0,
        d.total_area_sqft or 0,
        d.hostel_capacity or 0,
        d.annual_budget or 0,
        int(d.iso_certified),
        nba_count,
        faculty_ratio,
        phd_percentage,
        area_per_student,
        computer_student_ratio,
        naac_encoded,
    ]