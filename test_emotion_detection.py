"""Unit tests for the EmotionDetection application (mocked Watson API)."""

import unittest
from unittest.mock import patch

from EmotionDetection.emotion_detection import emotion_detector


def _watson_response(emotions):
    """Build a fake Watson EmotionPredict response object."""

    class FakeResponse:
        """Minimal stand-in for requests.Response."""

        status_code = 200

        def json(self):
            """Return canned emotion predictions."""
            return {'emotionPredictions': [{'emotion': emotions}]}

        def raise_for_status(self):
            """Mimic a successful status check."""

    return FakeResponse()


JOY = {'anger': 0.05, 'disgust': 0.02, 'fear': 0.03, 'joy': 0.92, 'sadness': 0.04}
SADNESS = {'anger': 0.04, 'disgust': 0.03, 'fear': 0.08, 'joy': 0.02, 'sadness': 0.89}
ANGER = {'anger': 0.9, 'disgust': 0.2, 'fear': 0.1, 'joy': 0.01, 'sadness': 0.05}


class TestEmotionDetector(unittest.TestCase):
    """Test the emotion_detector function output format and values."""

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_joy_detected(self, mock_post):
        """Joyful text returns joy as the dominant emotion."""
        mock_post.return_value = _watson_response(JOY)
        result = emotion_detector('I am glad this happened')
        self.assertEqual(result['dominant_emotion'], 'joy')
        self.assertAlmostEqual(result['joy'], 0.92)

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_sadness_detected(self, mock_post):
        """Sad text returns sadness as the dominant emotion."""
        mock_post.return_value = _watson_response(SADNESS)
        result = emotion_detector('I am really sad about this')
        self.assertEqual(result['dominant_emotion'], 'sadness')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_anger_detected(self, mock_post):
        """Angry text returns anger as the dominant emotion."""
        mock_post.return_value = _watson_response(ANGER)
        result = emotion_detector('I am so angry about this')
        self.assertEqual(result['dominant_emotion'], 'anger')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_output_format(self, mock_post):
        """Result contains all five scores plus the dominant emotion."""
        mock_post.return_value = _watson_response(JOY)
        result = emotion_detector('I am glad this happened')
        for key in ('anger', 'disgust', 'fear', 'joy', 'sadness', 'dominant_emotion'):
            self.assertIn(key, result)

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_bad_request_returns_nones(self, mock_post):
        """HTTP 400 from Watson yields all-None values."""
        mock_post.return_value.status_code = 400
        result = emotion_detector('???')
        self.assertTrue(all(value is None for value in result.values()))


if __name__ == '__main__':
    unittest.main()
