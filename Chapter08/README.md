# CloudFormation Registry 

## DynamoDB Item Extension

1. Create prerequisite stack 
```bash
cd dynamodb-item
aws cloudformation deploy --stack-name extension-dynamo-item --template-file prerequisite.yaml --capabilities CAPABILITY_IAM
```

2. Get IAM role ARN, LogGroup and DynamodB table names
```bash
LOGGROUP=$(aws cloudformation describe-stacks --stack-name extension-dynamo-item --query 'Stacks[0].Outputs[0].OutputValue' --output text)
TABLE=$(aws cloudformation describe-stacks --stack-name extension-dynamo-item --query 'Stacks[0].Outputs[1].OutputValue' --output text)
ROLE=$(aws cloudformation describe-stacks --stack-name extension-dynamo-item --query 'Stacks[0].Outputs[2].OutputValue' --output text)
```

3. Activate DynamoDB Item extension
```bash
aws cloudformation activate-type --type RESOURCE --type-name AwsCommunity::DynamoDB::Item --execution-role-arn $ROLE --logging-config LogRoleArn=$ROLE,LogGroupName=$LOGGROUP --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b
```

4. Deploy a template with DynamoDB item
```bash
aws cloudformation deploy --stack-name configuration-items --template-file item.yaml --parameter-overrides TableName=$TABLE
```

## Private Registry

1. Deploy RDS stack if not already
```bash
cd private-database-registry
aws cloudformation deploy --stack-name rds --template-file rds.yaml --parameter-overrides VpcId=$VPCID # Locate your default VPC
```

2. Install dependencies 
```bash
pip install cloudformation-cli aws-sam-cli # PIP installation
brew update && brew install cloudformation-cli aws-sam-cli # Brew installation
pip install -r database-resource-type/requirements.txt
```

3. Update test input adding RDS endpoint.

4. Prepare and test the resource type
```bash
cd database-resource-type
cfn submit --dry-run
sam local start-lambda # run in a separate terminal window
cfn test
```

5. Upload the resource type extension to registry
```bash
cfn submit -v --region $REGION # pick any of your choice, recommend using the same region as RDS stack
```

6. Deploy custom database using private registry
```bash
cd ..
aws cloudformation deploy --stack-name mydatabase --template-file database.yaml
```

7. Clean up
```bash
aws cloudformation delete-stack --stack-name mydatabase
aws cloudformation delete-stack --stack-name rds
aws cloudformation deregister-type --type RESOURCE --type-name 'Org::Storage::Database'
```