# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
# (This reads your requirements.txt file)
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup.
# We use the functions-framework to listen to requests, just like Cloud Functions does.
CMD exec functions-framework --target=log_submission --port=$PORT