# 实现图片上传并返回链接
import json
import logging
import sys
import time

# pip install -U cos-python-sdk-v5

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from Calendar import settings

with open('api_key.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    secret_id = data.get("cos-secret-id")
    secret_key = data.get("cos-secret-key")
    bucket_name = data.get("cos-bucket-name")

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 设置用户属性
# Appid 已在CosConfig中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
region = 'ap-beijing'
token = None
scheme = 'https'

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)


# 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py


def upload_percentage(consumed_bytes, total_bytes):
    """进度条回调函数，计算当前上传的百分比


    :param consumed_bytes: 已经上传的数据量
    :param total_bytes: 总数据量
    """
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate))
        sys.stdout.flush()


def upload(path: str, title: str):
    key = str(time.time())[:4] + title
    response = client.upload_file(
        Bucket=bucket_name,
        Key=key,
        LocalFilePath=path,
        PartSize=1,
        MAXThread=5,
        progress_callback=upload_percentage,
        EnableMD5=False,
        ACL='public-read',
    )

    url = client.get_object_url(
        Bucket=bucket_name,
        Key=key
    )

    return url


if __name__ == "__main__":
    url = upload("images/#金汤豆花鱼.jpg", "pic_test.png")
    print(url)
