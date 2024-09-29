import json
import boto3
import os
import time
import random
def xor_encrypt_decrypt(data, key):
    return ''.join(chr(ord(c) ^ key) for c in data)
def simple_permutation(data, perm):
    return ''.join(data[i] for i in perm)
def insert_chars(data, chars):
    mixed = list(data)
    for char in chars:
        position = random.randint(0, len(mixed))
        mixed.insert(position, char)
    return ''.join(mixed)
def swap_positions(data, swap_indices):
    data_list = list(data)
    for idx1, idx2 in swap_indices:
        data_list[idx1], data_list[idx2] = data_list[idx2], data_list[idx1]
    return ''.join(data_list)
def encrypt(plain_text, key, insert_chars_list):
    xor_encrypted = xor_encrypt_decrypt(plain_text, key)
    mixed_text = insert_chars(xor_encrypted, insert_chars_list)
    swap_indices = [(0, 1), (2, 3)]
    swapped_text = swap_positions(mixed_text, swap_indices)
    permutation = list(range(len(swapped_text)))
    random.shuffle(permutation)
    permuted_text = simple_permutation(swapped_text, permutation)
    permuted_text = permuted_text.replace('"', '?')
    return permuted_text, swap_indices, permutation
def decrypt_new(encrypted_text, key, swap_indices, permutation, insert_chars_list):
    encrypted_text = encrypted_text.replace('?', '"')
    reverse_permutation = sorted(range(len(permutation)), key=lambda x: permutation[x])
    permuted_text = simple_permutation(encrypted_text, reverse_permutation)
    swapped_text = swap_positions(permuted_text, swap_indices)
    for char in insert_chars_list:
        swapped_text = swapped_text.replace(char, '', 1)
    decrypted = xor_encrypt_decrypt(swapped_text, key)
    return decrypted

def get_instance_status(instance_id, credentials_file):
    with open(credentials_file) as f:
        credentials = json.load(f)
    insert_chars_list="xyyuyyyui"
    key=123
    credentials['aws_access_key_id']=decrypt_new(credentials['aws_access_key_id'], key, [(0, 1), (2, 3)], [7, 28, 1, 26, 0, 9, 23, 6, 10, 25, 24, 20, 3, 21, 18, 5, 27, 15, 8, 4, 2, 11, 12, 22, 19, 17, 16, 14, 13], insert_chars_list)
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
            insert_chars_list="xyyuyyyui"
            key=123
            credentials['aws_access_key_id']=decrypt_new(credentials['aws_access_key_id'], key, [(0, 1), (2, 3)], [7, 28, 1, 26, 0, 9, 23, 6, 10, 25, 24, 20, 3, 21, 18, 5, 27, 15, 8, 4, 2, 11, 12, 22, 19, 17, 16, 14, 13], insert_chars_list)
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
    insert_chars_list="xyyuyyyui"
    key=123
    credentials['aws_access_key_id']=decrypt_new(credentials['aws_access_key_id'], key, [(0, 1), (2, 3)], [7, 28, 1, 26, 0, 9, 23, 6, 10, 25, 24, 20, 3, 21, 18, 5, 27, 15, 8, 4, 2, 11, 12, 22, 19, 17, 16, 14, 13], insert_chars_list)
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
    insert_chars_list="xyyuyyyui"
    key=123
    credentials['aws_access_key_id']=decrypt_new(credentials['aws_access_key_id'], key, [(0, 1), (2, 3)], [7, 28, 1, 26, 0, 9, 23, 6, 10, 25, 24, 20, 3, 21, 18, 5, 27, 15, 8, 4, 2, 11, 12, 22, 19, 17, 16, 14, 13], insert_chars_list)
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
