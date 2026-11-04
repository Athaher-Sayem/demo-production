FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements-production.txt .
RUN pip install --no-cache-dir -r requirements-production.txt
COPY . .
RUN chmod +x entrypoint.sh
EXPOSE 8000
CMD ["sh", "entrypoint.sh"]