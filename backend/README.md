## Instructions for getting the backend deployed
1) aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
2) sam build
3) sam deploy --guided
4) The API endpoint is at "FlaskApi - URL for application            https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/"

## Run the docker locally
1) docker run -d -p 8080:8080 {ECR Image}