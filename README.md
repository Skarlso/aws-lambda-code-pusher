# Code Pusher

This is a small lambda function to take a change from an S3 bucket and apply it to a checked out repository.

After the change has been applied it's pushed up to the remote.

Deploy the stack: [![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=blogbuilder&templateURL=https://s3.amazonaws.com/blog-builder-template-bucket/template.yaml)
