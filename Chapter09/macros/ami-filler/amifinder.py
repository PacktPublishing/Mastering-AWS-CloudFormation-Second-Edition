import boto3

image_names = {
    'amazonlinux': 'al2023-ami-2023.1.20230809.0-kernel-6.1-x86_64',
    'ubuntu': 'ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20230516',
    'rhel': 'RHEL-9.2.0_HVM-20230503-x86_64-41-Hourly2-GP2',
    'sles': 'suse-sles-15-sp5-v20230620-hvm-ssd-x86_64'
}


def get_image(img_name):
    client = boto3.client('ec2')
    resp = client.describe_images(
        Filters=[{'Name': 'name', 
                  'Values': [img_name]}])
    return resp['Images'][0]['ImageId']


def lambda_handler(event, context):
    response = {}
    response['requestId'] = event['requestId']
    response['fragment'] = {'ImageId': ''}
    response['status'] = 'SUCCESS'
    osfamily = event['params']['OSFamily']

    if osfamily not in image_names.keys():
        response['status'] = 'FAILURE'
        return response

    image_id = get_image(image_names[osfamily])
    response['fragment']['ImageId'] = image_id
    return response