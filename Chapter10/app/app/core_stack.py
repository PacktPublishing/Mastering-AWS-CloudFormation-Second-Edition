from aws_cdk import Stack, Fn
from constructs import Construct
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam


class CoreStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # IAM section
        admin_role = iam.Role(self, 'admin', assumed_by=iam.AccountPrincipal(Fn.ref('AWS::AccountId')))
        self.dev_role = iam.Role(self, 'developer', assumed_by=iam.AccountPrincipal(Fn.ref('AWS::AccountId')))
        admin_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AdministratorAccess'))
        self.dev_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('ReadOnlyAccess'))
        # VPC section
        self.vpc = ec2.Vpc(self, 'vpc', ip_addresses=ec2.IpAddresses.cidr('10.0.0.0/16'), enable_dns_hostnames=True, enable_dns_support=True,
                           max_azs=3, nat_gateways=1, 
                           subnet_configuration=[
                               ec2.SubnetConfiguration(name='Public', subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
                               ec2.SubnetConfiguration(name='Private', subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24)
                           ])
