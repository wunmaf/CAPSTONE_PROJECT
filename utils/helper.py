import configparser
import boto3


#a function to house the bucket creation
def create_bucket(access_key, secret_key, bucket_name, region):
    client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        
    )


    client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': region,
        },
    )