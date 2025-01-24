#!/bin/bash

# PROJECT_ID="baas-web-content"   # Replace with your Google Cloud project ID
# SERVICE_NAME="media-agent"    # Replace with the desired Cloud Run service name

# Import variables
# get location of currect script file
CURRENT_LOCATION=$(dirname "$0")

# Import variables
source ${CURRENT_LOCATION}/variables.sh

# define variables
IMAGE_URL="gcr.io/$PROJECT_ID/$SERVICE_NAME"  # Image URL for GCR
SERVICE_ACCOUNT_NAME=${SERVICE_NAME}-service-account

# Authenticate using service account
gcloud auth activate-service-account --key-file=${CURRENT_LOCATION}/${SERVICE_ACCOUNT_NAME}.json --project=${PROJECT_ID}

# Create repository with explicit project and location
gcloud artifacts repositories create "$SERVICE_NAME-repo" --repository-format=docker  --project="$PROJECT_ID"  --location=${REGION}


# Check if the service already exists
EXISTING_SERVICE=$(gcloud run services describe "$SERVICE_NAME" --project "$PROJECT_ID" --format="value(status.url)" 2>/dev/null)

if [ -z "$EXISTING_SERVICE" ]; then
  # The service does not exist, so create the Docker image repository on GCR
  gcloud artifacts repositories create "$SERVICE_NAME-repo" --repository-format=docker --location=${REGION} --platform=managed

#   # Build and push the Docker image to GCR
#   gcloud builds submit --tag="$IMAGE_URL" .

#   # Deploy the Cloud Run service
#   gcloud run deploy "$SERVICE_NAME" \
#     --image="$IMAGE_URL" \
#     --platform=managed \
#     --region=us-central1  # Replace with your desired region
else
  echo "Service '$SERVICE_NAME' already exists."
fi
