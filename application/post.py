import json
import logging
import boto3
import os
import uuid
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit


log = logging.getLogger()
log.setLevel(logging.DEBUG)

region = os.getenv("AWS_REGION")
tablename = os.getenv("TABLE_NAME")

tracer = Tracer(service="Post")
logger = Logger(service="Post")
metrics = Metrics(service="Post", namespace="PostService")


class NoTableName(Exception):
    pass


if os.getenv("AWS_SAM_LOCAL", ""):
    ddb = boto3.resource('dynamodb',
                         endpoint_url="http://dynamodb:8000")
    ddb_table = tablename
else:
    ddb = boto3.resource('dynamodb')
    ddb_table = os.getenv("TABLE_NAME", None)

if not ddb_table:
    raise NoTableName("Check SAM env variables")
else:
    table = ddb.Table(ddb_table)


def respond(data="", status=200):
    return {
        "statusCode": status,
        "body": json.dumps(data)
    }


def aws_request_was_successful(resp):
    if (
            resp["ResponseMetadata"]["RequestId"] and
            resp["ResponseMetadata"]["HTTPStatusCode"] == 200
    ):
        return True
    return False


def put_to_dynamo(event):
    log.debug("Received in put_to_dynamo: {}".format(json.dumps(event)))
    data = json.loads(event["body"])
    user_name = data.get("name", "")
    user_email = data.get("email", "")
    user_id = str(uuid.uuid4())
    params = {
        "Item": {
            "id": user_id,
            "email": user_email,
            "name": user_name
        }
    }
    try:
        ret = table.put_item(**params)
        if aws_request_was_successful(ret):
            return respond(params['Item'], 200)
    except ClientError as e:
        print(e)
        return respond("Operation failed", 500)


@metrics.log_metrics(capture_cold_start_metric=True)
@tracer.capture_lambda_handler
@logger.inject_lambda_context
def lambda_handler(event, context):

    metrics.add_metric(name="PostSucceeded", value=1, unit=MetricUnit.Count)

    log.debug("Event in create_item: {}".format(json.dumps(event)))
    return put_to_dynamo(event)
