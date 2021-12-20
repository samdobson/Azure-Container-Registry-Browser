import aiodocker


async def get_docker_images():
    docker = aiodocker.Docker()
    print("== Images ==")
    for image in await docker.images.list():
        tags = image["RepoTags"][0] if image["RepoTags"] else ""
        print(image["Id"], tags)


async def pull(name: str):
    docker = aiodocker.Docker()
    await docker.pull(name)
