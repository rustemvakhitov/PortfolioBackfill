import boto3
from botocore.exceptions import ClientError
import config
import project

class DynamoDbHelper():

    def __init__(self, cgf):
        self.Config: config.Config = cgf

    def loadTags(self, tags):
        self.createTagsTable()

        dynamodb = boto3.resource('dynamodb', region_name=self.Config.Region)
        table = dynamodb.Table(self.Config.TagsTableName)

        for key in tags:
            print(key, tags[key])
            table.put_item(
                Item={
                    'key': key,
                    'info': tags[key],
                }
            )


        return
    
    def tableExists(self, tableName:str) -> bool:

        client = boto3.client('dynamodb', region_name=self.Config.Region)

        try:
            client.describe_table(TableName=tableName)
            print(f"Table '{tableName}' exists.")
            return True
        except client.exceptions.ResourceNotFoundException:
            print(f"Table '{tableName}' does not exist.")
            return False

    def createTagsTable(self):

        dynamodb = boto3.resource('dynamodb', region_name=self.Config.Region)
        client = boto3.client('dynamodb', region_name=self.Config.Region)

        if self.tableExists(self.Config.TagsTableName):
            client.delete_table(TableName=self.Config.TagsTableName)
            waiter = client.get_waiter('table_not_exists')
            waiter.wait(TableName=self.Config.TagsTableName)

        table = dynamodb.create_table(
        TableName=self.Config.TagsTableName,
        KeySchema=[
            {
                'AttributeName': 'key',
                'KeyType': 'HASH'  #Partition_key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'key',
                'AttributeType': 'S'
            }

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
        )

        table.wait_until_exists()

        print("Table status:", table.table_status)

        return