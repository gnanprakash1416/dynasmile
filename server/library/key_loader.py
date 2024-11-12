import os
import requests
import json
from .crypt import encrypt_aws,encrypt_ec2
def check_json_file_exists(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        print(f"The file {file_path} exists.Using server configred by yourself.")
        # Optional: Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                print("File content:", data)
            except json.JSONDecodeError:
                print("The content of the file is not a valid JSON format.")
        return True
    else:
        #print(f"The file {file_path} does not exist.")
        print("using preconfigured EC2 client...")
        return False

def load_key_api():
    api_url = 'https://rt0ut7kstj.execute-api.us-east-1.amazonaws.com/prod/keyapi'
    
    # api key, for security
    headers = {
        'x-api-key': '123456'  
    }
    current_path=os.path.abspath(__file__)
    current_folder=os.path.dirname(current_path)

    search_target=os.path.join(current_folder,"data.json")
    if check_json_file_exists(search_target)==True:
        with open(search_target, 'r') as file:
            config = json.load(file)
            aws_config={}
            ec2_config={}
            aws_config["aws_config_aws_access_key_id"]=config.get("aws_config_aws_access_key_id")
            aws_config["aws_config_aws_secret_access_key"]=config.get("aws_config_aws_secret_access_key")
            aws_config["region_name"]=config.get("region_name")
            ec2_config["ec2_config_aws_access_key_id"]=config.get("ec2_config_aws_access_key_id")
            ec2_config["ec2_config_aws_secret_access_key"]=config.get("ec2_config_aws_secret_access_key")
            ec2_config["region_name"]=config.get("region_name")
            #print(aws_config,ec2_config)
            return aws_config,ec2_config
    else:
        try:
            response = requests.get(api_url, headers=headers)
            
            # 检查响应状态码
            if response.status_code == 200:
                # 打印返回的 JSON 数据
                json_return=response.json()
                json_return_body_original=json_return.get('body')
                json_return_body=json.loads(json_return_body_original)
                aws_config={}
                ec2_config={}
                aws_config["aws_config_aws_access_key_id"]=json_return_body.get("aws_config_aws_access_key_id")
                aws_config["aws_config_aws_secret_access_key"]=json_return_body.get("aws_config_aws_secret_access_key")
                aws_config["region_name"]=json_return_body.get("region_name")
                ec2_config["ec2_config_aws_access_key_id"]=json_return_body.get("ec2_config_aws_access_key_id")
                ec2_config["ec2_config_aws_secret_access_key"]=json_return_body.get("ec2_config_aws_secret_access_key")
                ec2_config["region_name"]=json_return_body.get("region_name")
                #print(aws_config,ec2_config)
                return aws_config,ec2_config
            else:
                print(f"request error，status code: {response.status_code}, info: {response.json()}")
        
        except Exception as e:
            print(f"error occured: {e}")
if __name__ == "__main__":
    load_key_api()