import csv
from pathlib import Path

import requests


def query_rest_api(url: str) -> dict[str, str]:
    """
    queries the rest api
    :raises:
        :exception Exception url is incorrect
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed to run with a {response.status_code}. {response.text}")


def filter_data(data: dict[str, str], filter_criteria: dict[str, str]) -> dict[str, str]:
    filtered_data = []
    for item in data:
        match = True
        for key, value in filter_criteria.items():
            if item.get(key) != value:
                match = False
                break
        if match:
            filtered_data.append(item)
    return filtered_data


def format_data(data: dict[str, str], location_name: str) -> list[dict[str, str]]:
    formatted_data = []
    for item in data:
        formatted_data.append({
            'Name': item['name'],
            'Location': location_name,
            'Image': item['image']
        })
    return formatted_data


def save_to_csv(data: list[dict[str, str]], csv_file: Path):
    """
    Saves the given `data` to a CSV file.
    """
    if data:
        keys = data[0].keys()
        with csv_file.open('w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)


def get_location_info(location_name: str) -> list[str]:
    """
    Queries API by `location_name` to get residents URLs

    :raises:
        :exception Exception location was not found
    """
    url = f'https://rickandmortyapi.com/api/location/?name={location_name}'
    result = query_rest_api(url)
    locations = result['results']
    if locations:
        residents_urls = locations[0]['residents']
        return residents_urls
    else:
        raise Exception(f"No location found with name {location_name}")


def get_residents_details(residents_urls: list[str]) -> dict[str, str]:
    """
    Queries URL for resident details
    """
    residents_ids = ','.join(url.split('/')[-1] for url in residents_urls)
    url = f'https://rickandmortyapi.com/api/character/{residents_ids}'
    return query_rest_api(url)


def main(location_name: str, filter_criteria: dict[str, str]):
    try:
        residents_urls = get_location_info(location_name)
        residents_data = get_residents_details(residents_urls)
        filtered_data = filter_data(residents_data, filter_criteria)
        formatted_data = format_data(filtered_data, location_name)
        save_to_csv(formatted_data, Path('data.csv'))

        print("Data has been successfully filtered, formatted, and saved to 'data.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Variables
    location_name = "Earth (C-137)"
    filter_criteria = {
        'species': "Human",
        'status': "Alive"
    }

    main(location_name, filter_criteria)
