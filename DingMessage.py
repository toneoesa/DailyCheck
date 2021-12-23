import time
import requests
import hmac
import hashlib
import base64
import urllib.parse


def DingMessage(message, access_token, secret):
    api_url = 'https://oapi.dingtalk.com/robot/send'
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(
        secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
    ).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    params = {
        'access_token': access_token,
        'timestamp': timestamp,
        'sign': sign,
    }
    data = {'msgtype': 'text', 'text': {'content': str(message)}}
    result = requests.post(api_url, params=params, json=data)
    return 'ok' in result.content.decode('utf-8')


if __name__ == '__main__':
    access_token = 'access_token'
    secret = 'secret'
    DingMessage(f'Test at {time.asctime()}', access_token, secret)
