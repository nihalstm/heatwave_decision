# schemas.py

from pydantic import BaseModel
from typing import List, Dict, Optional


class PlanningRequest(BaseModel):
    location: str                      # Human-readable location
    date: str                          # YYYY-MM-DD
    time: Optional[str] = None         # HH:MM (optional)
    activity_description: str          # Free-text activity description


class RiskEntry(BaseModel):
    time: str
    risk_level: str
    temperature: float
    humidity: float


class DecisionSummary(BaseModel):
    verdict: str                       # PROCEED / MODIFY / AVOID
    reason: str                        # Short, deterministic justification


class PlanningResponse(BaseModel):
    location: str
    intent: str
    decision: DecisionSummary
    focused_time: Optional[str]
    focused_hour_context: Optional[Dict]
    risk_timeline: List[RiskEntry]
    summary_facts: Dict
    planning_explanation: str
