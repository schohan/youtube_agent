#!/bin/sh

# # Import variables 
CURRENT_LOCATION=$(dirname "$0")
source ${CURRENT_LOCATION}/variables.sh

# define variables
#BRANCH=`git rev-parse --abbrev-ref HEAD`
BRANCH="main"
DATE=$(date "+%Y-%m-%d-%H%M")
APP="$SERVICE_NAME:${BRANCH}${DATE}"
TAG="${PROJECT_ID}/${APP}"

#change project to beta/prod project
gcloud config set project $PROJECT_ID

# Add test to find current director. This script should run from project root where Dockerfile is present. 
BASEDIR="$(pwd)"
echo "Base dir $BASEDIR"

#Tag
#./scripts/deploy/tag-release.sh 'version-prod'
# if [ $? -ne 0 ]; then
#     echo 'Could not tag this release. Make sure git is properly installed and you are running this script from project root. `e.g. ./scripts/deploy-prod.sh`'
#     exit 1;
# fi
  
echo "Tag ${TAG}"
# Build google image
gcloud builds submit --tag gcr.io/${TAG} .

if [ $? -eq 0 ]; then
    # Deploy the image
    gcloud run deploy ${SERVICE_NAME} --image gcr.io/${TAG} --platform managed --region ${REGION} 
    # --service-account=${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com 
fi

