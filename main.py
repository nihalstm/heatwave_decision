# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

from schemas import PlanningRequest
from weather_client import fetch_hourly_forecast
from geocoding_client import geocode_location
from risk_engine import generate_risk_timeline, derive_planning_decision
from llm_client import generate_planning_explanation
from pdf_generator import generate_planning_pdf
from nlp.intent_detector import detect_intent

import os


app = FastAPI(
    title="Heatwave Decision Support API",
    version="1.2.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# -------- UI SERVING --------
@app.get("/ui", response_class=HTMLResponse)
def serve_ui():
    with open(
        os.path.join(BASE_DIR, "static", "index.html"),
        "r",
        encoding="utf-8"
    ) as f:
        return f.read()


# -------- CORS --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def find_hour_context(risk_timeline: list, time_str: str | None):
    """
    Find the risk entry closest to the requested hour.
    Expected time_str format: HH:MM
    """
    if not time_str:
        return None

    target_hour = time_str.split(":")[0]

    for entry in risk_timeline:
        if entry["time"].endswith(f"{target_hour}:00"):
            return entry

    return None


# -------- HEALTH CHECK --------
@app.get("/")
def health_check():
    return {"status": "ok"}


# -------- MAIN JSON ENDPOINT --------
@app.post("/heatwave/planning")
def generate_planning_insight(request: PlanningRequest):
    # --- Geocode location ---
    geo = geocode_location(request.location)
    if not geo:
        raise HTTPException(status_code=404, detail="Location not found")

    # --- Fetch forecast ---
    forecast = fetch_hourly_forecast(
        geo["latitude"],
        geo["longitude"],
        request.date
    )
    if not forecast:
        raise HTTPException(status_code=404, detail="No forecast data available")

    # --- NLP intent detection ---
    intent = detect_intent(request.activity_description)

    # --- Risk analysis ---
    result = generate_risk_timeline(forecast)

    # --- Planning decision ---
    decision = derive_planning_decision(
        risk_timeline=result["risk_timeline"],
        intent=intent
    )

    # --- Optional time focus ---
    hour_context = find_hour_context(
        result["risk_timeline"],
        request.time
    )

    # --- Deterministic explanation (SOURCE OF TRUTH) ---
    explanation = generate_planning_explanation(
        summary_facts=result["summary_facts"],
        intent=intent,
        activity_description=request.activity_description,
        hour_context=hour_context
    )

    return {
        "location": geo["display_name"],
        "intent": intent,
        "decision": decision,
        "focused_time": request.time,
        "focused_hour_context": hour_context,
        "risk_timeline": result["risk_timeline"],
        "summary_facts": result["summary_facts"],
        "planning_explanation": explanation
    }


# -------- PDF ENDPOINT --------
@app.post("/heatwave/planning/pdf")
def generate_planning_pdf_endpoint(request: PlanningRequest):
    # --- Geocode location ---
    geo = geocode_location(request.location)
    if not geo:
        raise HTTPException(status_code=404, detail="Location not found")

    # --- Fetch forecast ---
    forecast = fetch_hourly_forecast(
        geo["latitude"],
        geo["longitude"],
        request.date
    )
    if not forecast:
        raise HTTPException(status_code=404, detail="No forecast data available")

    # --- NLP intent ---
    intent = detect_intent(request.activity_description)

    # --- Risk analysis ---
    result = generate_risk_timeline(forecast)

    # --- Planning decision ---
    decision = derive_planning_decision(
        risk_timeline=result["risk_timeline"],
        intent=intent
    )

    # --- Optional time focus ---
    hour_context = find_hour_context(
        result["risk_timeline"],
        request.time
    )

    # --- Deterministic explanation ---
    explanation = generate_planning_explanation(
        summary_facts=result["summary_facts"],
        intent=intent,
        activity_description=request.activity_description,
        hour_context=hour_context
    )

    file_path = "heatwave_planning_summary.pdf"

    generate_planning_pdf(
        file_path=file_path,
        location=geo["display_name"],
        date=request.date,
        summary_facts=result["summary_facts"],
        decision=decision,
        explanation=explanation,
        intent=intent
    )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename="heatwave_planning_summary.pdf"
    )
