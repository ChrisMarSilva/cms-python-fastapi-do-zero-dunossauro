import json
import datetime as dt
import logging
import time
from http import HTTPStatus
from contextlib import asynccontextmanager

# import redis
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

from app.routers import auth, users
from app.schemas.message import MessageResponse
from app.utils.tracing import instrument_async
# from app.utils.settings import Settings

# settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('event_startup')
    # session = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD, db=settings.REDIS_DB, encoding="utf-8", decode_responses=True)
    # app.state.redis = redis.Redis(connection_pool=session)
    yield
    # app.state.redis.close()
    logger.info('event_shutdown')


app = FastAPI(title='FastAPI do Zero - Dunossauro', version='1.0', lifespan=lifespan)
app.include_router(auth.router, prefix='/auth', tags=['Auth'])
app.include_router(users.router, prefix='/users', tags=['Users'])

FastAPIInstrumentor.instrument_app(app=app)

app.add_middleware(GZipMiddleware, minimum_size=1000000)
app.add_middleware(
    CORSMiddleware, allow_origins=['http://localhost', 'http://localhost:8080'], allow_credentials=True, allow_methods=['*'], allow_headers=['*']
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
LoggingInstrumentor().instrument(log_level=logging.INFO, set_logging_format=True, logging_format='%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s trace_sampled=%(otelTraceSampled)s] - %(message)s')

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    try:
        response = await call_next(request)
    finally:
        end_time = time.perf_counter() - start_time

    process_time: str = f'{dt.timedelta(seconds=end_time)}({end_time:.2f}s)'
    # logger.info(f'Request to {request.url.path}: {process_time}')
    response.headers['X-Process-Time'] = process_time
    return response


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    return JSONResponse(status_code=400, content={"message": f"Failed to execute: {request.method}: {request.url}. Detail: {err}"})


@app.get(path='/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request, "id": 1000})


@instrument_async('calling get_name_sync')
@app.get(path='/root', status_code=HTTPStatus.OK, response_model=MessageResponse)
async def root():
    logger.info('Get Message')
    try:

        value = app.state.get('users-json')
        if value is None:
            # response = await app.state.http_client.get('https://jsonplaceholder.typicode.com/users')
            # value = response.json()
            # app.state.set('users-json', json.dumps(value))
            app.state.set('users-json', "ok")

        # await asyncio.sleep(5)
        return MessageResponse(message='Olá Mundo!')
    except Exception as exc:
        logger.error(f'Error: {exc}')
