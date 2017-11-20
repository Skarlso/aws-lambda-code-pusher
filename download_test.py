import os
import boto3

s3_client = boto3.resource('s3')
BUCKET = os.environ.get("BUCKET")

bucket = s3_client.Bucket(name=BUCKET)
for obj in bucket.objects.filter(Prefix='datamunger/'):
    print('{0}.{1}'.format(bucket.name, obj.key))
    path, filename = os.path.split(obj.key)
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    s3_client.meta.client.download_file(bucket.name, obj.key, obj.key)
