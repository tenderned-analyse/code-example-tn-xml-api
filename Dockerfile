# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# (optioneel) iets strakker qua security
RUN useradd -m -u 10001 appuser

# Dependencies eerst (betere cache)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# App code
COPY tenderned_xml_api_example.py /app/tenderned_xml_api_example.py
COPY tenderned_json_api_example.py /app/tenderned_json_api_example.py
COPY run.py /app/run.py
COPY .env.dist /app/.env.dist

USER appuser

# Use JSON API by default (XML API has limited availability)
CMD ["python", "tenderned_json_api_example.py"]
