# Task Tracker API

A minimal REST API for tracking tasks, built with FastAPI and Pydantic as a
learning project. Task data is persisted to a local JSON file rather than a
database, per [ADR-001](#) (JSON File Storage Architecture), to keep the
project simple and focused on REST API fundamentals.

This skeleton currently exposes only a health check endpoint. CRUD endpoints
for tasks will be added in a later step.

## Tech Stack

- Python 3
- FastAPI
- Pydantic
- Uvicorn (ASGI server)
- python-dotenv (environment variable loading)

## Project Structure
