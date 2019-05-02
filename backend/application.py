# Copyright 2013. Amazon Web Services, Inc. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import print_function
import os
import json

import boto3
from botocore.exceptions import ClientError

# Default config vals
FLASK_DEBUG = os.environ.get('FLASK_DEBUG') or 'false'
DYNAMODB_TABLE_NAME = os.environ['STARTUP_SIGNUP_TABLE']
SNS_TOPIC = os.environ['NEW_SIGNUP_TOPIC']

# Only enable Flask debugging if an env var is set to true
DEBUG = os.environ.get('FLASK_DEBUG') in ['true', 'True']

# Connect to DynamoDB and get ref to Table
DYNAMODB = boto3.resource('dynamodb')
DDB_TABLE = DYNAMODB.Table(DYNAMODB_TABLE_NAME)

# Connect to SNS
SNS = boto3.client('sns')


def signup(event, context):

    if DEBUG:
        print("[DEBUG] Signup with body: %s" % event['body'])
        print("[DEBUG] Event: %s" % json.dumps(event))
        print("[DEBUG] Context: %s" % json.dumps(context))

    signup_data = json.loads(event['body'])

    try:
        store_in_dynamo(signup_data)
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("already existing email")
            return _response(409, "Already existing")
    except Exception as ex:
        print(ex)
        return _response(500, "KO from DDB")

    try:
        publish_to_sns(signup_data)
    except Exception:
        print(ex)
        return _response(500, "KO from SNS")

    # all good
    return _response(201, "OK")

def _response(status, message):
    return {
        "body": json.dumps({"message": message}),
        "statusCode": status,
        "headers": {
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Credentials" : True,
            "Access-Control-Allow-Headers": "'x-requested-with'"
        },
    }


def store_in_dynamo(signup_data):
    DDB_TABLE.put_item(
        Item=signup_data,
    )


def publish_to_sns(signup_data):
    SNS.publish(
        TopicArn=SNS_TOPIC,
        Message=json.dumps(signup_data),
        Subject="New signup: %s" % signup_data['email'],
    )