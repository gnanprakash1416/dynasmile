import json
import boto3
import os
import time

def get_instance_status(instance_id, credentials_file):
    with open(credentials_file) as f:
        credentials = json.load(f)
    ec2 = boto3.client(
        'ec2',
        aws_access_key_id=credentials['aws_access_key_id'],
        aws_secret_access_key=credentials['aws_secret_access_key'],
        region_name=credentials['region_name']
    )
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        status = response['Reservations'][0]['Instances'][0]['State']['Name']
        return status
    except ClientError as e:
        print(f"Error fetching instance status: {e}")
        return None
def start_ec2_instance(instance_id, credentials_file):
    # check instance status
    instance_status = get_instance_status(instance_id, credentials_file)
    if instance_status is None:
        print("Could not determine the status of the instance.")
        return
    
    if instance_status != 'stopped':
        if instance_status=='running':
            with open(credentials_file) as f:
                credentials = json.load(f)
            ec2 = boto3.resource(
                'ec2',
                aws_access_key_id=credentials['aws_access_key_id'],
                aws_secret_access_key=credentials['aws_secret_access_key'],
                region_name=credentials['region_name']
            )
            instance = ec2.Instance(instance_id)
            return {
            'public_ip': instance.public_ip_address,
            'public_dns': instance.public_dns_name
        }
        print(f"Instance {instance_id} is currently in '{instance_status}' state. Cannot start.")
        return
    # get aws credential from json
    with open(credentials_file) as f:
        credentials = json.load(f)
    ec2 = boto3.resource(
        'ec2',
        aws_access_key_id=credentials['aws_access_key_id'],
        aws_secret_access_key=credentials['aws_secret_access_key'],
        region_name=credentials['region_name']
    )
    instance = ec2.Instance(instance_id)
    response = instance.start()
    instance.wait_until_running()
    status = instance.state
    print(f'Instance {instance_id} is now {status["Name"]}.')
    return {
        'public_ip': instance.public_ip_address,
        'public_dns': instance.public_dns_name
    }

def stop_ec2_instance(instance_id, credentials_file, region='us-west-2'):
    """
    Load AWS credentials from a JSON file and stop a specified EC2 instance.
    :param instance_id: EC2 instance ID
    :param credentials_file: Path to the JSON file containing access keys
    :param region: AWS region name
    """
    # Load AWS credentials from the JSON file
    with open(credentials_file, 'r') as file:
        credentials = json.load(file)
    try:
        access_key = credentials['aws_access_key_id']
        secret_key = credentials['aws_secret_access_key']
        region='us-east-1'
        # Create EC2 resource object
        ec2 = boto3.resource(
            'ec2',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        # Get EC2 instance object
        instance = ec2.Instance(instance_id)
        # Stop the instance
        response = instance.stop()
        print(f'Stopping instance {instance_id}...')
        
        # Wait until the instance is stopped
        #instance.wait_until_stopped()
        #print(f'Instance {instance_id} has been stopped.')
        return response
    except Exception as e:
        # Catch and print any exception that occurs, but continue execution
        print(f'An error occurred: {e}')

# testing code
if __name__ == "__main__":
    current_path=os.path.abspath(__file__)
    current_folder=os.path.dirname(current_path)
    instance_id = 'i-034544d95b9703bfc'  # substance ID
    credentials_file = os.path.join(current_folder,'ec2_config.json')  # 
    oo=start_ec2_instance(instance_id, credentials_file)
    print(oo)
    time.sleep(30)
    stop_ec2_instance(instance_id, credentials_file)
