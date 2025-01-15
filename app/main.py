from fastapi import FastAPI
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every
from pydantic_settings import BaseSettings
from loguru import logger

from app.services.weather_city import WeatherCityService


class ProjectSettings(BaseSettings):
    LOCAL_MODE: bool = False


def register_exception(application):
    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        # or logger.error(f'{exc}')
        logger.debug(f'{exc}')
        content = {'status_code': 422, 'message': exc_str, 'data': None}
        return JSONResponse(
            content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


def register_cors(application):
    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def init_web_application():
    project_settings = ProjectSettings()
    application = FastAPI(
        openapi_url='/openapi.json',
        docs_url='/docs',
        redoc_url='/redoc'
    )

    if project_settings.LOCAL_MODE:
        register_exception(application)
        register_cors(application)

    from app.routes.coordinates import router as coordinates_router
    from app.routes.city import router as city_router
    from app.routes.auth import router as auth_router

    application.include_router(coordinates_router)
    application.include_router(city_router)
    application.include_router(auth_router)

    @repeat_every(seconds=15 * 60)
    async def weather_update_task():
        try:
            await WeatherCityService.update_cities_weather()
        except Exception as e:
            logger.exception(e)

    application.add_event_handler("startup", weather_update_task)

    return application


def init_database():
    from app.db.base import run_init_models
    run_init_models()


def create_app() -> FastAPI:
    application = init_web_application()
    return application


fastapi_app = create_app()
