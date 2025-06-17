FROM python3.11-slim
LABEL AUTHOR=HawerPL

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]