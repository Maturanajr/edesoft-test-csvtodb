
# Edesoft test - CSV to DB

This is a function created to be executed in Lambda AWS.
The porpuse is read a .csv file in a bucket from S3 AWS and insert this on a MySql DB running in RDS AWS.


## Execute

To execute the lambda function on my Aws execute the following code:
```bash
  curl -v -X POST -H "Content-Type: application/json" -d '{"""object_key""":"""arquivo_exemplo.csv""","""bucket_name""":"""bucket-edesoft"""}' https://ui5ohcrvrdtyzgo7dhlkl5r2tu0mvmxh.lambda-url.us-east-1.on.aws
```
Where "object_key" is the csv file name and "bucket_name" is the bucket from S3.

You can POST for this URL with other methods you want.
## Install to own usage

There is 2 ways to install and test the code. 

Uploading zipfile directly to Lambda or using SAM CLI.

### Create MySQL database
First of all you will need a MySQL database. For this project i have used RDS Aws to host my DB.

Create a Table with any name, using the base struct in "CREATE TABLE CESSAO_FUNDO.sql" (avaliable in this repository)


### METHOD 1: Uploading zipfile to Lambda
1: Create a Lambda function in AWS with any name.

2: ADD role to this function to access Layers and S3 files.

3: ADD the following ARNs to Layers in created function:

```bash
  arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python39:1
  arn:aws:lambda:us-east-1:194015752867:layer:sqlalchemy:2
```
4: Upload the zipfile in "lambda_aws" folder as code.

5: Go to configuration tab and in general configuration set Timeout to 30sec at least.

6: Still in configuration tab go to Enviroments variable and add these values:
```bash
key     value

DBHOST	YOUR_DATABASE_ENDPONT
DBNAME	YOUR_DATABASE_NAME
DBPASS	YOUR_DATABASE_PASSWORD
DBPORT	YOUR_DATABASE_PORT
DBTABLE	NAME_OF_DATABASE_TABLE
DBUSER	YOUR_DATABASE_USER
```

7: Create a test event

8: Configure the test event to send the following JSON object:
```bash
    {
  "object_key": "arquivo_exemplo.csv",
  "bucket_name": "bucket-edesoft"
    }
```
9: Runs test.

### METHOD 2: Using Serverless Application Manager CLI to locally invoke

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

First you have to add credentials to your AWS CLI.

Type on your terminal:
```bash
   aws configure
```
And inform the requested data

From main folder on this repository open the powershell terminal and type the following commands:
```bash
   cd edesoft-test-local
```
Create a .env file with the data:
```bash
DBHOST=edesoft-test.cujsn6qajjg2.us-east-1.rds.amazonaws.com
DBNAME=edesoft
DBPASS=Po97017085
DBPORT=3306
DBTABLE=CESSAO_FUNDO
DBUSER=root
```
Execute the following code to start:
```bash
sam local invoke -e ./events/event.json CsvToDbFunction --region us-east-1
```
This will invoke the code with the JSON object in events/event.json file.

You can change the JSON object data if you want.