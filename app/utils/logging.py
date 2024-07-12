import logging  # pragma: no cover

from opentelemetry.instrumentation.logging import LoggingInstrumentor  # pragma: no cover

LoggingInstrumentor().instrument(
    log_level=logging.INFO,
    set_logging_format=True,
    logging_format='%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s trace_sampled=%(otelTraceSampled)s] - %(message)s',
)  # pragma: no cover

# Add logging
logging.basicConfig(level=logging.INFO)  # pragma: no cover
logger = logging.getLogger(__name__)  # pragma: no cover
# logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
