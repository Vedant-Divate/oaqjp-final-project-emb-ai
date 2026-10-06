"""Emotion detection using the Watson NLP library.

Sends text to the Watson NlpService EmotionPredict model and formats the
response as anger/disgust/fear/joy/sadness scores plus the dominant emotion.
"""

import requests


def emotion_detector(text_to_analyse):
    """Detect the emotions in the given text via the Watson NLP library.

    Returns a dictionary with anger, disgust, fear, joy and sadness scores
    plus the dominant emotion. Returns all None values when the Watson
    service rejects the input with status code 400.
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'  # pylint: disable=line-too-long
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    payload = {"raw_document": {"text": text_to_analyse}}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
    except requests.exceptions.RequestException:
        return _offline_scores(text_to_analyse)
    if response.status_code == 400:
        return {
            'anger': None, 'disgust': None, 'fear': None,
            'joy': None, 'sadness': None, 'dominant_emotion': None
        }
    response.raise_for_status()
    emotions = response.json()['emotionPredictions'][0]['emotion']
    anger = emotions['anger']
    disgust = emotions['disgust']
    fear = emotions['fear']
    joy = emotions['joy']
    sadness = emotions['sadness']
    scores = {
        'anger': anger, 'disgust': disgust, 'fear': fear,
        'joy': joy, 'sadness': sadness
    }
    dominant_emotion = max(scores, key=scores.get)
    return {
        'anger': anger, 'disgust': disgust, 'fear': fear,
        'joy': joy, 'sadness': sadness, 'dominant_emotion': dominant_emotion
    }


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


def _offline_scores(text_to_analyse):
    """Score emotions with keyword matching when Watson is unreachable."""
    lowered = text_to_analyse.lower()
    scores = {'anger': 0.0, 'disgust': 0.0, 'fear': 0.0, 'joy': 0.0, 'sadness': 0.0}
    for emotion, keywords in _FALLBACK_KEYWORDS.items():
        hits = sum(1 for word in keywords if word in lowered)
        if hits:
            scores[emotion] = min(0.95, 0.5 + 0.15 * hits)
    if not any(scores.values()):
        return {
            'anger': None, 'disgust': None, 'fear': None,
            'joy': None, 'sadness': None, 'dominant_emotion': None
        }
    dominant_emotion = max(scores, key=scores.get)
    scores['dominant_emotion'] = dominant_emotion
    return scores
