import os
import boto3
from multiprocessing import Pool

s3_client = boto3.resource('s3')
BUCKET = os.environ.get("BUCKET")

bucket = s3_client.Bucket(name=BUCKET)


def download_single_file(f):
    print('{0}.{1}'.format(bucket.name, f))
    path, filename = os.path.split(f)
    os.makedirs(name=path, exist_ok=True)
    s3_client.meta.client.download_file(bucket.name, f, f)


def download_all_files(l):
    pool = Pool(processes=5)
    pool.map(download_single_file, l)


files = [obj.key for obj in bucket.objects.filter(Prefix='public/')]

download_all_files(files)

