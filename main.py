import uvicorn

# from app.api import app

if __name__ == '__main__':
    uvicorn.run('app.main:app', host='0.0.0.0', port=8080, log_level='info', reload=True)

# add
# CORS
# itsdangerous - Necessário para suporte a SessionMiddleware
# orjson - Necessário se você quer utilizar ORJSONResponse.
# ujson - Necessário se você quer utilizar UJSONResponse.
# pip install --upgrade xxxx


# https://fastapidozero.dunossauro.com/
# pip freeze > requirements.txt
# poetry add --group dev pytest pytest-cov taskipy ruff httpx

# alembic init migrations
# alembic revision --autogenerate -m "create users table"
# alembic upgrade head
# alembic downgrade -1

# git add .
# git commit -m "Aula 08 - Tornando o sistema de autenticação robusto"
# git push
# license GNU General Public License v3.0

# python -i app/api.py
# fastapi dev app/api.py --host 0.0.0.0
