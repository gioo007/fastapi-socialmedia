FROM  python:3.13.5
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"] 
#inside port of container, hardcoded for testing, but should be $PORT in production (Railway/Render)

