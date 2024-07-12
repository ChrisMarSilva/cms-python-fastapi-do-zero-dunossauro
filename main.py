import uvicorn

if __name__ == '__main__':
    # update uvicorn access logger format
    # log_config = uvicorn.config.LOGGING_CONFIG
    # log_config['formatters']['access']['fmt'] = (
    #     '%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s'
    # )
    # uvicorn.run('app.api:app', log_level='info', reload=True, log_config=log_config)
    uvicorn.run('app.api:app', log_level='info', reload=True)  # , host='0.0.0.0', port=8000, host='127.0.0.1'


# add
# itsdangerous - Necessário para suporte a SessionMiddleware
# orjson - Necessário se você quer utilizar ORJSONResponse.
# ujson - Necessário se você quer utilizar UJSONResponse.
# https://opentelemetry-python-contrib.readthedocs.io/en/latest/index.html

# https://fastapidozero.dunossauro.com/
# pip freeze > requirements.txt
# poetry add --group dev pytest pytest-cov taskipy ruff httpx
# pip install --upgrade xxxx
# pip uninstall aioredis -y

# alembic init migrations
# alembic revision --autogenerate -m "create users table"
# alembic upgrade head
# alembic downgrade -1

# docker-compose down
# docker-compose up -d --build
# docker run -p 9090:9090 -v ./config/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus

# git add .
# git commit -m "Aula 08 - Tornando o sistema de autenticação robusto"
# git push
# license GNU General Public License v3.0

# python -i app/api.py
# fastapi dev app/api.py --host 0.0.0.0
