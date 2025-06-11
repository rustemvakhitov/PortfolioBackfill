import config
import os
import project
import datatobackfill
import s3helper


def main():
    print("this is main()")
    c = config.Config()

    keyValue = c.ProjectsRoot

    d2b = datatobackfill.DataToBackfill(c)
    projects = d2b.getProjects()
    tags = d2b.getTags()

    print(projects)
    print(tags)

    s3h = s3helper.S3Helper(c)
    for project in projects:
        s3h.uploadProjectPictures(project)
          

    s = input()


if __name__ == "__main__":
	main()