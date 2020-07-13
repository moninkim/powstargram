from storages.backends.s3boto3 import S3Boto3Storage
class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    bucket_name = 'powstargrambucket'

    region_name = 'us-east-1'
    custom_domain = 's3.%s.amazonaws.com/%s' % (region_name, bucket_name)