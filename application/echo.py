import json
import os
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit
from chaos_lambda import inject_fault

os.environ['CHAOS_PARAM'] = 'chaoslambda.config'


tracer = Tracer(service="echo")
logger = Logger(service="echo")
metrics = Metrics(service="echo", namespace="EchoService")


@metrics.log_metrics(capture_cold_start_metric=True)
@tracer.capture_lambda_handler
@logger.inject_lambda_context
@inject_fault
def lambda_handler(event, context):

    metrics.add_metric(name="EchoSucceeded", value=1, unit=MetricUnit.Count)

    logger.info("about to return echo")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello, Worlds!"
        }),
    }
