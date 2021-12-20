<!-- markdownlint-disable MD026 -->
# Azure Container Registry Browser

https://shields.io/pypi/pyversions/acr-browser
[![Python versions](https://shields.io/pypi/pyversions/acr-browser)](https://badge.fury.io/py/acr-browser)
[![PyPI version](https://badge.fury.io/py/acr-browser.svg)](https://pypi.org/project/acr-browser/)

As a terminal-based user interface for managing container images and artifacts in [Azure Container Registry](https://azure.microsoft.com/en-us/services/container-registry/).

![home_view](media/interface.png)

:rocket: This project owes a huge debt of gratitude to the fantastic [Azure Key Vault Browser](https://github.com/chelnak/azure-keyvault-browser), on which it is based, and of course, to the underlying packages that make both of these projects possible: [textual](https://github.com/willmcgugan/textual) and [rich](https://github.com/willmcgugan/rich)!

## Installation

`acr-browser` requires Python 3.9 or later.

```bash
pip install acr-browser
```

Once the app is installed you can run the application from your terminal with the `acr` command.

```bash
acr
```

Alternatively, you can run with Docker:

```bash
docker run --rm -it --volume $HOME:/app --volume $HOME/.azure:/root/.azure ghcr.io/samdobson/acr-browser:latest
```

### Authentication

`acr-browser` uses the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/) for authentication. Before using the app, make sure that you have logged in and set your subscription.

```bash
az login
az account set --subscription "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxx"
```

### Configuration

On first run you will be asked for some information so that the app can build your configuration file.

You'll need to enter a valid Azure Container Registry name.

Alternatively you can create a config file at `~/.acr-browser.toml`:

```bash
# .acr-browser.toml

registry = ""
```

## Contributing

If you would like to contribute to `acr-browser` head over to the [contributing guide](CONTRIBUTING.md) to find out more.
