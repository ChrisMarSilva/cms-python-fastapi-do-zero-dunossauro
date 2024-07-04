import uvicorn

if __name__ == '__main__':
    uvicorn.run('app.main:app', reload=True)

# https://fastapidozero.dunossauro.com/
# pip freeze > requirements.txt
# poetry add --group dev pytest pytest-cov taskipy ruff httpx

# alembic init migrations
# alembic revision --autogenerate -m "create users table"
# alembic upgrade head
# alembic downgrade -1

# git add .
# git commit -m "Aula 07 - Refatorando estrutura do projeto: Criado routers para Users e Auth; movido constantes para variáveis de ambient"
# git push
# license GNU General Public License v3.0

# python -i app/main.py
# fastapi dev app/main.py --host 0.0.0.0
