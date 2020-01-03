
import oss2


class SDKOss(object):

    def __init__(self, access_key_id: str, access_key_secret: str, region_id: str):
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.endpoint = f'http://oss-{region_id}.aliyuncs.com'

    def get_bucket(self, bucket_name):
        return oss2.Bucket(self.auth, self.endpoint, bucket_name)

    def create_bucket(self, bucket_name: str):
        """
        创建存储空间
        https://help.aliyun.com/document_detail/32029.html?spm=a2c4g.11186623.6.831.7dc853f5ZlRfit
        :param bucket_name:
        :return:
        """
        return self.get_bucket(bucket_name).create_bucket()

    def list_buckets(self):
        """
        列举存储空间
        https://help.aliyun.com/document_detail/145656.html?spm=a2c4g.11186623.6.832.151d61d9OrotSJ
        :return:
        """
        service = oss2.Service(self.auth, self.endpoint)
        return [b.name for b in oss2.BucketIterator(service)]

    def get_bucket_info(self, bucket_name: str):
        """
        获取存储空间信息
        https://help.aliyun.com/document_detail/145657.html?spm=a2c4g.11186623.6.833.50833430BYKZZB
        :param bucket_name:
        :return:
        """
        return self.get_bucket(bucket_name).get_bucket_info()

    def delete_bucket(self, bucket_name: str):
        """
        删除存储空间
        https://help.aliyun.com/document_detail/145659.html?spm=a2c4g.11186623.6.835.5de444aagzAG5R
        :param bucket_name:
        :return:
        """
        return self.get_bucket(bucket_name).delete_bucket()

    def resumable_upload(self, bucket_name: str, object_name: str, local_file):
        """
        断点续传上传
        https://help.aliyun.com/document_detail/88433.html?spm=a2c4g.11186623.6.847.4c3e5779fGZANj
        :param bucket_name:
        :param object_name:
        :param local_file:
        :return:
        """
        bucket = self.get_bucket(bucket_name)
        oss2.resumable_upload(bucket, object_name, local_file,
                              store=oss2.ResumableStore(root='/tmp'),
                              multipart_threshold=100 * 1024,
                              part_size=100 * 1024,
                              num_threads=4)

    def put_object(self, bucket_name: str, key: str, object_content):
        """
        https://help.aliyun.com/document_detail/88426.html?spm=a2c4g.11186623.6.845.5de444aakBMWYp
        :param bucket_name:
        :param key:
        :param object_content:
        :return:
        """
        bucket = self.get_bucket(bucket_name)
        result = bucket.put_object(key, object_content)
        return result

    def put_object_from_file(self, bucket_name: str, key: str, filename):
        """
        上传本地文件
        https://help.aliyun.com/document_detail/88426.html?spm=a2c4g.11186623.6.845.5de444aakBMWYp
        :param bucket_name:
        :param key:
        :param filename:
        :return:
        """
        bucket = self.get_bucket(bucket_name)
        return bucket.put_object_from_file(key, filename=filename)
