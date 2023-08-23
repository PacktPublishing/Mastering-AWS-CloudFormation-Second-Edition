# AWS SAM

_Make sure you have followed prerequisites steps and installed Docker._

## Hello World
1. Run `sam init` and initialize the project as it is written in the book
2. Run build by issuing `sam build --use-container`
3. Run function locally `sam local invoke`
4. Start API `sam local start-api`
5. In a separate terminal window make a call to local API `curl localhost:3000/hello`
6. Deploy the stack `sam deploy --stack-name hello-world --capabilities CAPABILITY_IAM --resolve-s3`
7. Invoke remote API `curl API_URL/Prod/hello`

## Party planner
Steps are similar to Hello, World
```bash
sam build --use-container
sam deploy --stack-name party --capabilities CAPABILITY_IAM --resolve-s3
```
1. Invoke remote API `curl -X POST -d @events/event.json -H "Content-Type: application/json" https://API_URL/Prod/register`
2. Examine the DynamoDB table
3. Invoke Lambda function for reporting `aws lambda invoke --function-name REPORTING_FUNCTION --payload '{}' out.txt`
4. Check S3
```bash
aws s3 ls s3://REPORTING_BUCKET
aws s3 cp s3://REPORTING_BUCKET/Birthday.txt .
cat Birthday.txt
```
