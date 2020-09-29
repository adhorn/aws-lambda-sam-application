import json
import logging
import boto3
import os
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit


log = logging.getLogger()
log.setLevel(logging.DEBUG)

tablename = os.getenv("TABLE_NAME")

tracer = Tracer(service="Get")
logger = Logger(service="Get")
metrics = Metrics(service="Get", namespace="GetService")


class NoTableName(Exception):
    pass


if os.getenv("AWS_SAM_LOCAL", ""):
    region = "dynamodb-local"
    ddb = boto3.resource('dynamodb',
                         endpoint_url="http://dynamodb:8000")
    ddb_table = tablename

else:
    ddb = boto3.resource('dynamodb')
    ddb_table = os.getenv("TABLE_NAME", None)
    region = os.getenv("AWS_REGION")

if not ddb_table:
    raise NoTableName("Check SAM env variables")
else:
    table = ddb.Table(ddb_table)


def respond(data="", status=200):
    return {
        "statusCode": status,
        "body": json.dumps(data)
    }


def get_from_dynamo(event):
    log.debug("Received in get_from_dynamo: {}".format(json.dumps(event)))
    id = event['pathParameters']['id']
    log.debug("id: {}".format(id))
    try:
        item = table.get_item(
            Key={
                'id': id,
            }
        )
        resp = item["Item"]
        resp["retrieved from"] = region
        return respond(data=resp, status=200)
    except ClientError as e:
        print(e)
        return respond(data="Operation failed", status=500)


@metrics.log_metrics(capture_cold_start_metric=True)
@tracer.capture_lambda_handler
@logger.inject_lambda_context
def lambda_handler(event, context):

    metrics.add_metric(name="GetSucceeded", value=1, unit=MetricUnit.Count)

    log.debug("Received event in get_item: {}".format(json.dumps(event)))
    return get_from_dynamo(event)
