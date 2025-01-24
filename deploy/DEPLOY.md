# Deploying the app to GCP

App can be deployed to GCP (Cloud Run) which provides managed kubernetes cluster. It is an extermely
easy way to deploy and manage apps without having to worry about the underlying infrastructure.

There are multiple scripts included which help with the deployment process. 
But the key script is `deploy.sh` which will deploy the app to GCP as a Cloud Run service.

Configuration is done in the `variables.sh` file and Google Cloud Service needs to have 
OPENAI_API_KEY configured at least.

Other variables are optional and can be configured as needed.

## Deploying the app

Prerequisites:
- Google Cloud SDK installed
- gcloud CLI installed
- Service account with necessary permissions is created and key is present in the project
- `variables.sh` file is configured with the correct values


Run from the root of the project.
```bash
./deploy/deploy.sh
```

