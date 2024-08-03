# Script
This Python script retrieves characters from the Rick and Morty API based on specified criteria, filters them by the given origin, and formats the characters to include their Name, Location, and Image. The formatted data is then saved into a CSV file.

## Features
- Retrieves characters based on filter criteria.
- Filters characters by their origin.
- Formats character data for CSV output.
- Utilizes Python generators for efficient data processing.

## Usage
The script uses Python generators to efficiently process and filter large sets of data without loading everything into memory. This is particularly useful when dealing with large datasets or when you want to stream data as it's being processed.

## Running the Script
To run the script, simply execute it in your terminal:
```
python script.py
```
The script will generate a data.csv file containing the filtered and formatted character data.

# REST API
## Building and Running the Docker Image
To build and run the Docker image for the REST API, use the following commands:
```
docker build . -t rickandmorty:0.1.0 
docker run -p 80:80 rickandmorty:0.1.0
```
## API Documentation
The REST API documentation is available at `[URL]/docs`.
## Endpoints

### GET /
**Docs Redirect**
### GET /healthcheck
**Healthcheck**
### GET /search/{origin_name}
**Characters by Origin filter by criteria**
#### Parameters
- `origin_name` *required* (string, path): The origin name to filter characters by.
- `name` (string, query): Filter by character name.
- `status` (string, query): Filter by status (Available values: `alive`, `dead`, `unknown`).
- `species` (string, query): Filter by species.
- `type` (string, query): Filter by type.
- `gender` (string, query): Filter by gender (Available values: `female`, `male`, `genderless`, `unknown`).
