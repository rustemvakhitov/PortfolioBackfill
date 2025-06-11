import config
import os
import project
import datatobackfill
import s3helper
import dynamoDbHelper


def main():
    print("this is main()")
    c = config.Config()

    keyValue = c.ProjectsRoot

    d2b = datatobackfill.DataToBackfill(c)
    projects = d2b.getProjects()
    tags = d2b.getTags()

    print(projects)
    print(tags)

    dDbHelper = dynamoDbHelper.DynamoDbHelper(c)
    dDbHelper.loadTags(tags)


    # upload pictures to S3, give read-only access, remember URLs
    s3h = s3helper.S3Helper(c)
    for project in projects:
        picturesURLs = s3h.uploadProjectPictures(project)
        project.pictures = picturesURLs

    #load project tags to Dynamo
    dDbHelper = dynamoDbHelper.DynamoDbHelper(c)
    dDbHelper.loadTags(tags)

    #load Project details to Dynamo

    s = input()


if __name__ == "__main__":
	main()