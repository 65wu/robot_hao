import requests,json

url = "http://openapi.tuling123.com/openapi/api/v2"

data = {
	"reqType":0,
    "perception": {
        "inputText": {
            "text": "明天会下雨吗"
        },
        "selfInfo": {
            "location": {
                "city": "北京",
                "province": "北京",
                "street": "信息路"
            }
        }
    },
    "userInfo": {
        "apiKey": "b6aab09b04ef41898b85f60e18b69940",
        "userId": "haohao"
    }
}
data = json.dumps(data).encode('utf8')
res = requests.post(url,data=data)
print(res.text)