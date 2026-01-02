"""
confidence_guard.py

Detects vague or low-information activity descriptions.
Used to keep planning language neutral and non-assumptive.
"""

def is_vague_activity(text: str) -> bool:
    """
    Returns True if the activity description is too vague
    to justify confident or specific language.
    """

    if not text:
        return True

    text = text.lower().strip()

    # Very short inputs are usually vague
    if len(text.split()) <= 3:
        return True

    # Common vague phrases
    vague_phrases = [
        "going out",
        "just going out",
        "long drive",
        "roaming",
        "hanging out",
        "traveling",
        "travelling",
        "outing",
        "trip",
        "drive",
        "plan",
        "plans",
        "going somewhere"
    ]

    for phrase in vague_phrases:
        if phrase in text:
            return True

    return False
