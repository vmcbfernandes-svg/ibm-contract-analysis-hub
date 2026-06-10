# Hugging Face Deployment Fix

## Issue
The initial build failed with error:
```
ERROR: process "/bin/sh -c apt-get update && apt-get install -y build-essential curl software-properties-common && rm -rf /var/lib/apt/lists/*" did not complete successfully: exit code: 100
```

## Solution
Updated Dockerfile to remove `software-properties-common` which is not needed and causing the build failure.

## Steps to Fix

1. **Go to your Hugging Face Space:**
   https://huggingface.co/spaces/vitorfernandes1969/ibm-contract-analysis-hub

2. **Click on "Files" tab**

3. **Click on "Dockerfile"** to open it

4. **Click the "Edit" button** (pencil icon)

5. **Replace the entire content** with the new Dockerfile (see below)

6. **Click "Commit changes to main"**

7. **Wait 5-10 minutes** for the rebuild to complete

## New Dockerfile Content

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port (Hugging Face uses 7860)
EXPOSE 7860

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=7860
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Health check
HEALTHCHECK CMD curl --fail http://localhost:7860/_stcore/health

# Run the application
CMD ["streamlit", "run", "contract_analysis_app.py", "--server.port=7860", "--server.address=0.0.0.0"]
```

## What Changed
- Removed `software-properties-common` package (not needed)
- Kept only essential packages: `build-essential` and `curl`
- Added health check for better monitoring
- Optimized Docker layer caching

## Expected Result
After committing the changes, the build should complete successfully in 5-10 minutes and your app will be live at:
https://huggingface.co/spaces/vitorfernandes1969/ibm-contract-analysis-hub