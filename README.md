# FastAPI-Authentication-and-Interaction-Service
A lightweight API built with FastAPI to authenticate users via API keys and process interaction-based requests with intent and slot handling.



## Overview
This project implements a FastAPI-based interaction service that processes user requests with text, context, and language inputs. It includes an authentication module to validate API keys and supports intent-based interaction logic. The service is designed to be scalable and secure, with modular components for handling API requests and responses.

## Project Structure
- **api/auth/auth.py**: Handles API key authentication, validating tokens and sub-versions.
- **api/interaction/execute.py**: Core API logic for processing interaction requests and handling intent-based responses.
- **main.py**: Entry point to start the FastAPI server.
- **utils/utils.py**: Utility functions for configuration, version management, and user validation (not included in the provided code).
- **helpers.py**: Contains helper functions like `StringHelper` for text processing (not included in the provided code).
- **logger.py**: Logging configuration for tracking API events (not included in the provided code).

## Prerequisites
- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- Dependencies listed in `utils.utils`, `helpers`, and `logger` modules

## Installation
1. Clone the repository:
   ```bash
   git clone [<repository-url>](https://github.com/moinakhter/FastAPI-Authentication-and-Interaction-Service.git)
   cd FastAPI-Authentication-and-Interaction-Service.
   ```
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn pydantic
   ```
3. Ensure the required utility modules (`utils.utils`, `helpers`, `logger`) are available or implemented.

## Configuration
- Set environment variables or configuration for `HOST`, `PORT`, and `ADMIN_KEY` in your environment or configuration file, as accessed by `get_conf()` in `utils.utils`.
- Configure sub-version and parent version data for API versioning, as used in `get_sub_version_apis()` and `get_version()`.

## Usage
1. Start the API server:
   ```bash
   python main.py
   ```
2. The API will be available at `http://<HOST>:<PORT>` (default values depend on your configuration).
3. Send a POST request to `/interaction/request` with the required headers and body:
   - **Headers**:
     - `Authorization`: Your API key or token.
     - `SubVersion`: API sub-version for routing.
   - **Body** (JSON):
     ```json
     {
       "text": "Sample text",
       "context": {"intent": "sample_intent", "slots": {}},
       "language": "tr"
     }
     ```
   - **Example** (using curl):
     ```bash
     curl -X POST "http://localhost:<PORT>/interaction/request" \
     -H "Authorization: <your-api-key>" \
     -H "SubVersion: <sub-version>" \
     -H "Content-Type: application/json" \
     -d '{"text":"Hello world","context":{"intent":"greeting","slots":{}},"language":"tr"}'
     ```

## API Endpoints
### POST `/interaction/request`
- **Description**: Processes an interaction request with text, context, and language.
- **Authentication**: Requires a valid API key in the `Authorization` header and a valid `SubVersion` header.
- **Request Body**:
  - `text` (string, required): Input text for processing.
  - `context` (dict, required): Context containing intent and slots.
  - `language` (string, optional): Language code (defaults to "tr").
- **Response**:
  - Success: `{"result": {"intent": <intent>, "slots": <slots>, "interaction_response": <response>}, "status": true}`
  - Error: HTTP 401 (Invalid API key) or HTTP 400 (Missing language parameter).

## Authentication
- The `api/auth/auth.py` module validates API keys using the `Authorization` header.
- An admin key (configured via `get_conf("ADMIN_KEY")`) bypasses user validation.
- User tokens are validated using `validate_user_id()` from `utils.utils`.
- Sub-version validation ensures compatibility with the requested API version.

## Intent Processing
- The `handle_intent_process` function in `execute.py` processes the input text and context to generate an intent, slots, and interaction response.
- Custom logic for intent processing should be implemented in this function.

## Logging
- The `logger.LOG` module (not provided) logs key events, such as intent, slots, and interaction responses.

## Running the Service
- The `main.py` script initializes the FastAPI application and starts the server using Uvicorn.
- Ensure the `HOST` and `PORT` are correctly configured in your environment.

## Notes
- The `utils.utils`, `helpers`, and `logger` modules are referenced but not provided. Ensure these are implemented or available in your project.
- The `handle_intent_process` function currently returns a placeholder `"custom logic"` response. Replace it with your actual intent processing logic.
- The API supports versioning via the `SubVersion` header, validated against `get_sub_version_apis()` and `get_version()`.

## License
This project is licensed under the MIT License.
