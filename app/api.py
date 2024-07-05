import logging
from http import HTTPStatus

from fastapi import FastAPI

from app.routers import auth, users
from app.schemas.message import MessageResponse

app = FastAPI(
    title='FastAPI do Zero - Dunossauro',
    description='',
    summary='',
    version='1.0',
    # terms_of_service='http://example.com/terms/',
    # contact={
    #     'name': 'Deadpoolio the Amazing',
    #     'url': 'http://x-force.example.com/contact/',
    #     'email': 'dp@x-force.example.com',
    # },
    # license_info={
    #     'name': 'Apache 2.0',
    #     'url': 'https://www.apache.org/licenses/LICENSE-2.0.html',
    #     'identifier': 'MIT',
    # },
)
app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(auth.router, prefix='/auth', tags=['Auth'])

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get('/', status_code=HTTPStatus.OK, response_model=MessageResponse)
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
