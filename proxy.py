from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

@app.route("/ai-helper")
def proxy_streamlit():
    return """
    <iframe src="http://127.0.0.1:8501" width="100%" height="800px" style="border:none;"></iframe>
    """

if __name__ == "__main__":
    app.run(port=5000)
