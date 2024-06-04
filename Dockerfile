FROM python:3.10-alpine

WORKDIR /app

COPY . /app

RUN pip install asyncpg
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
