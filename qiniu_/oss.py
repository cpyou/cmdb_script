from qiniu import Auth, put_file, config
from qiniu import http
from qiniu import BucketManager
from conf.qiniu import secret_id, secret_key, region
import time

EXPIRES = 5


class QiniuOSS:
    def __init__(self, access_key, secret_key, region):
        # 账户ak，sk
        self.auth = Auth(access_key=access_key, secret_key=secret_key)
        self.region = region

    def list_bucket(self):
        bucket = BucketManager(self.auth)
        ret, info = bucket.list_bucket(self.region)
        return ret

    def bucket_info(self, bucket_name):
        bucket = BucketManager(self.auth)
        ret, info = bucket.bucket_info(bucket_name)
        return ret

    def get_upload_token(self, bucket_name, key=None, policy=None):
        """
        https://developer.qiniu.com/kodo/sdk/1242/python#3
        :param bucket_name: 存储空间名称
        :param key: 上传后保存的文件名
        :param policy: {
            'callbackUrl':'http://your.domain.com/callback.php',
            'callbackBody':'filename=$(fname)&filesize=$(fsize)'
        }
        :return:
        """
        return self.auth.upload_token(bucket_name, key, expires=EXPIRES, policy=policy)

    @staticmethod
    def get_up_host_by_token(up_token):
        return config.get_default('default_zone').get_up_host_by_token(up_token)

    @staticmethod
    def upload_file(token, key, local_file):
        """
        上传本地文件
        :param token:
        :param key:
        :param local_file:
        :return:
        """
        ret, info = put_file(token, key, local_file)
        return ret, info


if __name__ == '__main__':

    q = QiniuOSS(secret_id, secret_key, region)
    # up_token = q.get_upload_token('cpy-test', '123')
    up_token = q.get_upload_token('cpy-test', '', policy={'isPrefixalScope': 1})
    res = q.upload_file(up_token, '123/456.jpg', '/Users/chenpuyu/Desktop/test/2020-01-0615.03.50.png')
    print(res)
    time.sleep(5)
    res1 = q.upload_file(up_token, '123/45678.jpg', '/Users/chenpuyu/Desktop/test/2020-01-0615.03.50.png')
    print(res1)
    # q.list_bucket(q.region)
    # print(q.bucket_info('mtl-app'))
