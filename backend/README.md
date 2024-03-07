## Instructions for getting the backend up
1) install mongo server and run the command `sudo systemctl start mongod` and check status with `sudo systemctl status mongod`
2) install the requirements: `pip install -r requirements.txt`
3) issue the command `python run.py` inside the `backend directory`

### IF YOU MAKE A CHANGE TO THE DATABASE SCHEMA
in `__init__.py`, add the line `db.["users"].drop()` (replace users with the name of the table) and after you save it will recompile, dropping the table. then  you can remove this line and the table will be recreated with the new schema

### Instructions for getting the backend deployed to lambda
1) aws ecr-public get-login-password --region us-east-1 --profile YourSSOProfile | docker login --username AWS --password-stdin public.ecr.aws
Note 1: You may need to first login to the AWS CLI with the command `aws sso login --profile YourSSOProfile`
Note 2: Docker needs to be running
Note 3: If the command fails, you may need to delete the `credsStore` line in the `~/.docker/config.json` file and try again
2) sam build (in the backend directory)
3) sam deploy --guided (in the backend directory, if asked for auth proceed without it, and for the region use eu-north-1)
4) The API endpoint is at "FlaskApi - URL for application            https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/"

### Run the docker container (the artifact of sam build command) locally
1) docker run -d -p 8080:8080 name-of-ecr-image