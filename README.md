<!-- markdownlint-disable MD026 -->
# acr-browser

![acr-browser](https://github.com/samdobson/acr-browser/actions/workflows/ci.yaml/badge.svg) [![PyPI version](https://badge.fury.io/py/acr-browser.svg)](https://badge.fury.io/py/acr-browser)

`acr-browser` is a terminal-based user interface for managing container images and artifacts in Azure Container Registry.

![home_view](media/interface.png)

:rocket: This project owes a huge debt of gratitude to the fantastic [Azure Key Vault Browser](https://github.com/chelnak/azure-keyvault-browser), from which it is forked, and of course, to the underlying technologies that make both of these projects possible: [textual](https://github.com/willmcgugan/textual) and [rich](https://github.com/willmcgugan/rich)!

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

## Compatibility

This project has been tested on macOS and Linux with Python 3.9.

For Ubuntu 20.04, it may be necessary to install the `python3.9` package.

## Contributing

If you would like to contribute to `acr-browser` head over to the [contributing guide](CONTRIBUTING.md) to find out more.
