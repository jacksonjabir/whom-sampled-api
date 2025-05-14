@app.route("/", methods=["POST"])
def download_audio():
    try:
        data = request.get_json()
        print("✅ Received data:", data)

        original_url = data["original_url"]
        sampled_url = data["sampled_url"]
        original_start = data["original_start"]
        sampled_start = data["sampled_start"]

        subprocess.run([
            "yt-dlp", "-x", "--audio-format", "mp3", original_url,
            "--postprocessor-args", f"-ss {original_start} -t 30",
            "-o", "original_sample.%(ext)s"
        ], check=True)

        subprocess.run([
            "yt-dlp", "-x", "--audio-format", "mp3", sampled_url,
            "--postprocessor-args", f"-ss {sampled_start} -t 30",
            "-o", "sampled_track.%(ext)s"
        ], check=True)

        print("✅ Download and conversion complete.")
        return jsonify({"status": "Download complete"}), 200

    except subprocess.CalledProcessError as e:
        print("🚨 yt-dlp failed:", e)
        return jsonify({"error": "Download failed", "details": str(e)}), 500

    except Exception as e:
        print("🚨 Unexpected error:", e)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
