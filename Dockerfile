# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api api/

# Set environment variables
ENV GOOD_DATES_ADMIN_API_KEY=change-me-in-production
ENV GOOD_DATES_LOG_LEVEL=INFO

# Expose port
EXPOSE 28000

# Run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "28000"] 