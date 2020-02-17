import requests
import json
import time
import base64
import random
import hashlib

# 姓名和学号
name = input("输入姓名：")
number = input("输入学号：")
phone = input("输入电话：")
area = input("输入小区 / 社区 / 村镇 / 寝室号：")
leave = input("是否已离开重庆（“是”或“否”）：")
infected = input("所在地是否有感染 / 疑似病例（“无”或“有”）：")

# 微信小程序的固定 HTTP 请求头
headers = {
    'Host': 'we.cqu.pt',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 '
                  'Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat ',
    'content-type': 'application/json',
    'Referer': 'https://servicewechat.com/wx8227f55dc4490f45/25/page-frame.html'
}

# We 的 IP 高精度定位 API
loc_api_url = "https://apis.map.qq.com/ws/location/v1/ip"
loc_api_para = {
    'key': 'IVOBZ-QNW6P-SUKDY-LFQSE-LUFCJ-3CFUE',
    'sig': 'afebe5ad5227ec75a1f3d8b97f888cda'
}


# 随机一个 sign
def sign():
    md5 = hashlib.md5(str(random.randint(0, 114514)).encode('utf-8'))
    return md5.hexdigest()


# 官方打卡次数查询接口
def check_status():
    # 构造并执行原版打卡次数查询请求
    check_key = {'xh': number, 'timestamp': int(time.time()), 'sign': sign()}
    check_key_base64 = base64.b64encode(json.dumps(check_key).encode('utf-8'))
    check_data = {'key': check_key_base64.decode('utf-8')}
    count = requests.post('https://we.cqu.pt/api/mrdk/get_mrdk_flag.php', data=json.dumps(check_data), headers=headers)
    return int(count.json()['data']['count'])


# 官方每日打卡接口
def check_in():
    # 请求高精度 GPS 坐标和区县级地址
    # TODO: 简化此部分代码（好像没什么可以简化的
    print("正在请求 GPS 坐标和区县级地址...")
    loc = requests.get(loc_api_url, params=loc_api_para)
    lat = loc.json()['result']['location']['lat']
    lng = loc.json()['result']['location']['lng']
    province = loc.json()['result']['ad_info']['province']
    city = loc.json()['result']['ad_info']['city']
    district = loc.json()['result']['ad_info']['district']
    address = province + ',' + city + ',' + district
    print("成功，经纬度：" + str(lat) + "°N, " + str(lng) + "°E, 所在地：" + address)

    # 创建打卡数据
    key = {'jbsks': '否', 'jbsfl': '否', 'jbsbs': '否', 'jbslt': '否', 'jbsyt': '否', 'jbsfx': '否', 'name': name,
           'xh': number, 'xb': '', 'latitude': lat, 'longitude': lng, 'lxdh': phone,
           'szdq': address, 'xxdz': area, 'hjsfly': leave, 'sfyfy': '否', 'xjzdywqzbl': infected, 'twsfzc': '是',
           'ywytdzz': '无', 'brsfqz': '无', 'brsfys': '无', 'ywjchblj': '无', 'fyjtgj': '无', 'fyddsj': '无',
           'sfbgsq': '无', 'sfjjgl': '无', 'jjglqssj': '无', 'wjjglmqqx': '无', 'qtycqk': '无', 'beizhu': '填写其他需要说明的情况',
           'ywjcqzbl': '无', 'timestamp': int(time.time()), 'sign': sign()}
    key_base64 = base64.b64encode(json.dumps(key).encode('utf-8'))
    post_data = {'key': key_base64.decode('utf-8')}

    # 构造并执行 HTTP POST 请求
    print("正在提交打卡请求...")
    result = requests.post('https://we.cqu.pt/api/mrdk/post_mrdk_info.php', data=json.dumps(post_data), headers=headers)
    return result.json()


# 主循环
while 1 == 1:
    # 判断是否已打卡
    if check_status() > 0:
        print(time.strftime("%Y-%m-%d", time.localtime()) + " 已打卡，不再重复打卡")
    else:
        print(time.strftime("%Y-%m-%d", time.localtime()) + " 未打卡，开始执行打卡")
        # 判断是否打卡成功（返回 JSON 判断）
        # TODO：下面两个失败重试和简化
        if check_in()['message'] == 'OK':
            # 判断是否打卡成功（当天打卡次数判断）
            if check_status() > 0:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 打卡成功")
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 打卡失败")
        else:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 打卡请求提交失败")
    print("1 天后再次执行")
    time.sleep(86392)
