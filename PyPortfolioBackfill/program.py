import config
import os
import project
import datatobackfill
import s3helper
import dynamoDbHelper


def main():
    c = config.Config()

    d2b = datatobackfill.DataToBackfill(c)
    projects = d2b.getProjects()
    tags = d2b.getTags()

    # upload pictures to S3, give read-only access, remember URLs
    s3h = s3helper.S3Helper(c)
    for project in projects:
        picturesURLs = s3h.uploadProjectPictures(project)
        project.pictures = picturesURLs

    print(projects)
    print(tags)

    #load project Tags to Dynamo
    #load Project details to Dynamo
    dDbHelper = dynamoDbHelper.DynamoDbHelper(c)
    dDbHelper.loadProjects(projects)
    dDbHelper.loadTags(tags)

    #s = input()


if __name__ == "__main__":
	main()