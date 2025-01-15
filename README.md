# Weather API in Python3 FastAPI

## Features:
- JWT Authentication
- Creating city points and observing the weather at them
- Each user owns their own list of city points.
- Weather from open-source API

## Documentation:
Available at http://localhost:8000/docs as Swagger.

## Run:

### Development mode
Create virtual environment:
- `python3 -m venv env && activate env/bin/activate`
Install dependencies:
- `pip install -r requirements.txt`
- `pip install -e .`
Run postgresql database:
- `docker compose up -d postgres`
Run migrations:
- `python3 -c "__import__('app.db.base').db.base.run_init_models()"`
Run app:
- `python3 script.py` OR `uvicorn app.main:fastapi_app --reload` for hot-reload

### Production mode
- `docker compose up -d --build`

### Tests
Install dependencies:
- `pip install -r requirements.txt`
- `pip install pytest pytest-asyncio`
- `pip install -e .`
Run postgresql database:
- `docker compose up -d postgres`
Run tests:
- `python3 -m pytest -v`
