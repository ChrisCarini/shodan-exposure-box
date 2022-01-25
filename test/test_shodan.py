import os

from typing import Dict, List
from unittest import mock
from unittest.mock import MagicMock, PropertyMock

import pytest

import shodan

from shodan import RequestsData, build_url, generate_bars, get_port_bars, get_port_data, get_shodan_exposure_data

MOCK_DATA: Dict[str, List[List[object]]] = {
    'ports': [
        ['80', 123],
        ['443', 456],
        ['22', 789],
    ],
}


def test_build_url():
    # given
    locale = 'US'

    # when
    result = build_url(locale=locale)

    # then
    assert f'/{locale}.json' in result, 'The URL should contain our local'
    assert result.startswith('https://'), 'The URL should start with https://'
    assert result.endswith('.json'), 'The URL should end with .json'


def test_get_shodan_exposure_data(requests_mock):
    # given
    locale = 'US'

    requests_mock.get(
        f'https://shodan.nyc3.digitaloceanspaces.com/exposure-data/{locale}.json',
        json=MOCK_DATA,
    )

    # when
    result = get_shodan_exposure_data(locale=locale)

    # then
    assert len(result['ports']) == 3, 'We expect to get 3 ports back.'


def test_get_port_data():
    # given
    expected_result = (123, 789, (123 + 456 + 789))

    # when
    # noinspection PyTypeChecker
    result = get_port_data(data=MOCK_DATA)

    # then
    assert expected_result == result

    # given
    # Note: Flip the ordering of the ports; helps trigger more branch coverage.
    # noinspection PyTypeChecker
    mock_data: RequestsData = {
        'ports': [
            ['22', 789],
            ['443', 456],
            ['80', 123],
        ],
    }

    # when
    result = get_port_data(data=mock_data)

    # then
    assert expected_result == result, 'The expected result should be the same if we flip the ordering.'


def test_get_port_bars():
    # when
    # noinspection PyTypeChecker
    result = get_port_bars(data=MOCK_DATA, max_count=789)

    # then
    assert result == (
        'Port 80    │ ████▌░░░░░░░░░░░░░░░░░░░░░░░░ │      123\n'
        'Port 443   │ ████████████████▊░░░░░░░░░░░░ │      456\n'
        'Port 22    │ █████████████████████████████ │      789'
    )

    # given
    # noinspection PyTypeChecker
    mock_data: RequestsData = {
        'ports': [
            ['22', 789],
            ['443', 456],
            ['80', 123],
        ],
    }
    # when
    result = get_port_bars(data=mock_data, max_count=789)

    # then
    assert result == (
        'Port 22    │ █████████████████████████████ │      789\n'
        'Port 443   │ ████████████████▊░░░░░░░░░░░░ │      456\n'
        'Port 80    │ ████▌░░░░░░░░░░░░░░░░░░░░░░░░ │      123'
    )


@pytest.mark.parametrize(
    'percent, size, expected_result',
    [
        (10, 10, '█░░░░░░░░░'),
        (9, 10, '▉░░░░░░░░░'),
        (8, 10, '▊░░░░░░░░░'),
        (7, 10, '▋░░░░░░░░░'),
        (6, 10, '▌░░░░░░░░░'),
        (5, 10, '▌░░░░░░░░░'),
        (4, 10, '▍░░░░░░░░░'),
        (3, 10, '▎░░░░░░░░░'),
        (2, 10, '▏░░░░░░░░░'),
        (1, 10, '░░░░░░░░░░'),
        (0, 10, '░░░░░░░░░░'),
    ],
)
def test_generate_bars(percent, size, expected_result):
    # expect
    assert generate_bars(percent=percent, size=size) == expected_result


def test_update_gist_no_env_vars():
    # when - no env vars set
    with pytest.raises(KeyError):
        shodan.update_gist(title='my title', content='my content')

    # when - `ENV_VAR_GITHUB_TOKEN` is set, but not `ENV_VAR_GIST_ID`
    os.environ[shodan.ENV_VAR_GITHUB_TOKEN] = '123'
    with pytest.raises(KeyError):
        shodan.update_gist(title='my title', content='my content')


@mock.patch(f'{shodan.__name__}.{shodan.Github.__name__}')
def test_update_gist(mock_Github: MagicMock):  # title: str, content: str) -> None:
    # given
    my_title = 'my title'
    old_title = 'file_title.txt'
    mock_gist = MagicMock()
    mock_gist = PropertyMock(files={old_title: '_'})
    mock_Github.return_value.get_gist.return_value = mock_gist

    # set env vars
    os.environ[shodan.ENV_VAR_GITHUB_TOKEN] = 'access_token'
    os.environ[shodan.ENV_VAR_GIST_ID] = 'gist_id'

    # when
    shodan.update_gist(title=my_title, content='my content')

    # then
    mock_Github.return_value.get_gist.assert_called_once()
    mock_gist.edit.assert_called_once_with(
        description=my_title,
        files={
            old_title: mock.ANY,
            'INFO.md': mock.ANY,
        },
    )
