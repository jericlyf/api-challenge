## Story

Gemini is a popular cryptocurrency exchange. In this exercise, we are extracting the price of various cryptocurrencies at a 15 minutes interval from Gemini and storing that data in an S3 bucket. This data could be used to monitor prices of cryptocurrencies of interest and analyse potential good times to buy or sell. With an interval of every 15 minutes, this data would be more suitable for users who buy and hold cryptocurrencies as opposed to users who are looking  for daily trading. 

## Assumptions

1. UTC timestamp is desired.
2. Price in USD is desired.
3. AWS CLI is available for replication of the resources.
4. User has permissions to create S3 buckets and cloudformation stacks.
5. One file contains data for one day. Data is injected every 15 minutes.
6. Assume raw data for the prices are good enough.

## Files in repository
- api_challenge.zip - zip file containing lambda code and required modules for the lambda
- gemini_market.py - Python code (Python3.7)
- resources.template - Template file to be used for creating Cloudformation stack
- README file

## Instructions

Create S3 bucket using AWS CLI

```
aws s3 mb s3://tdf-gemini-challenge 
```
Navigate to the root of this repository. Add the zip file containing code and modules to the S3 bucket
```
aws s3 cp api_challenge.zip s3://tdf-gemini-challenge/code/
```
Create Cloudformation stack using the resource.template file
```
aws cloudformation create-stack --stack-name gemini-market --template-body file://resources.template --capabilities CAPABILITY_NAMED_IAM
```

The stack will create the following resources:

1. Lambda function to request the Gemini market prices.
2. Cloudwatch event to trigger the lambda every 15 minutes.
3. The appropriate roles to give the lambda permissions to S3 bucket.
4. The appropriate roles to give the cloudwatch event permission to trigger the lambda.

Once the stack is created, wait 15 minutes to see the first data injection in S3 (s3://tdf-gemini-challenge/output/) or manually invoke the lambda using the command below or directly from the AWS console
```
aws lambda invoke --function-name GeminiMarket --invocation-type RequestResponse lambda-result.txt
```
The command above invokes the lambda and returns the lambda response body in a new file "lambda-result.txt".