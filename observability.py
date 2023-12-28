from dotenv import load_dotenv
import os, logging, grpc, re, uptrace
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.resources import Resource

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter,
)
from opentelemetry.sdk import metrics as sdkmetrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    AggregationTemporality,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk import metrics as sdkmetrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    AggregationTemporality,
    PeriodicExportingMetricReader,
)

load_dotenv()  # take environment variables from .env.

regex = r"@[\d.]*:\d*"

dsn = os.getenv("UPTRACE_DSN")
print("dsn:" + dsn)
service_name = os.getenv("OTEL_SERVICE_NAME")
matches = re.search(regex, dsn, re.DOTALL)
endpoint = None
if matches:
    endpoint = matches.group(0).lstrip('@')

print(endpoint)
uptrace.configure_opentelemetry(
    # Set dsn or UPTRACE_DSN env var.
    dsn=dsn,
    service_name=os.getenv("OTEL_SERVICE_NAME"),
    service_version="1.0.0",
    deployment_environment="Production",
    resource=Resource(attributes={"service.name": os.getenv("OTEL_SERVICE_NAME"), "service.version": "1.0.0"})
)
resource = Resource(
    attributes={"service.name": os.getenv("OTEL_SERVICE_NAME"), "service.version": "1.0.0"}
)


# logging exporter
logger_provider = LoggerProvider(resource=resource)
set_logger_provider(logger_provider)

log_exporter = OTLPLogExporter(
    endpoint=endpoint,
    headers=(("uptrace-dsn", dsn),),
    timeout=5,
    compression=grpc.Compression.Gzip,
    insecure=True
)

logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
logging.getLogger().addHandler(handler)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
LoggingInstrumentor().instrument(set_logging_format=True)


#  Span exporter
tracer_provider = TracerProvider(
    resource=resource,
    id_generator=AwsXRayIdGenerator(),
)
span_exporter = OTLPSpanExporter(
    endpoint=endpoint,
    # Set the Uptrace dsn here or use UPTRACE_DSN env var.
    headers=(("uptrace-dsn", dsn),),
    timeout=5,
    compression=grpc.Compression.Gzip,
    insecure=True
)
span_processor = BatchSpanProcessor(
    span_exporter,
    max_queue_size=1000,
    max_export_batch_size=1000,
)
trace.set_tracer_provider(tracer_provider)
tracer_provider.add_span_processor(span_processor)

# metrics exporter
temporality_delta = {
    sdkmetrics.Counter: AggregationTemporality.DELTA,
    sdkmetrics.UpDownCounter: AggregationTemporality.DELTA,
    sdkmetrics.Histogram: AggregationTemporality.DELTA,
    sdkmetrics.ObservableCounter: AggregationTemporality.DELTA,
    sdkmetrics.ObservableUpDownCounter: AggregationTemporality.DELTA,
    sdkmetrics.ObservableGauge: AggregationTemporality.DELTA,
}

metric_exporter = OTLPMetricExporter(
    endpoint=endpoint,
    headers=(("UPTRACE_DSN", os.getenv("UPTRACE_DSN")),),
    timeout=5,
    compression=grpc.Compression.Gzip,
    preferred_temporality=temporality_delta,
    insecure=True,
)
reader = PeriodicExportingMetricReader(metric_exporter)
provider = MeterProvider(metric_readers=[reader], resource=resource)
metrics.set_meter_provider(provider)