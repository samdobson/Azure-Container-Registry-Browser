FROM python:3.9-slim
ENV ACR_BROWSER_CONFIG /app/.acr-browser.toml
WORKDIR /app
COPY dist/ /tmp

RUN pip install --no-cache-dir -U pip && \
  pip install --no-cache-dir azure-cli && \
  pip install --no-cache-dir /tmp/acr_browser*.whl && \
  rm /tmp/acr_browser*.whl

ENTRYPOINT ["acr"]
