import json
import re
from typing import Any, Dict, Optional

import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_MODEL = "llama3:latest"


def _strip_markdown_code_blocks(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_ai_summary(check_type: str, source: str, description: str, severity: str, trigger_data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, str]]:
    prompt = (
        "You are a data quality investigator. "
        f"Incident: check_type={check_type}, source={source}, severity={severity}. "
        f"Description: {description}. "
        f"Trigger data: {json.dumps(trigger_data or {}, default=str)}. "
        "Return ONLY a JSON object with these exact keys: likely_cause, impact, suggested_fix. "
        "Keep each value concise and actionable."
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": DEFAULT_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=45,
        )
        response.raise_for_status()
        payload = response.json()
        text = payload.get("response", "")
        cleaned = _strip_markdown_code_blocks(text)
        parsed = json.loads(cleaned)
        return {
            "likely_cause": str(parsed.get("likely_cause", "")),
            "impact": str(parsed.get("impact", "")),
            "suggested_fix": str(parsed.get("suggested_fix", "")),
        }
    except Exception:
        return None
