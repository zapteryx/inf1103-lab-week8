FROM python:3.14.7-slim
WORKDIR /app
COPY main.py .
CMD ["python", "main.py"]