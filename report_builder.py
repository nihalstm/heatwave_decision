# report_builder.py

from typing import Dict


def build_planning_prompt(summary_facts: Dict) -> str:
    """
    Builds a controlled prompt for the LLM using
    pre-computed risk facts (not raw weather data).
    """

    max_temp = summary_facts["max_temperature_c"]
    peak_humidity = summary_facts["peak_humidity_pct"]
    high_risk_hours = summary_facts["high_risk_hours"]
    safer_hours = summary_facts["safer_hours"]

    if not high_risk_hours:
        risk_statement = (
            "No significant heatwave risk is indicated for this date "
            "based on forecasted temperature and humidity patterns."
        )
    else:
        risk_statement = (
            f"Elevated heat stress risk is concentrated during the following hours: "
            f"{', '.join(high_risk_hours)}."
        )

    safer_window_text = (
        "The majority of the day falls within lower-risk conditions, "
        "allowing flexibility for outdoor scheduling."
        if len(safer_hours) > 12
        else f"Lower-risk periods are primarily observed during: {', '.join(safer_hours)}."
    )

    prompt = f"""
You are generating a planning explanation for an institution evaluating outdoor activities.

Context:
- Maximum forecast temperature: {max_temp}°C
- Peak forecast humidity: {peak_humidity}%

Heat Risk Interpretation:
- {risk_statement}
- {safer_window_text}

Task:
Write a clear, neutral, and informative planning explanation that:
1. Summarizes the overall heat-related risk for the day
2. Explains why the day is considered low-risk or high-risk
3. Mentions general considerations such as hydration, shade, and supervision
4. Avoids issuing commands or guarantees

Tone:
- Informative
- Calm
- Decision-support focused
- Suitable for school or institutional planning

Length:
- 2 to 3 short paragraphs
"""

    return prompt.strip()
