import uvicorn

if __name__ == '__main__':
    uvicorn.run('app.main:app', reload=True)

# https://fastapidozero.dunossauro.com/
# pip freeze > requirements.txt
# poetry add --group dev pytest pytest-cov taskipy ruff httpx
# task test
# pytest -s -x --cov=app -vv
# coverage html

# git add .
# git commit -m "Configuração inicial do projeto"
# git push
# license GNU General Public License v3.0

# python -i app/main.py
# read_root()
# fastapi dev app/main.py
# fastapi dev app/main.py --host 0.0.0.0
