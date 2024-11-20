# Use a Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /app/

# Install pipenv
RUN pip install pipenv

# Install dependencies
RUN pipenv install --deploy --system

# Copy the src directory and models directory
COPY ./src /app/src
COPY ./models /app/models
# Add src directory to PYTHONPATH (ensures common_feature imports work)
ENV PYTHONPATH="/app/src:$PYTHONPATH"

# Expose the Flask app port
EXPOSE 5042

# Command to run the application
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:5042", "src.predict:app"]
