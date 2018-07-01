# Stager for Kate

## Introduction

The stager implements following functions:

- Provide API service using Flask framework;
- Collect users' application file and its metadata from request, then generate Dockerfile based on that;
- Build docker image using above Dockerfile and upload the image to Docker hub, return the image identifier to the requester.

## Configurations

### AWS credentials
If the credentials are not stored in ~/.aws/credentials, run following command to load credentials:
```
(venv) ➜  aws configure
AWS Access Key ID [****************ABCD]: 
AWS Secret Access Key [****************abcd]: 
```

### Docker credentials
Run following command to login to Docker Hub:
```
(venv) ➜  docker login
```

## Quick Start
Go to root directory, make bootstrap.sh executable:
```
(venv) ➜  chmod +x bootstrap.sh
```
Start the stager application:
```
(venv) ➜  ./bootstrap.sh &
```

## Tests
```
curl -X POST -H "Content-Type: application/json" -d '{
  'file': 'ABC12345abc/app.jar'
  'appid': '1234'
  'appname': 'kate-app1'
  'space': 'naeast'
  'org': 'tech'
}' http://localhost:5000/stager
```
