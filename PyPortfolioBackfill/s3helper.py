import boto3
from botocore.exceptions import ClientError
import config
import project
import os
import botocore


class S3Helper():

    def __init__(self, config):
        self.Config = config
        

    def uploadProjectPictures(self, proj: project.Project) -> list[str]:

        self.createBucket(self.Config.BucketName, self.Config.Region)
        self.createSubfolder(self.Config.BucketName, proj.key)

        picturesURLs: list[str] = list[str]() # = list()

        botoconfig = botocore.config.Config(signature_version = botocore.UNSIGNED)
        client = boto3.client("s3", config=botoconfig)

        for picture in proj.pictures:
            self.uploadPicture(self.Config.BucketName, proj.key, picture)
            self.setAclForPicture(self.Config.BucketName, proj.key, picture)

            pictureKey = f"{proj.key}/{os.path.basename(picture)}"
            url = client.generate_presigned_url("get_object", ExpiresIn=0, Params={"Bucket": self.Config.BucketName, "Key": pictureKey})
            picturesURLs.append(url)

        return picturesURLs
    
    def setAclForPicture(self, bucketName, folderName, picturePath):
        pictureKey = f"{folderName}/{os.path.basename(picturePath)}"

        self.setAclForObject(bucketName, pictureKey)

        return
    
    def setAclForObject(self, bucketName, key):
        client = boto3.client('s3')

        try:
            response = client.put_object_acl(
                Bucket=bucketName,
                Key=key,
                ACL='public-read'  # Set ACL to public-read
            )
            print(response)
            print(f"ACL updated successfully for object '{key}' in bucket '{bucketName}'.")
        except Exception as e:
            print(f"Error put_object_acl: {e}")

        return
    
    def uploadPicture(self, bucketName, folderName, picturePath):
        client = boto3.client('s3')
        pictureKey = f"{folderName}/{os.path.basename(picturePath)}"

        try:
            response = client.upload_file(picturePath, bucketName, pictureKey)
            print(response)
            print(f"File '{picturePath}' uploaded to '{pictureKey}' in bucket '{bucketName}'")
        except Exception as e:
            print(f"Error uploading file: {e}")

        return
    
    def createSubfolder(self, bucketName, folderName):

        if self.objectExists(bucketName, folderName):
            return
        
        #otherwise let's create subfolder
        client = boto3.client('s3')

        try:
            response = client.put_object(Bucket=self.Config.BucketName, Key=f'{folderName}/')
            #print(response)
        except ClientError as e:
            print(e)

        return
    
    def createBucket(self, bucketName, region):

        if self.bucketExists(bucketName):
            return
        
        #otherwise let's create bucket
        client = boto3.client('s3')
        
        try:
            response = client.create_bucket(
                Bucket=bucketName,
                ObjectOwnership='ObjectWriter',
                CreateBucketConfiguration={
                    'LocationConstraint': region,
                },
            )
            print(response)

            response = client.put_public_access_block(Bucket=bucketName, PublicAccessBlockConfiguration={'BlockPublicAcls': False,'IgnorePublicAcls': False,'BlockPublicPolicy': False,'RestrictPublicBuckets': False})
            print(response)

            response = client.put_bucket_acl(ACL='public-read',Bucket=bucketName)
            print(response)
        except ClientError as e:
            print(e)
            raise

        return

    def bucketExists(self, bucketName):
        client = boto3.client('s3')
        try:
            client.head_bucket(Bucket=bucketName)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                # Handle other exceptions as needed
                raise

    def objectExists(self, bucketName, key):
        client = boto3.client('s3')
        try:
            client.head_object(Bucket=bucketName, Key=key)
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