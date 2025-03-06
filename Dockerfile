FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    libssl-dev \
    gcc \
    libjpeg-dev \
    libpng-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies - use pip wheel to avoid compilation issues
RUN pip install --upgrade pip && \
    pip install wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port for the application
EXPOSE 5000

# Run command
CMD ["flask", "run", "--host=0.0.0.0"]
