from cfnlint import CloudFormationLintRule # pip install cfnlint
from cfnlint import RuleMatch # pip install cfnlint


class RdsDeletionPolicy(CloudFormationLintRule):
    id = 'W9001'
    shortdesc = 'Check RDS deletion policy'
    description = 'This rule checks DeletionPolicy on RDS resources to be Snapshot or Retain'
    RDS_RESOURCES = [
        'AWS::RDS::DBInstance', 
        'AWS::RDS::DBCluster'
    ]

    def match(self, cfn):
        matches = []
        resources = cfn.get_resources(self.RDS_RESOURCES)
        for resource_name, resource in resources.items():
            deletion_policy = resource.get('DeletionPolicy')
            path = ['Resources', resource_name]
            if deletion_policy is None:
                message = f'Resource {resource_name} does not have Deletion Policy!'
                matches.append(RuleMatch(path, message))
            elif deletion_policy not in ('Snapshot', 'Retain'):
                message = f'Resource {resource_name} does not have Deletion Policy set to Snapshot or Retain!'
                matches.append(RuleMatch(path, message))
        return matches
