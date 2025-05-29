FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    wget curl unzip libglib2.0-0 libnss3 libgdk-pixbuf2.0-0 libgtk-3-0 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libasound2 libxss1 \
    libxtst6 fonts-liberation libappindicator3-1 xdg-utils \
    && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install

COPY . /app
WORKDIR /app

CMD ["python", "aviso_bot.py"]
