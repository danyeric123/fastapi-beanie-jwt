# Base image
FROM python:3.9-slim-buster AS base

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY ./myserver .

# Test stage
FROM base AS test
COPY ./tests ./tests
RUN python -m pip install -r tests/requirements.txt
CMD ["pytest"]

# Production stage
FROM base AS prod
EXPOSE 8080
CMD ["uvicorn", "myserver.main:app", "--reload", "--port", "8080"]
