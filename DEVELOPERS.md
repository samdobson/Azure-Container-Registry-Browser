# Developing

Welcome to the developer guide for `azurecr-browser`. All commands assume that you in the root of the repository.

## Setting up your environment

```bash
make init
```

This will install dependencies and pre-commit hooks.

## Releasing

Run the following command. It will tag and push the latest commit, triggering the CI/CD pipeline, which will create a release.

```bash
make tag version="v1.0.0"
```
