import config
import os
import project
import datatobackfill


def main():
    print("this is main()")
    c = config.Config()

    keyValue = c.ProjectsRoot

    d2b = datatobackfill.DataToBackfill(c)
    projects = d2b.getProjects()
    tags = d2b.getTags()

    print(projects)
    print(tags)

    s = input()


if __name__ == "__main__":
	main()