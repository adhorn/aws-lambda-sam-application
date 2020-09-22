#!/bin/bash
# original version from https://github.com/jeffisadams/lambda-cognito-go

CLIENT_ID=$1
USERNAME=$2
PASSWORD=$3

aws cognito-idp initiate-auth \
--auth-flow USER_PASSWORD_AUTH \
--auth-parameters "USERNAME=$2,PASSWORD=$3" \
--client-id $1