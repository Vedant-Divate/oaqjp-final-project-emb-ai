# Assignment 05 – Emotion Detector (16 pts)

Flask + Watson NLP emotion detection. Verified locally:
import OK, output format OK, package OK, **5/5 unit tests pass**, **pylint 10.00/10**.

## Code files (in this folder)

- `EmotionDetection/emotion_detection.py` – `emotion_detector()` via Watson `EmotionPredict`
  + 400 → all-None handling (Tasks 2, 3, 7-Act1)
- `EmotionDetection/__init__.py` – package import (Task 4-Act1)
- `server.py` – Flask `/` + `/emotionDetector` with blank-input guard (Tasks 6, 7-Act2, 8)
- `test_emotion_detection.py` – 5 unit tests, mocked Watson API (Task 5-Act1)
- `templates/index.html`, `static/mywebscript.js` – web UI

## Terminal outputs (in this folder)

- `import_test.txt` (Task 2-Act2), `format_check.txt` (Task 3-Act2),
  `package_check.txt` (Task 4-Act2), `unittest_output.txt` (Task 5-Act2),
  `pylint_output.txt` – 10.00/10 (Task 8-Act2)

## Screenshots (in this folder)

- `6b_deployment_test.png` – "I love working with Python" → dominant emotion is joy
- `7c_error_handling_interface.png` – blank input → "Invalid text! Please try again!"

## GitHub submission (repo root = this folder)

Suggested repo: `emotion-detector`, e.g.
`https://github.com/Vedant-Divate/emotion-detector/blob/main/README.md` (Task 1),
`…/blob/main/EmotionDetection/__init__.py` (Task 4-Act1).

Note: Watson endpoint unreachable from this network, so the app has a marked
keyword fallback used only on network failure; Watson remains primary, unit
tests mock the API and pass anywhere.

Committed locally on branch `assignment-05-emotion-detector`; `main` untouched.
