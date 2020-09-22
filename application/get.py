import json
import logging
import boto3
import os

log = logging.getLogger()
log.setLevel(logging.DEBUG)

region = os.getenv("AWS_REGION")
tablename = os.getenv("TABLE_NAME")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tablename)


def get_from_dynamo(event):
    log.debug("Received in get_from_dynamo: {}".format(json.dumps(event)))
    item_id = event['pathParameters']['item_id']
    log.debug("item_id: {}".format(item_id))
    item = table.get_item(
        Key={
            'item_id': item_id,
        }
    )
    return item['Item']


def lambda_handler(event, context):
    log.debug("Received event in get_item: {}".format(json.dumps(event)))
    body = {
        "item_id": get_from_dynamo(event),
        "retrieved from": region
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
