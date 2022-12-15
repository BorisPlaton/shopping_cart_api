FROM python:3.10.4

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.dev.txt .
RUN pip install --no-cache-dir -r requirements.dev.txt && rm -f requirements.dev.txt

COPY ./scripts/entrypoint.sh .
ENTRYPOINT ["sh", "entrypoint.sh"]

COPY ./shopping_cart_api .