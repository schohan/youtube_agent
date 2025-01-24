# deploy-google-cloud-run.sh
# 
# This script is used to deploy the Media Research & Content Creation API to Google Cloud Run.
# It will build the Docker image, push it to Google Container Registry, and deploy it to Google Cloud Run.
# 
# Usage:
# ./deploy-google-cloud-run.sh
# 
# Prerequisites:
# - Google Cloud SDK
# - Docker
# - gcloud CLI
# - kubectl CLI
# - git
# - python3
# - pip3

checkPip=$(pip --version)
echo "Pip version: ${checkPip}"

# get location of currect script file
CURRENT_LOCATION=$(dirname "$0")
#DOCKERFILE_LOCATION="${CURRENT_LOCATION}/Dockerfile"

# Import variables
source ${CURRENT_LOCATION}/variables.sh


#echo "Dockerfile location: ${DOCKERFILE_LOCATION}"


# Build the Docker image
# docker build -t gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest -f ${DOCKERFILE_LOCATION} .
# if [ $? -ne 0 ]; then
#     echo 'Could not build application'
#     exit 1;
# fi

# Push the Docker image to Google Container Registry
# docker push gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest
# if [ $? -ne 0 ]; then
#     echo 'Could not push image to Google Container Registry'
#     exit 1;
# fi

# Deploy the Docker image to Google Cloud Run
#gcloud run deploy ${SERVICE_NAME} --namespace ${SERVICE_NAME} --image gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest --platform managed --region ${REGION} --allow-unauthenticated

# Build and push the Google Cloud Run Docker image from source code
#gcloud builds submit --tag gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest
#gcloud run deploy $SERVICE_NAME --source . --platform managed --region ${REGION} --allow-unauthenticated --service-account=${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com 

#gcloud run deploy $SERVICE_NAME --image gcr.io/$PROJECT_ID/${SERVICE_NAME} --platform managed --region ${REGION} --allow-unauthenticated
