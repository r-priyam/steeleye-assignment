<div align="center">

## SteelEye Assessment

</div>

## Introduction

This repository contains the solution for `SteelEye Backend Developer Assessment`. API is written in `Python 3` which uses `FastAPI` framework.

## Libraries Used

- fastapi: API framework
- uvicorn: ASGI web server
- pydantic: Data validation
- elasticsearch: Async drive for the `elasticsearch` database

## File contents

- `app.py`: Core of the application resides in this file. It has all the required endpoints and connection for the `elasticsearch` cloud database.

- `config.py`: This file contains the class for environment variable validation which uses `pydantic` `BaseSettings` class that's useful for loading the environment variables.

- `schema.py`: This file contains the default schema provided in the assessment.

- `data.json`: Contains the fake data which has been mocked to the `elasticsearch` database index which is hosted in cloud.

- `requirements.txt`: The required packages which is needed to run this API application.

## Approach

I have picked up the `asynchronous` approach to build this API as it can process the multiple request in parallel which may process the request in another thread if needed and then notify the main thread which results in no queue wait when there are multiple requests on the same endpoint. Also using the `async` driver for the `elasticsearch` database to match with the other async operations.

For server I am using `uvicorn` which is recommended `fast server` for the `FastAPI` framework.


