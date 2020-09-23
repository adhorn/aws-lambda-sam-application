#  aws-lambda-sam-application

This project contains Python source code and supporting files for a serverless application that you can deploy with the SAM CLI.

It tries to follow best practices:  
* CodeDeploy and Lambda traffic shifting for deployment. [More info](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/automating-updates-to-serverless-apps.html)
* Authorization with Cognito.
* Offline and local testing (WIP)
* Regional Custom domain name.
* AWS Lambda powertools for python [More Info](https://github.com/awslabs/aws-lambda-powertools-python)


## This project includes the following files and folders.

- application - Code for the application's Lambda functions (echo, get, and post).
- pre-traffic-hook - Code for the pretraffic hook used by CodeDeploy to monitor the deployment of new Lambda functions versions. [More info](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/automating-updates-to-serverless-apps.html)

- events - Invocation events that you can use to invoke the function.
- tests - Unit tests for the application code. 
- template.yaml - A template that defines the application's AWS resources.
- scripts - Support for creating the Cognito user pool and get TokenIDs for Auth. [Original source](https://github.com/jeffisadams/lambda-cognito-go)


The application uses several AWS resources, including Lambda functions, an API Gateway API, AWS CloudWatch alarms, and AWS CodeDeploy. These resources are defined in the `template.yaml` file in this project.

## Deploy the application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell (change the parameters to reflect your own)

```bash
> sam build --use-container
> sam deploy --guided --parameter-overrides ParameterKey=YourEmail,ParameterValue="sam@example.com" ParameterKey=DomainName,ParameterValue="sam.example.com" ParameterKey=CertificateArn,ParameterValue="arn:aws:acm:eu-west-1:12345678920:certificate/27857f5c-8bfa-45db-aaa1-00fc5302c65f"
```
The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modified IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

After the first deployment, you can omit ``` --guided ```

```bash
> sam deploy --parameter-overrides ParameterKey=YourEmail,ParameterValue="sam@example.com" ParameterKey=DomainName,ParameterValue="sam.example.com" ParameterKey=CertificateArn,ParameterValue="arn:aws:acm:eu-west-1:12345678920:certificate/27857f5c-8bfa-45db-aaa1-00fc5302c65f"
```

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
> sam build --use-container
```

The SAM CLI installs dependencies defined in `application/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
> sam local invoke Echo --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
> sam local start-api
> curl http://localhost:3000/
```

## Fetch, tail, and filter Lambda function logs

SAM CLI has a command called `sam logs` that lets you fetch logs generated by your deployed Lambda function from the command line. 

```bash
> sam logs -n Echo --stack-name sam-app1 --tail
```

## Unit tests

Tests are defined in the `tests` folder. Use PIP to install the [pytest](https://docs.pytest.org/en/latest/) and run unit tests.
Notice the testing happens offline with tracing disabled.

```bash
> pip install pytest pytest-mock --user
> python -m pytest tests/ -v
```

## Cleanup

To delete the application, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
> aws cloudformation delete-stack --stack-name sam-app1
```
