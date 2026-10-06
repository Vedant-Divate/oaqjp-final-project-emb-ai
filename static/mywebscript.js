function analyze() {
  const text = document.getElementById('text').value;
  const resultDiv = document.getElementById('result');
  fetch('/emotionDetector?textToAnalyze=' + encodeURIComponent(text))
    .then((response) => response.text())
    .then((data) => { resultDiv.textContent = data; })
    .catch(() => { resultDiv.textContent = 'Error: could not reach the server.'; });
}
