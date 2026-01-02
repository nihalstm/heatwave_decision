"""
intent_detector.py

Lightweight, deterministic intent classification for activity context.
This module does NOT decide risk. It only influences explanation language.
"""

def detect_intent(text: str) -> str:
    """
    Detect high-level activity context from user-provided text.

    Returns:
        "school" | "construction" | "general"
    """

    if not text:
        return "general"

    text = text.lower()

    # --- School-related keywords ---
    school_keywords = [
        "school",
        "student",
        "students",
        "children",
        "class",
        "teacher",
        "teachers",
        "college",
        "campus",
        "picnic",
        "field trip",
        "annual trip",
        "excursion"
    ]

    # --- Construction / labor-related keywords ---
    construction_keywords = [
        "construction",
        "site",
        "labour",
        "labor",
        "worker",
        "workers",
        "contractor",
        "shift",
        "worksite",
        "building work"
    ]

    for keyword in school_keywords:
        if keyword in text:
            return "school"

    for keyword in construction_keywords:
        if keyword in text:
            return "construction"

    # --- Default fallback ---
    return "general"
