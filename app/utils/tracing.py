import functools

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as OTLPSpanExporterHTTP

# trace.set_tracer_provider(TracerProvider())  # Sets the global default tracer provider
# tracer = trace.get_tracer('api.dunossauro')  # Creates a tracer from the global tracer provider
# tracer = TracerProvider()
# trace.set_tracer_provider(tracer)
# tracer.add_span_processor(BatchSpanProcessor(OTLPSpanExporterHTTP(endpoint='http://jaeger-collector:4318/v1/traces')))

# setup resource, tracing, & exporter
resource = Resource(attributes={"service.name": "fast.api.dunossauro"})
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.set_tracer_provider(TracerProvider(resource=resource))
trace.get_tracer_provider().add_span_processor(span_processor)


def instrument(name="request"):
    def decorator(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(name=name) as span:
                response = method(*args, **kwargs)
                return response

        return wrapper

    return decorator


def instrument_async(name="request"):
    def decorator(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(name=name) as span:
                response = method(*args, **kwargs)
                return response

        return wrapper

    return decorator

    return decorator
