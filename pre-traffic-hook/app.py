import json
import boto3
import os


def lambda_handler(event, context):
    deploymentId = event["DeploymentId"]
    lifecycleEventHookExecutionId = event["LifecycleEventHookExecutionId"]
    client = boto3.client("lambda")
    codeclient = boto3.client("codedeploy")
    payload = {"message": "ping"}
    function_name = os.environ["CurrentVersion"]
    status = "Failed"
    resp = client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    dic = json.loads(resp["Payload"].read().decode("utf-8"))

    if dic["statusCode"] == 200:
        status = "Succeeded"
    else:
        status = "Failed"

    _ = codeclient.put_lifecycle_event_hook_execution_status(
        deploymentId=deploymentId,
        lifecycleEventHookExecutionId=lifecycleEventHookExecutionId,
        status=status,
    )