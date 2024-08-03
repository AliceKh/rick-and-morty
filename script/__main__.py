import csv
import urllib.parse
from pathlib import Path
from typing import Iterator, Any

import requests

Character = dict[str, Any]


def save_to_csv(data: list[Character], csv_file: Path):
    """
    Saves the given `data` to a CSV file.
    """
    if data:
        keys = data[0].keys()
        with csv_file.open('w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)


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
        if origin in character['origin']['name']:
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


def main(origin_name: str, filter_criteria: dict[str, str]):
    try:
        save_to_csv(list(format_characters(filter_by_origin(get_characters_by_criteria(filter_criteria), origin_name))),
                    Path('data.csv'))

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    origin_name = "Earth"
    filter_criteria = {
        'species': "Human",
        'status': "Alive",
    }

    main(origin_name, filter_criteria)
