# -*- coding: utf-8 -*-
"""
Main Github Pusher Code.
Copyright 2017-infinity @Gergely Brautigam
"""
import os
import git
import boto3

# First create a Github instance:
TOKEN = os.environ.get("GITHUB_TOKEN")
S3_CLIENT = boto3.client('s3')
BUCKET = os.environ.get("BUCKET")

def donwload_built_artifacts():
    """
    Downloads the blog's built source from the bucket.
    """
    s3_client = boto3.resource('s3')

    bucket = s3_client.Bucket(name=BUCKET)
    for obj in bucket.objects.filter(Prefix='datamunger/'):
        print('{0}.{1}'.format(bucket.name, obj.key))
        path, _ = os.path.split(obj.key)
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        s3_client.meta.client.download_file(bucket.name, obj.key, obj.key)


def handler(event, context):
    """
    Lambda handler which gets called when a lambda executes.
    """
    source = git.Repo.clone_from('https://' + TOKEN + '@github.com/Skarlso/blogsource.git', os.path.join(os.getcwd(), 'blog'))

    # Pull S3 artifact here and apply it to blog folder
    bucket = S3_CLIENT.Bucket(name=BUCKET)
    for obj in bucket.objects.filter(Prefix='public/'):
        S3_CLIENT.download_file(bucket.name, obj.key, './blog/obj.key')

    # response = S3_CLIENT.list_objects(Bucket=BUCKET, Prefix='public/', Delimiter='/')
    source.git.add(A=True)
    source.index.commit('Added new content.')
    source.git.push()
    return None
