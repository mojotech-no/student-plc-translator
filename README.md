,# template-python-app
[![example workflow](https://github.com/mojotech-no/template-python-app/actions/workflows/CI.yml/badge.svg?branch=main)](https://github.com/mojotech-no/template-python-app/actions/workflows/CI.yml)
[![example workflow](https://github.com/mojotech-no/template-python-app/actions/workflows/build-and-push-image-to-ghcr.yml/badge.svg?branch=main)](https://github.com/mojotech-no/template-python-app/actions/workflows/build-and-push-image-to-ghcr.yml)

[![Ruff format](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FJacobCoffee%2Fbfb02a83c8da3cbf53f7772f2cee02ec%2Fraw%2Facb94daa3aedecda67e2c7d8c5aec9765db0734d%2Fformat-badge.json)](https://github.com/astral-sh/ruff)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Hi! :wave: This is a template GitHub repository for Python.

CI is automatic by default as:
https://github.com/mojotech-no/template-python-app/blob/e25c1b34b5638976b8db336bfa99c5ede6d6b32d/.github/workflows/CI.yml#L3-L6

Build is manual by default. To enable automatic build, change:
[on:
  workflow_dispatch:](https://github.com/mojotech-no/student-plc-translator/blob/217c4645e26ca4d44a5f53fd3229c835ea9bc92b/.github/workflows/build-and-push-image-to-ghcr.yml#L12-L13)

to:
```yaml
on:
  push:
    branches: [ "main"]
  pull_request:
    branches: [ "main" ]
```
to get epic tests (you do write tests right? :thinking:)

Built Docker image pushed to ghcr (GitHub Container Registry, not Docker Hub by default), will end up to the right under Packages like this:
![image](https://user-images.githubusercontent.com/119582611/205160381-d47b6147-46cf-4cd4-8d58-bcf4ec5737de.png)

## Config and secrets
The config folder is set up with .toml files for local, developement, and production.
Intended use is to keep GitHub secrets secret in development and producition toml, while local shall only have not secret test variables.
Secrets must be made and match the secret name in the tomls e.g. ENV_SECRET_SDT_MQTT_BROKER_URL.
Secrets are read and populated by `config.replace_env_vars`.
Secrets can be made at different levels where the "lowest" (repo) level takes precendse.

Levels are: Organisation (ORG_), repo environment (ENV_), and repo (REP_).
If not secret, consider making the variable a not so secret GitHub variable, e.g. ENV_VAR_SHOW_ME_THE_LOGS.
More on GitHub secrets: [Manage secrets](https://docs.github.com/en/codespaces/managing-codespaces-for-your-organization/managing-secrets-for-your-repository-and-organization-for-github-codespaces)

## Pin versions!
Pinning versions makes applications reproducible and updates managable. Use dependabot to automatically open PR's for version updates, and since you write tests you can approve and merge with confidence.
Not all dependencies are created equal, see [Semantic Dependencies](https://peps.python.org/pep-0426/#semantic-dependencies). The most important deps to keep tabs on are the "runtime dependencies", dev not so much.
See [Version Specifiers](https://packaging.python.org/en/latest/specifications/version-specifiers/#id4) for options of pinning.

Example (feel free to remove this pin as you see fit): https://github.com/Goodtech-AS/template-python-app/blob/9347a19eb61da378febd5271a73bc2e3e5472e0d/pyproject.toml#L6

## Live share
Useful for sharing live. Collaborate.

Use Ctrl+Shift+P and type "live share" for options:

GLHF :partying_face:
:party_face:
Hello
hello