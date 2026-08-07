# ==========================
# Base Stage
# ==========================
FROM python:3.11.2-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt

# ==========================
# Development Stage
# ==========================
FROM base AS development

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# ==========================
# Test Stage
# ==========================
FROM development AS test

CMD ["pytest", "-vv"]


# ==========================
# Production Stage
# ==========================
FROM base AS production

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]