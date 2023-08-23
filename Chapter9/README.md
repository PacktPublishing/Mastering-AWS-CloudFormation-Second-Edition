# Template Macros

## AMI filler

1. Deploy Macro stack
```bash
cd macros/ami-filter
aws cloudformation deploy --stack-name ami-filler-macro --template-file macro.yaml --capabilities CAPABILITY_IAM
```
2. Deploy Launch Template stack
```bash
aws cloudformation deploy --stack-name lt --template-file lt.yaml
```

## Standard App
1. Deploy Core stack
```bash
cd ../standard-app
aws cloudformation deploy --stack-name core --template-file core.yaml --capabilities CAPABILITY_IAM
```
2. Create bucket and upload the code
```bash
aws s3 mb s3://masteringcfn
zip lambda-macro.zip standard-app.py
aws s3 cp lambda-macro.zip s3://masteringcfn
```
3. Deploy Macro stack
```bash
aws cloudformation deploy --stack-name standard-app-macro --template-file macro.yaml --capabilities CAPABILITY_IAM
```
4. Deploy Standard app stack
```bash
aws cloudformation deploy --stack-name app --template-file app.yaml
```

## Modules

1. Publish the module
```bash
cd ../modules/module
cfn submit --region REGION # pick yours
```
2. Deploy core stack
```bash
cd ..
aws cloudformation deploy --stack-name core --template-file core.yaml --capabilities CAPABILITY_IAM
```
3. Deploy modular stack
```bash
aws cloudformation deploy --stack-name app --template-file standard_app.yaml
```
4. Change the template, set `NeedsBalancer` to true
5. Deploy update
```bash
aws cloudformation deploy --stack-name app --template-file standard_app.yaml
```
