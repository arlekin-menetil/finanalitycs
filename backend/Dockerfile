FROM python:3.11

# =========================
# SYSTEM DEPENDENCIES 💣
# =========================
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libffi-dev \
    libssl-dev \
    curl \
    wget \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcb1 \
    libx11-6 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrender1 \
    libxcursor1 \
    libdbus-1-3 \
    libglib2.0-0 \
    libegl1 \
    libgl1 \
    libopengl0 \
    libwoff1 \
    libjpeg62-turbo \
    libwebp7 \
    libx264-dev \
    libpcre2-8-0 \
    libsecret-1-0 \
    && rm -rf /var/lib/apt/lists/*

# =========================
# ENV
# =========================
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# =========================
# PYTHON DEPENDENCIES
# =========================
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install playwright

# =========================
# COPY PROJECT
# =========================
COPY . .

# =========================
# START 💣
# =========================
CMD bash -c "python -m playwright install chromium && python manage.py runserver 0.0.0.0:8000"