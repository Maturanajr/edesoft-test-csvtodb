
## Install

There is 2 ways to install and test the code. 

Uploading zipfile directly to Lambda or using SAM CLI.

### METHOD 1: Uploading zipfile to Lambda
1: Create a Lambda function in AWS with any name.

2: ADD the following ARNs to Layers in created function:

```bash
  arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python39:1
  arn:aws:lambda:us-east-1:194015752867:layer:sqlalchemy:2
```
3: Upload the zipfile in "lambda_aws" folder as code.

4: Go to configuration tab and in general configuration set Timeout to 30sec at least.

5: Create a test event

6: Configure the test event to send the following JSON object:
```bash
    {
  "object_key": "arquivo_exemplo.csv",
  "bucket_name": "bucket-edesoft"
    }
```
7: Runs test.

### METHOD 2: Using Serverless Application Manager CLI to locally invoke

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

From main folder on this repository open the powershell terminal and type the following commands:
```bash
   cd edesoft-test-local
   sam local invoke -e ./events/event.json CsvToDbFunction --region us-east-1
```
This will invoke the code with the JSON object in events/event.json file.

You can change the JSON object data if you want.