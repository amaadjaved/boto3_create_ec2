import boto3

AWS_REGION = "us-east-1"
user_data_script = """#!/bin/bash
apt get update
apt install update  -y
apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io -y
sudo systemctl enable docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose"""

ec2 = boto3.resource('ec2')
instance = ec2.create_instances(
    ImageId="ami-04505e74c0741db8d",
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.small",
    UserData=user_data_script,
    KeyName="cp",
    # VpcId="vpc-0efb0450595bae7ba",
    SubnetId="subnet-0af7f914f589c7609",
    SecurityGroupIds=["sg-031e175563b7444ea"],
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'VolumeSize': 30,
                'VolumeType': 'gp2'
            }
        }
    ],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'rudder'
                },
            ]
        },
    ],
)
print(instance)
