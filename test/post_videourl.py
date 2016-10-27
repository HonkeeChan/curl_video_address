#encoding: utf8

import requests
import json
url = 'http://127.0.0.1:8888'
data = {
    "url": 'http://v.youku.com/v_show/id_XMTc2MjE2NTc1Mg==.html?spm=a2h0j.8191423.item_XMTc2MjE2NTc1Mg==.A&from=y1.2-2.4.1'
}

res = requests.post(url, data=data)
print res.content
# res = json.loads(res.content)
# if res["code"] == -1:
#     print res["msg"]
# elif res["code"] == 0:
#     print "finish download"
#     print res["data"]
# else:
#     print "in progress"