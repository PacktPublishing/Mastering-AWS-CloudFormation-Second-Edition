#!/usr/bin/env python3
import aws_cdk as cdk
from app.core_stack import CoreStack
from app.web_stack import WebStack
from app.rds_stack import RdsStack



app = cdk.App()
core = CoreStack(app, 'CoreStack')
web = WebStack(app, 'WebStack', vpc=core.vpc)
RdsStack(app, 'RdsStack', vpc=core.vpc, webserver_sg=web.webserver_sg)

app.synth()
