#!/usr/bin/env python3

import boto3

AWS_REGION = "us-east-1"
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
KEY_PAIR_NAME = 'xime-test'
AMI_ID = 'ami-0c02fb55956c7d316'



# User data
user_data = """#!/bin/bash
DOMAIN=sb.anacondaconnect.com
LOCAL_IP=$(/usr/bin/curl -s  http://169.254.169.254/latest/meta-data/local-ipv4 | cut -d = -f 2)

FQDN=$LOCAL_IP.$DOMAIN
echo $FQDN > /etc/hostname

cat >/etc/hosts <<EOF
127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4 ${FQDN}
::1 localhost6 localhost6.localdomain6 ${FQDN}
EOF

"""

instances = EC2_RESOURCE.create_instances(
    MinCount = 1,
    MaxCount = 1,
    ImageId=AMI_ID,
    InstanceType='t2.micro',
    KeyName=KEY_PAIR_NAME,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'sdk-ec2-test'
                },
            ]
        },
    ]
)

for instance in instances:
    print(f'EC2 instance "{instance.id}" has been launched')

    instance.wait_until_running()
    print(f'EC2 instance "{instance.id}" has been started')
