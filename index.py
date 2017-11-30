# -*- coding: utf-8 -*-
"""
Main Github Pusher Code.
Copyright 2017-infinity @Gergely Brautigam
"""
import os
import boto3
import tarfile
import sys
import zipfile

# First create a Github instance:
BUCKET = os.environ.get("BUCKET")
REPO = os.environ.get("REPO")
GIT_TAR = 'git-2.4.3.tar'
# BLOG_ARCHIVE = 'blog.zip'
EMAIL = os.environ.get("COMMITTER_EMAIL")
NAME = os.environ.get("COMMITTER_NAME")
BLOG_ARCHIVE = os.environ.get("ARCHIVE") + '.zip'


def install_git():
    print("Installing Git.")
    baseDir = '/tmp/git'
    with tarfile.open(GIT_TAR) as tar:
        tar.extractall(path=baseDir)
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


def download_blog_archive():
    s3_client = boto3.resource('s3')
    s3_client.meta.client.download_file(BUCKET, BLOG_ARCHIVE, '/tmp/blog.zip')
    assert os.path.isfile('/tmp/blog.zip')
    print('Blog zip successfully downloaded. Extracting now.')
    with zipfile.ZipFile('/tmp/blog.zip', 'r') as zip_ref:
        zip_ref.extractall('/tmp/public')
    assert os.path.isdir('/tmp/public')
    print('Zip extracted.')


def git_magic():
    print("Before Git, PATH is: %s." % sys.path)
    for param in os.environ.keys():
        print("%20s %s" % (param, os.environ[param]))
    import git
    print("Performing git magic.")
    source = git.Repo.init(path='/tmp/public')
    print("Repo initated.")
    origin = source.create_remote('origin', REPO)
    origin.fetch()
    source.head.reset(commit='origin/master')
    source.heads.master.set_tracking_branch(origin.refs.master)
    source.heads.master.checkout()
    source.git.add(A=True)
    from git import Actor
    author = Actor(NAME, EMAIL)
    committer = Actor(NAME, EMAIL)
    source.index.commit(message='Added new content through AWS Lambda.', author=author, committer=committer)
    source.git.push()
    print("Push done.")


def handler(event, context):
    """
    Lambda handler which gets called when a lambda executes.
    """

    # Install git executable and setup project path
    install_git()

    # Pull S3 artifact here and apply it to blog folder
    download_blog_archive()

    # Setup a Git repo and make a push with the changes.
    git_magic()
    return None
