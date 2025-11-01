FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN echo "micro_service_programming Graduation Verdiction AI Chatbot" > README.md && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi