import re
from typing import Dict, List

DIAGNOSIS_PATTERNS: List[str] = [
    r"\bdiagnose me\b",
    r"\bdo i have depression\b",
    r"\bam i depressed\b",
    r"\bwhat disorder do i have\b",
    r"\bam i clinically depressed\b",
    r"\btell me my diagnosis\b",
]

MEDICATION_PATTERNS: List[str] = [
    r"\bwhat medicine should i take\b",
    r"\bprescribe\b",
    r"\bwhich antidepressant\b",
    r"\bhow much dosage\b",
]

FIXED_DIAGNOSIS_RESPONSE = "I do not diagnose medical conditions."


def check_legal_boundary(message: str) -> Dict[str, object]:
    diagnosis_matches = [p for p in DIAGNOSIS_PATTERNS if re.search(p, message, flags=re.IGNORECASE)]
    medication_matches = [p for p in MEDICATION_PATTERNS if re.search(p, message, flags=re.IGNORECASE)]
    triggered = bool(diagnosis_matches or medication_matches)
    return {
        "triggered": triggered,
        "diagnosis_matches": diagnosis_matches,
        "medication_matches": medication_matches,
        "response": FIXED_DIAGNOSIS_RESPONSE if triggered else None,
    }
