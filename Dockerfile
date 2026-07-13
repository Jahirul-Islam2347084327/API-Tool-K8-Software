FROM python:3.10.20-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
RUN groupadd appgroup
RUN useradd -g appgroup appuser
RUN chown -R appuser:appgroup /app
USER appuser
EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0" ]