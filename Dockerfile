FROM python:3.14-slim

WORKDIR /app

ENV PORT=80

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-80} app:app"]