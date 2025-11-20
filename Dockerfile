# Use the official Python image.
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Set the working directory inside the container
ENV APP_HOME /app
WORKDIR $APP_HOME

# --- CRITICAL CHANGE HERE ---
# Copy the requirements from the 'backend' folder to the container
COPY backend/requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main application code from the 'backend' folder
COPY backend/main.py ./
# ----------------------------

# Run the web service on container startup.
CMD exec functions-framework --target=log_submission --port=$PORT