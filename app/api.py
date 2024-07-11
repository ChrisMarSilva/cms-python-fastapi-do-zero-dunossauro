import datetime as dt
import logging
import time
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

from app.routers import auth, users
from app.schemas.message import MessageResponse
from app.utils.tracing import instrument_async

app = FastAPI(title='FastAPI do Zero - Dunossauro', version='1.0')
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


@instrument_async('calling get_name_sync')
@app.get(path='/', status_code=HTTPStatus.OK, response_model=MessageResponse)
async def root_read():
    logger.info('Get Message')
    try:
        # await asyncio.sleep(5)
        return MessageResponse(message='Olá Mundo!')
    except Exception as exc:
        logger.error(f'Error: {exc}')
