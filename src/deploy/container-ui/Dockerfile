# Use a minimal Python image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY ../../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire source code into the container
COPY ../../src ./src

# Set environment variables
ENV PYTHONPATH=/app/src

# Expose Streamlit default port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "src/UI/main.py", "--server.headless=true", "--server.port=8501", "--server.enableCORS=false"]
