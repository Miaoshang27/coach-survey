# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .streamlit config directory
COPY .streamlit/ .streamlit/

# Copy the rest of the application source code
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Set the command to run the Streamlit app
# The --server.runOnSave=false flag is recommended for production
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.headless=true", "--server.runOnSave=false"]

