<!-- markdownlint-disable MD026 -->
[![Python versions](https://shields.io/pypi/pyversions/azurecr-browser)](https://badge.fury.io/py/azurecr-browser)
[![PyPI version](https://badge.fury.io/py/azurecr-browser.svg)](https://pypi.org/project/azurecr-browser/)
![PyPI - License](https://img.shields.io/pypi/l/azurecr-browser)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Azure Container Registry Browser

A terminal-based user interface for managing container images and artifacts in Azure Container Registry.

![home_view](media/interface.png)

## Installation

Install with pip, poetry, or your favourite package manager:

```bash
pip install azurecr-browser
```

Log in with [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli):

```
az login
```

Run the application with the following command. You can optionally append the name of the registry to be managed.

```bash
acr
```

The app will remember the registry you looked at last, so you don't need to specify it next time around.

If you prefer instead to use Docker:

```bash
docker run --rm -it --volume $HOME:/app --volume $HOME/.azure:/root/.azure ghcr.io/samdobson/azurecr-browser:latest
```
## Credits

:rocket: This project owes a huge debt of gratitude to the fantastic [Azure Key Vault Browser](https://github.com/chelnak/azure-keyvault-browser), from which it is forked, and of course, to the underlying technologies that make both of these projects possible: [textual](https://github.com/willmcgugan/textual) and [rich](https://github.com/willmcgugan/rich)!

## Contributing

If you would like to contribute to `azurecr-browser` head over to the [contributing guide](CONTRIBUTING.md) to find out more.
