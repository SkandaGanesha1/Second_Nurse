FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.lock /app/requirements.lock
RUN pip install --no-cache-dir -r requirements.lock
COPY . /app
RUN useradd --uid 10001 --create-home appuser && chown -R appuser:appuser /app
USER appuser
ENV PORT=3000
EXPOSE 3000
CMD ["sh", "-c", "uvicorn server.app:app --host 0.0.0.0 --port ${PORT:-3000}"]
