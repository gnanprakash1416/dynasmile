'''refernece code from: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
designed  for:  uploading videos to AWS s3 bucket.
to do:
1. design a function to upload a given file to s3 bucket.
2. develop a function to transit videos from s3 to EC2.
'''

'''demo function part.'''
import numpy as np
import cv2
import boto3
import os


def upload_func(s3_link, filename, bucket_name='frank--bucket',
                folder_target=None):
    # Let's use Amazon S3
    img = cv2.imread(filename)
    data = np.array(cv2.imencode('.png', img)[1]).tobytes()
    s3_link.Bucket(bucket_name).put_object(
        Key=os.path.basename(filename), Body=data)
    # Do not use cv2 in uploading.


def upload_video(s3_link, filename, bucket_name='frank--bucket',
                 folder_target=None):
    with open(filename, 'rb') as data:
        s3_link.Bucket(bucket_name).put_object(
            Key=os.path.basename(filename), Body=data)


def download_func(s3_link, filename,
                  bucket_name='frank--bucket', folder_target=None):
    target_file = folder_target + os.path.basename(filename)
    with open("./" + target_file, 'wb') as f:
        s3_link.download_fileobj(bucket_name, os.path.basename(target_file), f)


if __name__ == '__main__':
    s3_resource = boto3.resource('s3')
    upload_func(
        s3_resource,
        'C:\\Users\\denti\\Pictures\\R-C.png',
        'frank--bucket',
    )
    s3_client = boto3.client('s3')
    download_func(s3_client, 'R-C.png', 'frank--bucket', 'test\\')
