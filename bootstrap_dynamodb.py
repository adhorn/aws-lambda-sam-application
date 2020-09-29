#!/usr/bin/env python
# Local development with:
#
#   Download URL: http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.zip
#   Start command: java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -inMemory
#
#   Docker option:
#
#   docker run -d -v "$PWD":/dynamodb_local_db -p 8000:8000 --network sam-demo cnadiminti/dynamodb-local
#   More info: http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html

import boto3
import argparse
import uuid
import faker
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Uncomment this for local bootstrapping
dynamodb = boto3.resource(
    'dynamodb', region_name='eu-west-1', endpoint_url='http://localhost:8000')

# Uncomment this for non-local bootstrapping
# dynamodb = boto3.resource(
#     'dynamodb', region_name='eu-west-1')


fake = faker.Faker("en.GB")


def create_table(table_name, hash):
    """Creates DynamoDB table with given Hash and Range key as strings"""
    print("[+] Creating Table {}...".format(table_name))
    params = {
        "TableName": table_name,
        "KeySchema": [
            {
                'AttributeName': str(hash),
                'KeyType': 'HASH'
            }
        ],
        "AttributeDefinitions": [
            {
                'AttributeName': str(hash),
                'AttributeType': 'S'
            },
            {
                'AttributeName': "email",
                'AttributeType': 'S'
            }
        ],
        "ProvisionedThroughput": {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
        "GlobalSecondaryIndexes": [
            {
                'IndexName': 'email-gsi',
                'KeySchema': [
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            },
        ]
    }
    table = dynamodb.create_table(**params)
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    return table


def does_table_exist(table_name):
    """Quick check on table"""
    try:
        table = dynamodb.Table(table_name)
        if "ACTIVE" in table.table_status:
            return True
    except ClientError as error_message:
        return False


def bootstrap_table(table_name):
    """Adds basic data

    Ideally this would be a group command to accept params or a file

    """

    user_id = str(uuid.uuid4())
    user_email = fake.email()
    user_name = fake.name()

    try:
        table = dynamodb.Table(table_name)
        params = {
            "Item": {
                "id": user_id,
                "email": user_email,
                "name": user_name
            }
        }
        table.put_item(**params)        # This format will accept duplicates of same email
        response = table.query(
            KeyConditionExpression=Key('id').eq(user_id)
        )
        item = response['Items'][0]
        print(item)
        print("[+] Bootstrapping ran successfully...")
    except ClientError as error_message:
        print("[!] Failed to bootstrap table with demo data...")
        print(error_message)


def main():
    # Quick and dirty arg parsing
    parser = argparse.ArgumentParser(
        description='Quick and dirty create dynamoDB local for demo.')
    parser.add_argument(
        '-t', '--table', help='Table name to be created', required=True)
    parser.add_argument(
        '-p', '--hash-key', help='Primary key (Hash key)', required=True)
    # parser.add_argument(
    #     '-r', '--range-key', help='Range key (Range key)', required=True)
    args = parser.parse_args()

    if does_table_exist(args.table):
        print("[*] Table {} already exists! Skipping creation...".format(args.table))
    else:
        create_table(args.table, args.hash_key)
        # create_table(args.table, args.hash_key, args.range_key)

    try:
        bootstrap_table(args.table)
    except Exception as e:
        raise Exception("Operation failed due to {0}: ".format(e))


if __name__ == '__main__':
    main()
