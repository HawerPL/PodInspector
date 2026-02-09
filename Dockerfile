FROM python:3.11-slim
LABEL AUTHOR=HawerPL

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

RUN useradd -m podinspector \
    && chown podinspector:podinspector -R /app
USER podinspector

HEALTHCHECK CMD curl -f http://localhost:8080/healthz || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]