# Base Python image
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Return to app root
WORKDIR /app

# Copy the rest of the Python app
COPY . .

# Set PORT for Cloud Run
ENV PORT 8080
CMD streamlit run main.py --server.port $PORT --server.address 0.0.0.0
