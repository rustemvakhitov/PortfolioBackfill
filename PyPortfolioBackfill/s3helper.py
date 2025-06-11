import boto3
from botocore.exceptions import ClientError
import config
import project


class S3Helper():

    def __init__(self, config):
        self.Config = config
        

    def uploadProjectPictures(self, proj: project.Project):

        self.createBucket(self.Config.BucketName, self.Config.Region)

        client = boto3.client('s3')
        try:
            response = client.put_object(Bucket=self.Config.BucketName, Key=f'{proj.key}/')
            print(response)
        except ClientError as e:
            print(e)

        return
    
    def createBucket(self, bucketName, region):

        if self.bucketExists(bucketName):
            return
        
        #otherwise let's create bucket
        client = boto3.client('s3')
        
        response = client.create_bucket(
            Bucket=bucketName,
            CreateBucketConfiguration={
                'LocationConstraint': region,
            },
        )

        return

    def bucketExists(self, bucketName):
        s3 = boto3.client('s3')
        try:
            s3.head_bucket(Bucket=bucketName)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                # Handle other exceptions as needed
                raise

    def __str__(self):
        return f'Instance of Project == {self.toJSON()}'
    
    def __repr__(self):
        return f'Instance of Project == {self.toJSON()}'