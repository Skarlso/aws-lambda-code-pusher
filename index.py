# -*- coding: utf-8 -*-
"""
Main Github Pusher Code.
Copyright 2017-infinity @Gergely Brautigam
"""
import os
import boto3
import tarfile
import sys

# First create a Github instance:
TOKEN = os.environ.get("GITHUB_TOKEN")
S3_CLIENT = boto3.client('s3')
BUCKET = os.environ.get("BUCKET")
BLOG_PREFIX = '/tmp/public'
GIT_TAR = 'git-2.4.3.tar'


def install_git():
    print("Installing Git.")
    baseDir = '/tmp/git'
    tar = tarfile.open(GIT_TAR)
    tar.extractall(path=baseDir)
    tar.close()
    print("Extracted git tar into /tmp/git. Directory content: ")
    assert os.path.isdir(baseDir)
    assert os.path.isdir(os.path.join(baseDir, 'usr/bin'))
    print("Folder exists. Setting up environment properties.")
    os.environ['GIT_TEMPLATE_DIR'] = os.path.join(baseDir, 'usr/share/git-core/templates')
    os.environ['GIT_EXEC_PATH'] = os.path.join(baseDir, 'usr/libexec/git-core')
    os.environ['LD_LIBRARY_PATH'] = os.path.join(baseDir, 'usr/lib64')
    binDir = os.path.join(baseDir, 'usr/bin')
    os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = os.path.join(binDir, 'git')
    sys.path.append(binDir)
    print("Properties set. PATH is: %s." % sys.path)


def download_built_artifacts():
    """
    Downloads the blog's built source from the bucket.
    """
    print("Downloading artifacts.")
    s3_client = boto3.resource('s3')

    bucket = s3_client.Bucket(name=BUCKET)
    for obj in bucket.objects.filter(Prefix='%s/' % BLOG_PREFIX):
        print('{0}.{1}'.format(bucket.name, obj.key))
        path, _ = os.path.split(obj.key)
        os.makedirs(name=path, exist_ok=True)
        s3_client.meta.client.download_file(bucket.name, obj.key, obj.key)


def git_magic():
    print("Before Git, PATH is: %s." % sys.path)
    for param in os.environ.keys():
        print("%20s %s" % (param, os.environ[param]))
    import git
    print("Performing git magic.")
    source = git.Repo.init(path=os.path.join(os.getcwd(), BLOG_PREFIX))
    print("Repo initated.")
    origin = source.create_remote('origin', 'https://%s@github.com/Skarlso/skarlso.github.io.git' % TOKEN)
    origin.fetch()
    source.head.reset(commit='origin/master')
    source.heads.master.set_tracking_branch(origin.refs.master)
    source.heads.master.checkout()
    source.git.add(A=True)
    source.index.commit('Added new content.')
    source.git.push()
    print("Push done.")


def handler(event, context):
    """
    Lambda handler which gets called when a lambda executes.
    """

    # Install git executable and setup project path
    install_git()

    # Pull S3 artifact here and apply it to blog folder
    download_built_artifacts()

    # Setup a Git repo and make a push with the changes.
    git_magic()
    return None
