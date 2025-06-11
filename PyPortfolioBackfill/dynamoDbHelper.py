import boto3
from botocore.exceptions import ClientError
import config
import project

class DynamoDbHelper():

    def __init__(self, cgf):
        self.Config: config.Config = cgf

    def loadTags(self, tags):
        #drop-create table
        self.dropTable(self.Config.TagsTableName)
        self.createTagsTable()

        dynamodb = boto3.resource('dynamodb', region_name=self.Config.Region)
        table = dynamodb.Table(self.Config.TagsTableName)

        for key in tags:
            table.put_item(
                Item={
                    'key': key,
                    'info': tags[key],
                }
            )

        return
    
    def loadProjects(self, projects:list[project.Project]):
        #drop-create table
        self.dropTable(self.Config.ProjectsTableName)
        self.createProjectsTable()

        dynamodb = boto3.resource('dynamodb', region_name=self.Config.Region)
        table = dynamodb.Table(self.Config.ProjectsTableName)

        for project in projects:
            table.put_item(
                Item={
                    'id': project.id,
                    'key': project.key,
                    'info': project.toJSON(),
                }
            )

        return
    
    def dropTable(self, tableName): #self.Config.TagsTableName
        client = boto3.client('dynamodb', region_name=self.Config.Region)

        if self.tableExists(tableName):
            client.delete_table(TableName=tableName)
            waiter = client.get_waiter('table_not_exists')
            waiter.wait(TableName=tableName)

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
    
    def createProjectsTable(self):

        dynamodb = boto3.resource('dynamodb', region_name=self.Config.Region)

        table = dynamodb.create_table(
        TableName=self.Config.ProjectsTableName,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  #Partition_key
            },
            {
                'AttributeName': 'key',
                'KeyType': 'RANGE'  #Sort_key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            },
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