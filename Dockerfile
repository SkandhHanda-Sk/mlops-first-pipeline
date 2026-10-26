# Start with a lightweight Python image
# This gives our container a Python runtime environment without unnecessary bloat

FROM python:3.14-slim

# Set the working directory inside the container
WORKDIR /app 

# Copy the requirements file into the container
COPY requirements.txt .

# avoid retaining pip's download cache in the image
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and saved model into /app
COPY . .

# Document the port used by FastAPI application
EXPOSE 8000

# Start the API server when the container launches
# 0.0.0.0 allows connections through the contaner's network interface
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]