FROM python:3.11-slim

# Install ffmpeg which is required by yt-dlp
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose port (Render sets PORT env variable, defaulting to 10000)
ENV PORT=10000
EXPOSE 10000

# Run gunicorn, listening on all interfaces (0.0.0.0) and dynamically picking port
CMD gunicorn -w 1 --threads 4 -b 0.0.0.0:$PORT "app:app"
