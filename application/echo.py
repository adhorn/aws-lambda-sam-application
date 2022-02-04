import json
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit
from chaos_lambda import inject_fault


tracer = Tracer(service="echo")
logger = Logger(service="echo")
metrics = Metrics(service="echo", namespace="EchoService")


@inject_fault
@metrics.log_metrics(capture_cold_start_metric=True)
@tracer.capture_lambda_handler
@logger.inject_lambda_context
def lambda_handler(event, context):

    metrics.add_metric(name="EchoSucceeded", value=1, unit=MetricUnit.Count)

    logger.info("about to return echo")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello, Worlds!"
        }),
    }
