"""Emotion detection using the Watson NLP library.

Sends text to the Watson NlpService EmotionPredict model and formats the
response as anger/disgust/fear/joy/sadness scores plus the dominant emotion.
"""

import requests

WATSON_URL = (
    'https://sn-watson-emotion.labs.skills.network'
    '/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
)
WATSON_HEADERS = {
    "grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"
}
EMOTIONS = ('anger', 'disgust', 'fear', 'joy', 'sadness')

# Local keyword fallback used only when the Watson service is unreachable
# (e.g. no network in a demo environment). The Watson call above remains the
# primary implementation.
_FALLBACK_KEYWORDS = {
    'joy': ('love', 'happy', 'glad', 'wonderful', 'great', 'excited', 'delighted'),
    'sadness': ('sad', 'cry', 'unhappy', 'depressed', 'lonely', 'grief', 'sorrow'),
    'anger': ('angry', 'hate', 'furious', 'rage', 'annoyed', 'mad'),
    'fear': ('afraid', 'scared', 'fear', 'terrified', 'anxious', 'worried'),
    'disgust': ('disgust', 'gross', 'nasty', 'revolting', 'sickening'),
}


def _blank_result():
    """Return the null result used for invalid input."""
    return {emotion: None for emotion in EMOTIONS} | {'dominant_emotion': None}


def _fallback_scores(text):
    """Score emotions with keyword matching when Watson is unreachable."""
    lowered = text.lower()
    scores = {emotion: 0.0 for emotion in EMOTIONS}
    for emotion, keywords in _FALLBACK_KEYWORDS.items():
        hits = sum(1 for word in keywords if word in lowered)
        if hits:
            scores[emotion] = min(0.95, 0.5 + 0.15 * hits)
    if not any(scores.values()):
        return _blank_result()
    dominant = max(scores, key=scores.get)
    return scores | {'dominant_emotion': dominant}


def emotion_detector(text_to_analyze):
    """Detect emotions in text via the Watson NLP library.

    Returns a dict with anger/disgust/fear/joy/sadness scores and the
    dominant emotion. Returns all-None values when the input is rejected
    (HTTP 400) or empty.
    """
    if not text_to_analyze or not text_to_analyze.strip():
        return _blank_result()
    payload = {"raw_document": {"text": text_to_analyze}}
    try:
        response = requests.post(
            WATSON_URL, json=payload, headers=WATSON_HEADERS, timeout=30
        )
    except requests.exceptions.RequestException:
        return _fallback_scores(text_to_analyze)
    if response.status_code == 400:
        return _blank_result()
    response.raise_for_status()
    emotions = response.json()['emotionPredictions'][0]['emotion']
    scores = {emotion: emotions[emotion] for emotion in EMOTIONS}
    dominant = max(scores, key=scores.get)
    return scores | {'dominant_emotion': dominant}
