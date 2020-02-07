import requests
import json
import time
import base64
import random
import hashlib

# 姓名和学号
name = input("输入姓名：")
number = input("输入学号：")

# We 的 IP 高精度定位 API
loc_api_url = "https://apis.map.qq.com/ws/location/v1/ip"
loc_api_para = {
    'key': 'IVOBZ-QNW6P-SUKDY-LFQSE-LUFCJ-3CFUE',
    'sig': 'afebe5ad5227ec75a1f3d8b97f888cda'
}

# 请求高精度 GPS 坐标和区县级地址
loc = requests.get(loc_api_url, params=loc_api_para)
lat = loc.json()['result']['location']['lat']
lng = loc.json()['result']['location']['lng']
province = loc.json()['result']['ad_info']['province']
city = loc.json()['result']['ad_info']['city']
district = loc.json()['result']['ad_info']['district']

# 随机一个 sign
md5 = hashlib.md5(str(random.randint(0, 114514)).encode('utf-8'))
sign = md5.hexdigest()

# 构造打卡数据
address = province + ',' + city + ',' + district
key = {'latitude': lat, 'longitude': lng, 'name': name, 'xh': number, 'szdq': address, 'sfhxdgr': '否', 'stsfjk': '健康',
       'sffr': '否', 'sfks': '否', 'sfxm': '否', 'qtycqk': '无', 'beizhu': '无', 'timestamp': int(time.time()), 'sign': sign}
key_base64 = base64.b64encode(json.dumps(key).encode('utf-8'))
post_data = {'key': key_base64.decode('utf-8')}

# 构造并执行 HTTP POST 请求
headers = {
    'Host': 'we.cqu.pt',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 '
                  'Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat ',
    'content-type': 'application/json',
    'Referer': 'https://servicewechat.com/wx8227f55dc4490f45/25/page-frame.html'
}
result = requests.post('https://we.cqu.pt/api/mrdk/post_mrdk_info.php', data=json.dumps(post_data), headers=headers)

# 判断是否打卡成功
if result.json()['message'] == 'OK':
    print("打卡成功")
else:
    print("打卡失败")
print("5 秒后退出")
time.sleep(5)
