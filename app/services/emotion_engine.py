from typing import Dict, List

EMOTION_KEYWORDS = {
    "sadness": ["sad", "empty", "cry", "lonely", "down"],
    "anxiety": ["worried", "panic", "anxious", "scared", "nervous"],
    "frustration": ["frustrated", "annoyed", "stuck", "irritated"],
    "stress": ["stressed", "pressure", "overwhelmed", "burnout"],
    "anger": ["angry", "furious", "mad", "rage"],
}


def detect_emotions(message: str) -> Dict[str, object]:
    text = message.lower()
    detected: List[Dict[str, object]] = []
    for emotion, words in EMOTION_KEYWORDS.items():
        hits = [word for word in words if word in text]
        if hits:
            detected.append({"emotion": emotion, "confidence": min(0.55 + 0.15 * len(hits), 0.95), "hits": hits})
    return {"detected": detected, "primary": detected[0]["emotion"] if detected else "neutral"}
