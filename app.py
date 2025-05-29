from flask import Flask, request, jsonify
import subprocess
import os
import datetime

app = Flask(__name__)

def make_instagram_video():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"whomsampled_{timestamp}.mp4"
    command = [
        "ffmpeg", "-y",
        "-i", "original_sample.mp3",
        "-i", "sampled_track.mp3",
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[out]",
        "-map", "[out]",
        output_file
    ]
    subprocess.run(command, check=True)
    return output_file

@app.route("/", methods=["GET"])
def homepage():
    return "Your Flask webhook is live. Send a POST to use it.", 200

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

        output_video = make_instagram_video()

        return jsonify({
            "status": "Download and video creation complete",
            "video_file": output_video
        }), 200

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Download failed", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
