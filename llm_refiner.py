"""
llm_refiner.py

Optional LLM-based explanation elaboration using Bytez.
LLM is strictly limited to language refinement.
Fails safely to deterministic explanation.
"""

import os
from bytez import Bytez


SYSTEM_PROMPT = (
    "You are a technical writing assistant.\n"
    "You must NOT change facts, numbers, verdicts, or risk levels.\n"
    "You must NOT add new advice, risks, or interpretations.\n"
    "You may ONLY rephrase the provided explanation to improve clarity, "
    "professional tone, and readability.\n"
    "If unsure, return the text unchanged."
)


def refine_explanation_with_llm(
    base_explanation: str,
    decision: dict,
    summary_facts: dict
) -> str:
    """
    Refine explanation language using Bytez-hosted LLM.
    Deterministic output remains the source of truth.
    """

    api_key = os.getenv("BYTEZ_API_KEY")
    if not api_key:
        return base_explanation

    try:
        sdk = Bytez(api_key)
        model = sdk.model("google/gemma-3-1b-it")


        user_prompt = (
            f"Decision verdict: {decision.get('verdict')}\n"
            f"Decision reason: {decision.get('reason')}\n\n"
            f"Summary facts:\n"
            f"- Max temperature: {summary_facts.get('max_temperature')}°C\n"
            f"- Peak humidity: {summary_facts.get('peak_humidity')}%\n"
            f"- High-risk hours: {summary_facts.get('high_risk_hours')}\n\n"
            f"Base explanation:\n{base_explanation}"
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]

        result = model.run(messages)

        if result.error or not result.output:
            return base_explanation

        return result.output.strip() + "\n\n[LLM REFINEMENT ACTIVE]"


    except Exception:
        return base_explanation
