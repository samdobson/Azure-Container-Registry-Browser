from __future__ import annotations

from azure.containerregistry import ArtifactTagProperties
from azure.containerregistry.aio import ContainerRegistryClient
from azure.identity.aio import AzureCliCredential


class ContainerRegistry:
    def __init__(self, acr_name: str):
        credential = AzureCliCredential()
        self.client = ContainerRegistryClient(
            f"https://{acr_name}.azurecr.io",
            credential,
            audience="https://management.azure.com",
        )

    async def get_repositories(self) -> list[str]:
        repos = []
        async for p in self.client.list_repository_names():
            repos.append(p)
        return repos

    async def get_tags(self, name: str) -> list[ArtifactTagProperties]:
        properties = []
        async for p in self.client.list_tag_properties(name):
            properties.append(p)
        return properties
