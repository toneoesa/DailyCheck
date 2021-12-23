from base64 import b64decode
import random
import json
import requests


def check(id, pwd):
    lng = 108.835455 + (random.random() * 2 - 1) / 1000
    lat = 34.124031 + (random.random() * 2 - 1) / 1000
    accuracy = random.choice([10, 20, 25])
    data_raw = {
        "ymtys": "0",
        "sfzx": "1",
        "tw": "1",
        "area": "\u9655\u897f\u7701 \u897f\u5b89\u5e02 \u957f\u5b89\u533a",
        "city": "\u897f\u5b89\u5e02",
        "province": "\u9655\u897f\u7701",
        "address": "\u9655\u897f\u7701\u897f\u5b89\u5e02\u957f\u5b89\u533a\u5174\u9686\u8857\u9053\u4e01\u9999\u8def"
                   "\u897f\u5b89\u7535\u5b50\u79d1\u6280\u5927\u5b66\u957f\u5b89\u6821\u533a",
        "geo_api_info": '{"type":"complete","position":{"Q":' + str(round(lat, 12))
                        + ',"R":' + str(round(lng, 14))
                        + ',"lng":' + str(round(lng, 6))
                        + ',"lat":' + str(round(lat, 6))
                        + '},"location_type":"html5","message":"Get geolocation success.Convert Success.Get address '
                          'success.","accuracy": ' + str(accuracy)
                        + ',"isConverted":true,"status":1,"addressComponent":{"citycode":"029","adcode":"610116",'
                          '"businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"",'
                          '"buildingType":"","street":"\u96f7\u7518\u8def","streetNumber":"266#",'
                          '"country":"\u4e2d\u56fd","province":"\u9655\u897f\u7701","city":"\u897f\u5b89\u5e02",'
                          '"district":"\u957f\u5b89\u533a","township":"\u5174\u9686\u8857\u9053"},'
                          '"formattedAddress":"\u9655\u897f\u7701\u897f\u5b89\u5e02\u957f\u5b89\u533a\u5174\u9686'
                          '\u8857\u9053\u4e01\u9999\u8def\u897f\u5b89\u7535\u5b50\u79d1\u6280\u5927\u5b66\u957f\u5b89'
                          '\u6821\u533a","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"}',
        "sfcyglq": "0",
        "sfyzz": "0",
        "qtqk": "",
    }

    conn = requests.Session()
    result = conn.post(
        url=b64decode(b'aHR0cHM6Ly94eGNhcHAueGlkaWFuLmVkdS5jbi91Yy93YXAvbG9naW4vY2hlY2s=').decode('utf-8'),
        data={"username": id, "password": pwd},
    )

    if "账号或密码错误" in result.text:
        conn.close()
        return {"State": False, "Info": "Failed to login." + str(result.status_code)}

    result = conn.post(
        url=b64decode(
            b'aHR0cHM6Ly94eGNhcHAueGlkaWFuLmVkdS5jbi94aXN1bmNvdi93YXAvb3Blbi1yZXBvcnQvc2F2ZQ=='
        ).decode('utf-8'),
        data=data_raw
    )

    if result.status_code != 200:
        conn.close()
        return {"State": False, "Info": "Network Error." + str(result.status_code)}

    rjson = json.loads(result.text)
    return {"State": True, "Info": str(rjson["m"])}
