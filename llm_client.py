"""
llm_client.py

Deterministic planning explanation engine.
Context-aware, time-aware, and tone-safe.
No external LLMs. No randomness.
"""

from nlp.confidence_guard import is_vague_activity


def generate_planning_explanation(
    summary_facts: dict,
    intent: str,
    activity_description: str | None = None,
    hour_context: dict | None = None
) -> str:
    """
    Generate a human-readable planning explanation based on:
    - heat-risk summary facts
    - detected activity intent
    - confidence level of input
    - optional focused time context
    """

    # --- Extract normalized summary facts ---
    max_temp = summary_facts.get("max_temperature")
    peak_humidity = summary_facts.get("peak_humidity")
    high_risk_hours = summary_facts.get("high_risk_hours", [])
    safe_windows = summary_facts.get("safe_windows", [])

    # --- Confidence guard ---
    vague_input = is_vague_activity(activity_description)

    explanation_lines = []

    # --- Context framing (LANGUAGE ONLY) ---
    if vague_input:
        explanation_lines.append(
            "This summary provides general heat-risk context for the selected "
            "location and date based on available forecast data."
        )
    else:
        if intent == "school":
            explanation_lines.append(
                "This planning summary considers outdoor activities involving students, "
                "where supervision, hydration, and heat exposure management are important."
            )
        elif intent == "construction":
            explanation_lines.append(
                "This planning summary considers outdoor work conditions, "
                "with attention to prolonged physical activity and heat stress."
            )
        else:
            # General / work / unspecified activity
            explanation_lines.append(
                "This planning summary considers general outdoor activity and work conditions, "
                "with attention to comfort, hydration, and heat exposure."
            )

    explanation_lines.append("")

    # --- Time-focused context (OPTIONAL, FACTUAL ONLY) ---
    if hour_context:
        time_label = hour_context.get("time")
        temp = hour_context.get("temperature")
        risk_level = hour_context.get("risk_level")

        explanation_lines.append(
            f"Around {time_label[-5:]}, forecast conditions indicate a temperature "
            f"of approximately {temp}°C with {risk_level.lower()} heat risk."
        )

        explanation_lines.append("")

    # --- Core forecast highlights ---
    if max_temp is not None:
        explanation_lines.append(
            f"The maximum forecast temperature for the day is approximately {max_temp}°C."
        )

    if peak_humidity is not None:
        explanation_lines.append(
            f"Peak humidity levels are expected to reach around {peak_humidity}%."
        )

    explanation_lines.append("")

    # --- Risk interpretation (DAY-LEVEL) ---
    if high_risk_hours:
        explanation_lines.append(
            "Elevated heat risk is identified during certain periods of the day."
        )
        explanation_lines.append(
            "Activities during these hours may warrant additional heat mitigation planning."
        )
    else:
        explanation_lines.append(
            "No high-risk heat periods are identified across the day."
        )

    explanation_lines.append("")

    # --- Safe window summarization ---
    if safe_windows:
        if len(safe_windows) >= 20:
            explanation_lines.append(
                "Lower-risk conditions are expected throughout most of the day."
            )
        else:
            explanation_lines.append(
                "Lower-risk conditions are more likely during specific time windows."
            )

    explanation_lines.append("")

    # --- Institutional disclaimer ---
    explanation_lines.append(
        "This summary is intended to support planning decisions and does not "
        "replace official weather advisories or institutional safety protocols."
    )

    return "\n".join(explanation_lines)
