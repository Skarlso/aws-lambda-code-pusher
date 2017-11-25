import os
import git

BLOG_PREFIX = 'test_blog'
TOKEN = os.environ.get("GITHUB_TOKEN")

def git_magic():
    source = git.Repo.init(path=os.path.join('/Users/hannibal', BLOG_PREFIX))
    origin = source.create_remote('origin', 'https://%s@github.com/Skarlso/blogsource.git' % TOKEN)
    origin.fetch()
    source.head.reset(commit='origin/master')
    source.heads.master.set_tracking_branch(origin.refs.master)
    source.heads.master.checkout()
    source.git.add(A=True)
    source.index.commit('Added new content.')
    source.git.push()

git_magic()
