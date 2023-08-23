import aws_cdk as core
from aws_cdk.assertions import Template, Match

from app.core_stack import CoreStack

def test_vpc_has_public_subnets():
    app = core.App()
    stack = CoreStack(app, 'core')
    assert len(stack.vpc.public_subnets) > 0

def test_vpc_has_private_subnets():
    app = core.App()
    stack = CoreStack(app, 'core')
    assert len(stack.vpc.private_subnets) > 0

def test_dev_role_is_readonly():
    app = core.App()
    stack = CoreStack(app, 'core')
    template = Template.from_stack(stack)
    template.has_resource_properties('AWS::IAM::Role', {
        'ManagedPolicyArns': [Match.object_like({
            "Fn::Join": ["",["arn:",{"Ref": "AWS::Partition"},":iam::aws:policy/ReadOnlyAccess"]]
        })]
    })
