"""
risk_engine.py

Core deterministic heat-risk classification logic.
Produces a per-hour risk timeline and normalized summary facts.
Also derives a high-level planning decision.
"""

def classify_heat_risk(temperature: float, humidity: float) -> str:
    """
    Institution-oriented heat risk classification.
    Tuned for planning decisions, not medical alerts.
    """

    # Extreme heat
    if temperature >= 40:
        return "Extreme"

    # High heat
    if temperature >= 35:
        return "High"

    # Moderate heat (only when meaningfully warm)
    if temperature >= 32:
        return "Moderate"

    # Otherwise, considered safe for planning
    return "Safe"


def generate_risk_timeline(hourly_forecast: list) -> dict:
    risk_timeline = []
    temperatures = []
    humidities = []
    high_risk_hours = []
    safe_windows = []

    for hour in hourly_forecast:
        temp = hour["temperature"]
        humidity = hour["humidity"]
        time = hour["time"]

        risk_level = classify_heat_risk(temp, humidity)

        risk_timeline.append({
            "time": time,
            "risk_level": risk_level,
            "temperature": temp,
            "humidity": humidity
        })

        temperatures.append(temp)
        humidities.append(humidity)

        if risk_level in ("High", "Extreme"):
            high_risk_hours.append(time)
        else:
            safe_windows.append(time)

    summary_facts = {
        "max_temperature": round(max(temperatures), 1) if temperatures else None,
        "peak_humidity": round(max(humidities), 1) if humidities else None,
        "high_risk_hours": high_risk_hours,
        "safe_windows": safe_windows
    }

    return {
        "risk_timeline": risk_timeline,
        "summary_facts": summary_facts
    }


def _hour_to_int(time_str: str) -> int:
    return int(time_str[-5:-3])


def derive_planning_decision(risk_timeline: list, intent: str) -> dict:
    high_or_extreme = [
        h for h in risk_timeline
        if h["risk_level"] in ("High", "Extreme")
    ]

    daytime_moderate = [
        h for h in risk_timeline
        if h["risk_level"] == "Moderate"
        and 9 <= _hour_to_int(h["time"]) <= 16
    ]

    # ---------- CONSTRUCTION ----------
    if intent == "construction":
        if len(high_or_extreme) >= 2:
            return {
                "verdict": "AVOID",
                "reason": (
                    "Sustained high or extreme heat poses serious health risks "
                    "for continuous physical labor."
                )
            }

        if len(daytime_moderate) >= 3:
            return {
                "verdict": "MODIFY",
                "reason": (
                    "Prolonged moderate heat during work hours requires enforced "
                    "breaks, hydration, and shaded rest periods."
                )
            }

        return {
            "verdict": "PROCEED",
            "reason": (
                "Conditions are acceptable for outdoor work with standard "
                "heat-safety precautions."
            )
        }

    # ---------- SCHOOL / GENERAL ----------
    if len(high_or_extreme) >= 1:
        return {
            "verdict": "AVOID",
            "reason": (
                "Exposure during high or extreme heat hours is unsafe "
                "for student group activities."
            )
        }

    if len(daytime_moderate) >= 3:
        return {
            "verdict": "MODIFY",
            "reason": (
                "Sustained moderate heat during core activity hours may affect "
                "student comfort; scheduling adjustments are advised."
            )
        }

    return {
        "verdict": "PROCEED",
        "reason": (
            "Forecasted conditions are typical for the region and season. "
            "Standard school trip precautions are sufficient."
        )
    }
