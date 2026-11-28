FROM python:3.14-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.14-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
ENV UVICORN_PORT=8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]