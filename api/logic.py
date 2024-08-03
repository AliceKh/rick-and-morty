import urllib.parse
from typing import Iterator, Any

import requests

Character = dict[str, Any]


def get_characters_by_criteria(criteria: dict[str, str]) -> Iterator[Character]:
    """
    Yields characters that match criteria
    :raises:
        :exception: Exception if there are no matches
    """
    url = 'https://rickandmortyapi.com/api/character'
    url = f'{url}/?{urllib.parse.urlencode(criteria)}'
    response_json = {'info': {'next': url}}
    while response_json['info']['next']:
        response = requests.get(response_json['info']['next'])
        if response.status_code == 200:
            response_json = response.json()
            for character in response_json['results']:
                yield character
        else:
            raise Exception(f"Query failed to run with a {response.status_code}. {response.text}")


def filter_by_origin(characters: Iterator[Character], origin: str) -> Iterator[Character]:
    """
    Yields characters whose origin includes the given value
    """
    for character in characters:
        if origin.lower() in character['origin']['name'].lower():
            yield character


def format_characters(characters: Iterator[Character]) -> Iterator[Character]:
    """
    Formats the character to have name, location and image
    """
    for character in characters:
        yield {
            'Name': character['name'],
            'Location': character['location']['name'],
            'Image': character['image']
        }


def get_characters(origin_name: str, filter_criteria: dict[str, str]) -> Iterator[Character]:
    """
    Yields characters that contain Name, Location, and Image of characters from 'origin_name' and filtered with
    'filter_criteria'
    """
    try:
        return format_characters(filter_by_origin(get_characters_by_criteria(filter_criteria), origin_name))
    except Exception as e:
        print(f"An error occurred: {e}")
