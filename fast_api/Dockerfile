FROM python:3.9-slim

WORKDIR /app

COPY . /app

COPY ./data /app/data

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV HOST 0.0.0.0
ENV OPENAI_API_KEY=""

CMD ["uvicorn", "backend_service:app", "--host", "0.0.0.0", "--port", "8000"]
