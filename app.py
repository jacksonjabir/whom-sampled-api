from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def homepage():
    return "🚉 Your Flask webhook is live. Send a POST to use it.", 200

@app.route("/", methods=["POST"])
def download_audio():
    try:
        data = request.get_json()
        original_url = data["original_url"]
        sampled_url = data["sampled_url"]
        original_start = data["original_start"]
        sampled_start = data["sampled_start"]

        subprocess.run([
            "yt-dlp", "--cookies", "cookies.txt", "-x", "--audio-format", "mp3", original_url,
            "--postprocessor-args", f"-ss {original_start} -t 30",
            "-o", "original_sample.%(ext)s"
        ], check=True)

        subprocess.run([
            "yt-dlp", "--cookies", "cookies.txt", "-x", "--audio-format", "mp3", sampled_url,
            "--postprocessor-args", f"-ss {sampled_start} -t 30",
            "-o", "sampled_track.%(ext)s"
        ], check=True)

        return jsonify({"status": "Download complete"}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Download failed", "details": str(e)}), 500
