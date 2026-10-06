# Emotion Detector – Final Project

AI-based web application (Final Project) that detects emotions (anger, disgust, fear, joy,
sadness) in text using the **Watson NLP library** (`NlpService EmotionPredict`)
with a Flask web deployment.

## Project layout

- `EmotionDetection/emotion_detection.py` – `emotion_detector()` using Watson NLP
- `EmotionDetection/__init__.py` – package import for the application module
- `server.py` – Flask deployment (`/` home, `/emotionDetector` API with blank-input handling)
- `test_emotion_detection.py` – unit tests (mocked Watson API)
- `templates/index.html`, `static/mywebscript.js` – web interface

## Run

```bash
pip install -r requirements.txt
python server.py
# open http://localhost:5000
```

## Test

```bash
python -m unittest test_emotion_detection -v
```

## Static analysis

```bash
pylint server.py EmotionDetection/emotion_detection.py
```

By Vedant Divate — Coursera Final Project: Emotion Detector.
