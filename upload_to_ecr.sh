#!/bin/bash

# Set variables
REPOSITORY_NAME="tuamnuq-liar-detect-app"
AWS_REGION="us-east-1"
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)

# Full ECR Public URI (use public.ecr for public repositories)
ECR_PUBLIC_URI="public.ecr.aws/$ACCOUNT_ID/$REPOSITORY_NAME"

# Authenticate Docker to ECR Public
echo "Authenticating Docker with ECR Public..."
if ! aws ecr-public get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin public.ecr.aws; then
  echo "Docker authentication failed!"
  exit 1
fi

# Check if the public repository exists, create it if not
echo "Checking if ECR Public repository exists..."
if ! aws ecr-public describe-repositories --repository-name $REPOSITORY_NAME --region $AWS_REGION >/dev/null 2>&1; then
  echo "Public repository does not exist. Creating ECR Public repository..."
  if
    ! aws ecr-public create-repository --repository-name $REPOSITORY_NAME --region $AWS_REGION --catalog-data file://repository-description.json >/dev/null
  then
    echo "Failed to create the public repository!"
    exit 1
  fi
fi

# Tag the Docker image
echo "Tagging Docker image..."
docker tag liar-detect-app:latest "$ECR_PUBLIC_URI":latest

# Push the image to ECR Public
echo "Pushing Docker image to ECR Public..."
if ! docker push "$ECR_PUBLIC_URI":latest; then
  echo "Failed to push the Docker image to ECR Public!"
  exit 1
fi

echo "Docker image successfully pushed to ECR Public!"
