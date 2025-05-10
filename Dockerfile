FROM python:3.10-slim

# Install ffmpeg and yt-dlp
RUN apt update && apt install -y ffmpeg curl \
 && curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp \
 && chmod a+rx /usr/local/bin/yt-dlp

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose the port Railway expects
EXPOSE 8080

# Start the app using gunicorn (entry point is app.py -> app)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
