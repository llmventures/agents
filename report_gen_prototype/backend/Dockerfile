# Stage 1: Base build stage
FROM python:3.11-slim AS builder

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    gcc python3-dev\
    g++ \
    make \
    clang \
    libatlas-base-dev \
    liblapack-dev \
    libopenblas-dev \
    libfreetype6-dev \
    pkg-config \
    libpng-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create the app directory
RUN mkdir /app
 
# Set the working directory
WORKDIR /app
 
# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
# Install dependencies first for caching benefit
RUN pip install --upgrade pip 
COPY requirements.txt /app/ 
RUN pip install --no-cache-dir -r requirements.txt

RUN echo "Listing contents of /usr/:" && ls -al /usr/
# Stage 2: Production stage
FROM python:3.11-slim AS production
 
RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app
 
# Copy the Python dependencies from the builder stage

COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
 
# Set the working directory
WORKDIR /app
 
# Copy application code
COPY --chown=appuser:appuser . .
 
# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
# Switch to non-root user
USER appuser
 
# Expose the application port
EXPOSE 8000 
