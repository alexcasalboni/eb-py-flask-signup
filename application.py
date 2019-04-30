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

import os
import sys
import json

import flask
from flask import request, Response

from boto import dynamodb2
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.exceptions import ConditionalCheckFailedException
from boto import sns

# Default config vals
FLASK_DEBUG = os.environ.get('FLASK_DEBUG') or 'false'

# Create the Flask app
app = flask.Flask(__name__)

# Load config values specified above
app.config.from_object('config')

# Load configuration vals from a file
app.config.from_envvar('APP_CONFIG', silent=True)

# Only enable Flask debugging if an env var is set to true
app.debug = app.config['FLASK_DEBUG'] in ['true', 'True']

# Connect to DynamoDB and get ref to Table
ddb_conn = dynamodb2.connect_to_region(app.config['AWS_REGION'])
ddb_table = Table(
    table_name=app.config['STARTUP_SIGNUP_TABLE'],
    connection=ddb_conn,
)

# Connect to SNS
sns_conn = sns.connect_to_region(app.config['AWS_REGION'])


@app.route('/')
def welcome():
    return flask.render_template('index.html')


@app.route('/signup', methods=['POST'])
def signup():
    if app.debug:
        print "[DEBUG] Signup with body: %s" % json.dumps(request.form)

    signup_data = dict()
    for item in request.form:
        signup_data[item] = request.form[item]

    try:
        store_in_dynamo(signup_data)
        publish_to_sns(signup_data)
    except ConditionalCheckFailedException:
        return Response("", status=409, mimetype='application/json')

    return Response(json.dumps(signup_data), status=201, mimetype='application/json')


def store_in_dynamo(signup_data):
    signup_item = Item(ddb_table, data=signup_data)
    signup_item.save()


def publish_to_sns(signup_data):
    try:
        sns_conn.publish(app.config['NEW_SIGNUP_TOPIC'], json.dumps(signup_data), "New signup: %s" % signup_data['email'])
    except Exception as ex:
        sys.stderr.write("Error publishing subscription message to SNS: %s" % ex.message)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
