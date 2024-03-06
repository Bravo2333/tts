import requests

# 设置请求的 URL
url = "http://127.0.0.1:5000/api//masterlist"

# JSON 数据，根据需要进行调整
data = {
    "ownerlink":'iJ1Lw2Xs'
}
response = requests.post(url, json=data)

# 检查响应状态码
if response.status_code == 200:
    # 将响应内容从 JSON 转换为 Python 字典
    response_data = response.json()
    print(response_data)