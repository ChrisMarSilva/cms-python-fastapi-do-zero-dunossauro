import datetime as dt
import time
from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# from fastapi.responses import HTMLResponse  # , JSONResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from app.routers import auth, users
from app.schemas.message import MessageResponse
from app.utils.tracing import instrument_async

# from app.utils.metrics import configuration  # PrometheusMiddleware, metrics, setting_otlp
# from app.utils.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    # logger.info('event_startup')
    yield
    # logger.info('event_shutdown')


app = FastAPI(title='FastAPI do Zero - Dunossauro', version='1.0', lifespan=lifespan)

# Add routers
app.include_router(auth.router, prefix='/auth', tags=['Auth'])
app.include_router(users.router, prefix='/users', tags=['Users'])
# app.add_route('/metrics', metrics)

# Add CORS
app.add_middleware(GZipMiddleware, minimum_size=1000000)
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

# Add opentelemetry
FastAPIInstrumentor.instrument_app(app=app)  # , tracer_provider=tracer
# SystemMetricsInstrumentor(config=configuration).instrument()  # SystemMetricsInstrumentor().instrument()
# app.add_middleware(PrometheusMiddleware, app_name='fast.api.dunossauro')
# setting_otlp(app, 'fast.api.dunossauro', 'http://tempo:4317')


# Add templates and statics
# app.mount('/static', StaticFiles(directory='app/static', html=True), name='static')
# templates = Jinja2Templates(directory='app/templates')

# class EndpointFilter(logging.Filter):
#     def filter(self, record: logging.LogRecord) -> bool:
#         return record.getMessage().find("GET /metrics") == -1


# @app.exception_handler(Exception)
# def validation_exception_handler(request, err):
#     return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={'message': f'Failed to execute: {request.method}: {request.url}. Detail: {err}'})


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


# @app.get(path='/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse(name='index.html', context={'request': request, 'id': 1000})


@instrument_async('calling get_name_sync')
@app.get(path='/root', status_code=HTTPStatus.OK, response_model=MessageResponse)
async def root():
    # logger.info('Get Message')
    try:
        # await asyncio.sleep(5)
        return MessageResponse(message='Olá Mundo!')
    except Exception:  # pragma: no cover
        # logger.error(f'Error: {exc}')
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Invalid request body')  # pragma: no cover
