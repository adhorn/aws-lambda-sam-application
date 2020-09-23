#!/bin/bash
# original version from https://github.com/jeffisadams/lambda-cognito-go

USERPOOLID=$1
CLIENT_ID=$2
USERNAME=$3
PASSWORD=$4

# Do an initial login
# It will come back wtih a challenge response
AUTH_CHALLENGE_SESSION=`aws cognito-idp initiate-auth \
--auth-flow USER_PASSWORD_AUTH \
--auth-parameters "USERNAME=$3,PASSWORD=$4" \
--client-id $2 \
--query "Session" \
--output text`

echo "Then respond to the challenge"

# Then respond to the challenge
AUTH_TOKEN=`aws cognito-idp admin-respond-to-auth-challenge \
--user-pool-id $USERPOOLID \
--client-id $2 \
--challenge-responses "NEW_PASSWORD=Testing1,USERNAME=$3" \
--challenge-name NEW_PASSWORD_REQUIRED \
--session $AUTH_CHALLENGE_SESSION \
--query "AuthenticationResult.IdToken" \
--output text`

# Tell the world
echo "Changed the password to Testing1"
echo "Logged in ID Auth Token: "
echo $AUTH_TOKEN