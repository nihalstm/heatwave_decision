"""
text_parser.py

Lightweight text parsing utilities.
Extracts explicit hints from user-provided activity descriptions.
No guessing. No ML. No training.
"""

import re


def extract_location_hint(text: str) -> str | None:
    """
    Attempt to extract a location hint from free text.

    Examples:
        "School trip to Mysore" -> "Mysore"
        "We are visiting Delhi for an excursion" -> "Delhi"

    Returns:
        Location string if confidently detected, else None
    """

    if not text:
        return None

    text = text.strip()

    # Common patterns indicating destination
    patterns = [
        r"\bto\s+([A-Za-z\s]+)",
        r"\bvisit\s+([A-Za-z\s]+)",
        r"\bvisiting\s+([A-Za-z\s]+)",
        r"\bgoing\s+to\s+([A-Za-z\s]+)",
        r"\btrip\s+to\s+([A-Za-z\s]+)",
        r"\bexcursion\s+to\s+([A-Za-z\s]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            location = match.group(1).strip()

            # Avoid extracting overly long or suspicious strings
            if 2 <= len(location.split()) <= 6:
                return location

    return None
