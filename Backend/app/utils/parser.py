import json
import re
from typing import Any, Dict, Optional

def extract_json_from_llm(raw_text: str) -> Optional[Dict[str, Any]]:
    if not raw_text:
        return None

    text = raw_text.strip()

    markdown_json_pattern = r"```(?:json)?\s*(\{[\s\S]*?\})\s*```"
    match = re.search(markdown_json_pattern, text)
    
    if match:
        json_content = match.group(1)
    else:
        start_idx = text.find("{")
        end_idx = text.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_content = text[start_idx : end_idx + 1]
        else:
            json_content = text

    try:
        return json.loads(json_content)
    except json.JSONDecodeError:
        try:
            sanitized = re.sub(r",\s*([\]}])", r"\1", json_content)
            return json.loads(sanitized)
        except json.JSONDecodeError:
            return None


def parse_llm_budget_estimation(raw_cost_text: str) -> float:
    if not raw_cost_text:
        return 0.0
        
    numbers = "".join(re.findall(r"\d+", raw_cost_text))
    try:
        return float(numbers) if numbers else 0.0
    except ValueError:
        return 0.0