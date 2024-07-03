import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)

# https://fastapidozero.dunossauro.com/
# pip freeze > requirements.txt
# fastapi dev main.py