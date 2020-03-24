import requests
import hashlib
from airflow.contrib.hooks.redis_hook import RedisHook

def md5_str(string_input):
    md5_ins = hashlib.md5()
    md5_ins.update(string_input)
    return md5_ins.digest()

def download_google():
    r = requests.request('get', 'http://www.google.com')
    text = r.text

    with open('/tmp/downloader_test1', 'wb') as f:
        f.write(md5_str(text.encode('utf-8')))

def load_into_redis(file_path):
    print('checking {}'.format(file_path))

    lines = []

    with open('/tmp/downloader_test1', 'rb') as f:
        lines = f.readlines()

    file_md5 = ''.join([line.decode('latin-1') for line in lines])

    hook = RedisHook(redis_conn_id='redis_default')
    hook.host='redis'
    hook.port=6379
    redis = hook.get_conn()

    try:
        redis.ping()
    except Exception as e:
        print('could not ping redis')
        print(str(e))
        return

    redis.set('google', file_md5)
    md5_return_value = redis.get('google')
    print('set redis with keyvalue pair <google> {}'.format(md5_return_value))
    # redis.delete('test_key')
