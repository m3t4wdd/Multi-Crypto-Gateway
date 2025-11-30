FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    monero \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000


COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]
