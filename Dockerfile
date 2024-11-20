# Use a Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy Pipfile
COPY Pipfile Pipfile.lock /app/

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && \
    pip install --upgrade pip --no-cache-dir && \
    pip install pipenv --no-cache-dir && \
    pipenv install --deploy && \
    apt-get remove -y build-essential && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the src directory and models directory
COPY ./src /app/src
COPY ./models /app/models
# Add src directory to PYTHONPATH (ensures common_feature imports work)
ENV PYTHONPATH="/app/src:$PYTHONPATH"

# Expose the Flask app port
EXPOSE 5042

# Command to run the application
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:5042", "src.predict:app"]
