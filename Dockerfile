# Lightweight Python base image
FROM python:3.13-slim

# Install system deps (if needed by some libs). Keep minimal.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Copy dependency manifests first for better caching
COPY requirements.txt ./

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose default Gradio port
EXPOSE 7860

# Default to production-friendly Gradio binding
ENV PORT=7860

# Start the app
CMD ["python", "app.py"]
