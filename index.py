# -*- coding: utf-8 -*-
"""
Main Github Pusher Code.
Copyright 2017-infinity @Gergely Brautigam
"""
import os
import git

# First create a Github instance:
TOKEN = os.environ.get("GITHUB_TOKEN")
source = git.Repo.clone_from('https://' + TOKEN + '@github.com/Skarlso/blogsource.git', os.path.join(os.getcwd(), 'blog'))

with open(os.path.join(os.getcwd(), 'blog', 'temp.file'), 'w') as temp_file:
    temp_file.write('test')

source.git.add(A=True)
source.index.commit('Added new content.')
source.git.push()
