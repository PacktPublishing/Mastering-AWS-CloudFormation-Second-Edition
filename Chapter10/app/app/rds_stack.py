from aws_cdk import Stack, RemovalPolicy
from constructs import Construct
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds


class RdsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, webserver_sg: ec2.SecurityGroup, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = vpc
        self.webserver_sg = webserver_sg
        rds_instance = rds.DatabaseInstance(self, 'Rds', credentials=rds.Credentials.from_generated_secret('admin'),
                                            database_name="db", engine=rds.DatabaseInstanceEngine.MYSQL,
                                            vpc=vpc, instance_type=ec2.InstanceType.of(
                                                ec2.InstanceClass.BURSTABLE3, 
                                                ec2.InstanceSize.MICRO),
                                            removal_policy=RemovalPolicy.DESTROY, deletion_protection=False)
        rds_instance.connections.allow_from(webserver_sg, ec2.Port.tcp(3306))
