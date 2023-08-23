# CDK

## Preparation
Create virtualenv and install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run tests
```bash
pip install -r requirements-dev.txt
python -m pytest
```

## Deploy all stacks
```bash
cdk deploy --all
```