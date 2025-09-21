FROM python:3.11-slim

# Install Node.js & npm
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy generated website for Node setup
COPY generated_website ./generated_website
WORKDIR /app/generated_website
RUN npm install

# Return to app root
WORKDIR /app

# Copy the rest of your app
COPY . .

# Set PORT for Cloud Run
ENV PORT 8080
CMD streamlit run main.py --server.port $PORT --server.address 0.0.0.0

