<p align='center'>
  <img src="images/shodan-port-usage-box.png" width="600px">
  <h1 align="center">shodan-exposure-box</h1>
  <p align="center">💻 Update a pinned gist to contain Shodan.io Exposure Stats</p>
  <p align="center">
    <img src="https://github.com/ChrisCarini/shodan-exposure-box/workflows/Update%20gist%20with%20Shodan%20Stats/badge.svg?branch=main" alt="Update a pinned gist to contain Shodan.io Exposure Stats">
  </p>
</p>

## 🎒 Prep Work

1. Create a new public GitHub Gist (https://gist.github.com/)
2. Create a token with the `gist` scope and copy it. (https://github.com/settings/tokens/new)
3. Copy the `API token`

## 🖥 Project Setup

1. Go to your fork's `Settings` > `Secrets` > `Add a new secret` for each environment secret (below)

## 🤫 Environment Secrets

- **GH_TOKEN:** The GitHub token generated above.
- **GIST_ID:** The ID portion from your gist url:

  `https://gist.github.com/ChrisCarini/`**`0c0b8690e430b9fe4572f9c4a38811c1`**.

  (Alternatively this can be put directly in `.github/workflows/shodan.yml` as it is public anyway.)

## 🤓 Hacking

```bash
# setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```