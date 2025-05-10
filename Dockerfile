FROM python:3.10-slim

# Install ffmpeg and yt-dlp
RUN apt update && apt install -y ffmpeg curl \
 && curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp \
 && chmod a+rx /usr/local/bin/yt-dlp

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
