import math
import os
import sys

from typing import Any, Dict, NewType, Tuple

import requests

from github import Github
from github.InputFileContent import InputFileContent

RequestsData = NewType('RequestsData', Dict[str, Any])

ENV_VAR_GIST_ID = 'GIST_ID'
ENV_VAR_GITHUB_TOKEN = 'GH_TOKEN'
REPO_URL = 'https://github.com/ChrisCarini/shodan-exposure-box'
MAX_LINE_LENGTH = 53


def build_url(locale: str) -> str:
    return f'https://shodan.nyc3.digitaloceanspaces.com/exposure-data/{locale}.json'


def get_shodan_exposure_data(locale: str = 'US') -> RequestsData:
    url = build_url(locale=locale)
    resp = requests.get(url=url)
    return resp.json()


def get_port_data(data: RequestsData) -> Tuple[int, int, int]:
    min_count = sys.maxsize
    max_count = 0
    total = 0
    for port, count in data['ports']:
        if count > max_count:
            max_count = count
        if count < min_count:
            min_count = count
        total += count
    return min_count, max_count, total


def get_port_bars(data: RequestsData, max_count: int) -> str:
    result = []
    for port, value in data['ports']:
        # - 'port ' is 5 chars
        # - port value is 5 chars
        # - value is 8 chars
        # - spacing is 3 chars and occurs twice
        space_remaining = MAX_LINE_LENGTH - 5 - 5 - 8 - (2 * 3)

        percent = float(value / max_count) * 100

        bar = generate_bars(percent, space_remaining)

        result.append(f'Port {port:<5} │ {bar} │ {value:>8}')
    return '\n'.join(result)


def generate_bars(percent: float, size: int) -> str:
    syms = '░▏▎▍▌▋▊▉█'
    percent_ = (size * 8 * percent) / 100
    frac = math.floor(percent_)
    barsFull = math.floor(frac / 8)
    if barsFull >= size:
        return syms[8:9] * size

    semi = frac % 8
    return ''.join([syms[8:9] * barsFull] + [syms[semi : semi + 1]]) + (syms[0:1] * (size - barsFull - 1))


def update_gist(title: str, content: str) -> None:
    """Update gist with provided title and content.

    Use gist id and github token present in environment variables.
    Replace first file in the gist.
    """
    print(f'{title}\n{content}')
    access_token = os.environ[ENV_VAR_GITHUB_TOKEN]
    gist_id = os.environ[ENV_VAR_GIST_ID]
    gist = Github(access_token).get_gist(gist_id)
    # Works only for single file. Should we clear all files and create new file?
    old_title = list(gist.files.keys())[0]
    gist.edit(
        description=title,
        files={
            old_title: InputFileContent(content=content, new_name=title),
            'INFO.md': InputFileContent(
                content=f'_🔗 [See the source code behind this gist here!]({REPO_URL})_',
                new_name=f'{title} - INFO.md',
            ),
        },
    )
