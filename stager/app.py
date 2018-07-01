#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Zhen Qin
# @File : app.py


import os
import boto3
import botocore

from flask import Flask, jsonify, request, abort

from shutil import copy


BUCKET_NAME = '297517727354-kate-bucket'

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to Kate Stager!"


@app.route('/stager', methods=['POST'])
def create_task():
    if not request.json:  # or not 'title' in request.json:
        abort(400)
    inputs = convert(request.get_json(force=True))
    task = {
        'file': inputs['file'],
        'app_id': inputs['appid'],
        'app_name': inputs['appname'],
        'space': inputs['space'],
        'org': inputs['org']
    }
    file_name = download_file(task['file'])
    image_id = build_push_image(task, file_name)

    return jsonify({'image_identifier': image_id}), 201


# convert json templates in unicode format to string format for both key and value.
def convert(data):
    str_data = dict([(str(k), str(v)) for k, v in data.items()])
    return str_data


# download the user's file from AWS s3 bucket to local.
def download_file(key):
    s3 = boto3.resource('s3')
    file_name = key
    if '/' in key:
        file_name = key.split('/')[1]
    try:
        s3.Bucket(BUCKET_NAME).download_file(key, file_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    return file_name


# build docker image and push it to docker hub.
def build_push_image(task, file_name):
    tag = task['app_id'] + '-' + task['app_name'] + '-' + task['space'] + '-' + task['org']
    image_tag = 'demo/' + tag
    dest = 'Dockerfile'
    copy('templates/DockerfileTemplate', dest)

    with open(dest) as f:
        new_text = f.read().replace('application.zip', file_name)
    with open(dest, 'w') as f:
        f.write(new_text)

    os.system('sudo docker build -t ' + image_tag + ' .')
    push_cmd = 'sudo docker image push ' + image_tag
    os.system(push_cmd)

    return image_tag


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
