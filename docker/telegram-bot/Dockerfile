FROM python:3.12-slim

WORKDIR /app
COPY bot.py .

RUN pip install --no-cache-dir python-telegram-bot

CMD ["python", "bot.py"]
