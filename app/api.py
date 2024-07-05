import logging
import time
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users
from app.schemas.message import MessageResponse

app = FastAPI(title='FastAPI do Zero - Dunossauro', version='1.0')
app.include_router(auth.router, prefix='/auth', tags=['Auth'])
app.include_router(users.router, prefix='/users', tags=['Users'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost', 'http://localhost:8080'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(process_time)
    response.headers['X-Process-Time'] = str(process_time)
    return response


@app.get(path='/', status_code=HTTPStatus.OK, response_model=MessageResponse)
async def root_read():
    logger.info('Get Message')
    return MessageResponse(message='Olá Mundo!')
    # try:
    #     logger.info('Get Message')
    #     # await save_address(address)
    #     return Message(message='Olá Mundo!')
    #     # return {'message': 'Olá Mundo!'}
    # except Exception as exc:
    #     logger.error(f'Error: {exc}')
    # async def search_address(uf: Optional[str] = Query(None, max_length=2, min_length=2)):
    # try:
    #     await save_address(address.dict())
    #     return address
    # except errors.DuplicateKeyError:
    #     return JSONResponse(status_code=409, content={"message": "Cep já existe"})
