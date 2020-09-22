import json
import boto3
import os


def lambda_handler(event, context):
    deploymentId = event["DeploymentId"]
    lifecycleEventHookExecutionId = event["LifecycleEventHookExecutionId"]
    lambda_client = boto3.client("lambda")
    payload = {"message": "ping"}
    function_name = os.environ["CurrentVersion"]  # [docs] recommended to pass the lambda version through the Environment Variables
    resp = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    dic = json.loads(resp["Payload"].read().decode("utf-8"))

    status = "Failed"

    if dic["statusCode"] == 200:
        status = "Succeeded"
    else:
        status = "Failed"

    codedeploy_client = boto3.client("codedeploy")

    _ = codedeploy_client.put_lifecycle_event_hook_execution_status(
        deploymentId=deploymentId,
        lifecycleEventHookExecutionId=lifecycleEventHookExecutionId,
        status=status,
    )