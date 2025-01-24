#! /bin/bash

# This script creates a service account and a key for the service account
# It also sets the run.admin role for the service account


# get location of currect script file
CURRENT_LOCATION=$(dirname "$0")
# Import variables
source ${CURRENT_LOCATION}/variables.sh

SERVICE_ACCOUNT_NAME=${SERVICE_NAME}-service-account

SERVICE_ACCOUNT_ID=${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

# Create service account
# check if service account already exists
echo "Checking if service account ${SERVICE_ACCOUNT_ID} exists"

gcloud iam service-accounts describe ${SERVICE_ACCOUNT_ID} --project=${PROJECT_ID}
if [ $? -eq 0 ]; then
    echo "Service account ${SERVICE_ACCOUNT_NAME} already exists"
else
    echo "Service account ${SERVICE_ACCOUNT_NAME} does not exist"
    gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} --project=${PROJECT_ID} --display-name="${SERVICE_NAME}-service-account"
fi

#check if service account key already exists
echo "Checking if service account key ${SERVICE_ACCOUNT_NAME}.json exists locally"
ls -l ${SERVICE_ACCOUNT_NAME}.json

#gcloud iam service-accounts keys describe ${SERVICE_ACCOUNT_NAME}.json --project=${PROJECT_ID} --iam-account=${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
if [ $? -eq 0 ]; then
    echo "Service account key ${SERVICE_ACCOUNT_NAME}.json already exists"
else
    echo "Service account key ${SERVICE_ACCOUNT_NAME}.json does not exist. Creating it now..."
    gcloud iam service-accounts keys create ${SERVICE_ACCOUNT_NAME}.json --project=${PROJECT_ID} --iam-account=${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
fi


# echo "Run.admin role is not set for service account ${SERVICE_ACCOUNT_NAME}. Setting it now..."
# NOTE: These permissions need to be set by the project owner
# gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@$PROJECT_ID.iam.gserviceaccount.com" --role="roles/run.admin"
# gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@$PROJECT_ID.iam.gserviceaccount.com" --role="roles/artifactregistry.admin"
# gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@$PROJECT_ID.iam.gserviceaccount.com" --role="artifactregistry.repositories.create"
