![The Transformer](https://raw.githubusercontent.com/chrislemke/passsssword/master/docs/assets/icon.png)

# Passsssword
***Utilize 1Password vault data with Python decorators and context managers. Driven by the 1Password CLI interface. 🐍🔐***

[![ChecksAndTesting](https://github.com/chrislemke/passsssword/actions/workflows/checks-testing.yml/badge.svg)](https://github.com/chrislemke/passsssword/actions/workflows/checks-testing.yml)
[![codecov](https://codecov.io/github/chrislemke/passsssword/branch/main/graph/badge.svg?token=LJLXQXX6M8)](https://codecov.io/github/chrislemke/passsssword)
[![Release](https://github.com/chrislemke/passsssword/actions/workflows/release.yml/badge.svg)](https://github.com/chrislemke/passsssword/actions/workflows/release.yml)
[![pypi](https://img.shields.io/pypi/v/passsssword)](https://pypi.org/project/passsssword/)
[![python version](https://img.shields.io/pypi/pyversions/passsssword?logo=python&logoColor=yellow)](https://www.python.org/)
[![license](https://img.shields.io/github/license/chrislemke/passsssword)](https://github.com/chrislemke/passsssword/blob/main/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](https://github.com/python/mypy)


## Introduction

Passsssword is a Python-based utility designed to securely use your 1Password vault data right within your Python scripts. Utilizing Python decorators and context managers, the project interfaces with the 1Password CLI to automatically fetch and inject sensitive data, such as passwords or API-keys.

Passsssword offers two features:

1. **Decorator (`decjector`)**: Apply this decorator to any Python function to inject sensitive data automatically securely before its execution. The temporary `.env` file containing these variables is safely deleted after the function runs.

2. **Context Manager (`contextor`)**: This sets up a secure temporary environment for your code to run in, injecting the necessary passwords,etc. and ensuring their secure deletion afterward.

## Setup

### Requirements

1. Python 3.8 - 3.11
2. [1Password CLI](https://1password.com/downloads/command-line/)

### Installation Steps

1. **Clone the Repository:**
   ```
   git clone https://github.com/chrislemke/passsssword.git
   ```

2. **Navigate to Project Directory:**
   ```
   cd Passsssword
   ```

3. **Install Required Packages:**
   ```
   pip install -r requirements.txt
   ```

4. **Set Up `.env.op` File:**
   Create an `.env.op` file either in the project directory or one of its parent directories. This file will store the 1Password vault item paths, looking like this
   ```
    API_KEY = op://MyVault/MyItem/MyAPIKey
    ...
   ```

5. **Sign in to 1Password CLI:**
   Make sure you've signed into your 1Password account through the CLI.
   ```
   op signin <your-domain>
   ```

## Usage

### Using the `decjector` Decorator

To auto-inject the API-key automatically into your Python function, simply apply the `decjector` decorator:

```python
from Passsssword import decjector

@decjector
def sensitive_function():
    api_key = os.environ.get('API_KEY')
    # Your function logic here

sensitive_function()
```

The `decjector` decorator will securely fetch `API_KEY` from your 1Password vault and make it available within `sensitive_function`.

### Using the `contextor` Context Manager

You can also use the `contextor` context manager in a `with` statement:

```python
from Passsssword import contextor

with contextor():
    api_key = os.environ.get('API_KEY')
    # Your function logic here
```

Within the `with` block, any sensitive data from your 1Password vault specified in `.env.op` will be accessible as environment variables.
