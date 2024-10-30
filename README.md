---

# Feddit API - README

## Introduction

The `Feddit` API simulates a Reddit-like platform, created as part of the Allianz challenge. This service provides
access to `subfeddits` and `comments` with sentiment analysis capabilities, enabling data ingestion and automated
analysis of interactions.

## How to Run

1. **Ensure Docker is Installed**: Please verify that Docker is installed and running on your system.

2. **Running the API**: Open the terminal, navigate to the directory containing `docker-compose.yml`, and start the API
   with:
   ```sh
   docker compose -f <path-to-docker-compose.yml> up -d
   ```
   This will start the API service, which will be accessible at [http://0.0.0.0:8080](http://0.0.0.0:8080).

3. **Stopping the API**: To stop the `Feddit` API service, run:
   ```sh
   docker compose -f <path-to-docker-compose.yml> down
   ```

## API Specification

The `Feddit` API provides multiple endpoints to access and analyze data. Documentation of all endpoints is available at:

- [Swagger UI](http://0.0.0.0:8080/docs) - interactive API documentation.
- [ReDoc](http://0.0.0.0:8080/redoc) - API reference documentation.

### Available Endpoints:

- **GET /**: Root endpoint to verify the API is running.
- **POST /analyze/**: Analyzes comments in selected subfeddits using sentiment analysis. Parameters:
    - `subfeddit_id`: A list of IDs for the subfeddits to be analyzed.
    - `method`: Sentiment analysis method (`keywords`, `textblob`, `vader`).
    - `start_date` and `end_date`: Timestamps to filter comments by date.
    - `sort_by_polarity`: Sorts comments based on polarity score.
    - `limit`: Maximum number of comments returned.
    - `keyword`: Filters comments based on specific keywords.
    - `save_to_csv`: If `True`, saves results as a CSV.

### Pagination

To manage large data volumes, pagination parameters are available in the `/analyze/` endpoint:

- **skip**: Number of comments to skip for the query.
- **limit**: Maximum number of comments returned in the response.

## Data Schemas

### Comment

| Field       | Type    | Description                           |
|-------------|---------|---------------------------------------|
| `id`        | Integer | Unique identifier of the comment      |
| `username`  | String  | User who posted the comment           |
| `text`      | String  | Content of the comment                |
| `created_at`| Integer | Timestamp in Unix epoch time          |

### Subfeddit

| Field         | Type    | Description                                      |
|---------------|---------|--------------------------------------------------|
| `id`          | Integer | Unique identifier of the subfeddit               |
| `username`    | String  | User who started the subfeddit                   |
| `title`       | String  | Topic of the subfeddit                           |
| `description` | String  | Short description of the subfeddit               |
| `comments`    | Array   | Array of `Comment` objects under the subfeddit   |

## Example Usage

To test the `/analyze/` endpoint for sentiment analysis:

1. **Start the FastAPI server**:
   ```sh
   uvicorn src.main:app --reload
   ```
2. **Access Documentation**: Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to try out and interact with
   the API.

3. **Sample Request**:
   ```json
   {
     "subfeddit_id": [1, 2, 3],
     "method": "textblob",
     "start_date": "2023-01-01",
     "end_date": "2023-01-31",
     "sort_by_polarity": true,
     "limit": 50,
     "keyword": "awesome",
     "save_to_csv": true
   }
   ```

## Development

- **Volumes**:
   - `feedit-app_db_data`: Persists database data between sessions.
- **Note**: Ensure all required dependencies are included in `requirements.txt`.

## Automated End-to-End Testing

1. **GitHub Actions**: CI/CD setup can be verified to ensure integration and deployment of any updates.
2. **Data Ingestion & Analysis**: Run the full flow from data ingestion in `data_ingestion.py` to API requests in
   `main.py`.

---
