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

# Copy model and inference endpoint
COPY ./src/predict.py /app
COPY ./models/model.pickle /app
# Command to run the application
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:5042", "app:app"]
