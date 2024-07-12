import functools

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# setup resource, tracing, & exporter
resource = Resource(attributes={'service.name': 'fast.api.dunossauro', 'compose_service.name': 'fast.api.dunossauro'})
otlp_exporter = OTLPSpanExporter(endpoint='http://localhost:4317', insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)

tracer = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer)
# trace.get_tracer_provider().add_span_processor(span_processor)
tracer.add_span_processor(span_processor)


def instrument(name='request'):
    def decorator(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(name=name) as span:
                span.add_event('get response')
                response = method(*args, **kwargs)
                return response

        return wrapper

    return decorator


def instrument_async(name='request'):
    def decorator(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(name=name) as span:
                span.add_event('get response')
                response = method(*args, **kwargs)
                return response

        return wrapper

    return decorator

    return decorator
