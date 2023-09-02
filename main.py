import requests
from lxml import html

userId = "用户输入" #学号
passwd = "用户输入" #密码


url = "https://10.254.241.3/webauth.do?&wlanacname=SC-CD-XXGCDX-SR8810-X"

requests.packages.urllib3.disable_warnings()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.0.0 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded"
}

payload = {
    "loginType": "",
    "auth_type": "0",
    "isBindMac1": "0",
    "pageid": "1",
    "templatetype": "1",
    "listbindmac": "0",
    "recordmac": "0",
    "isRemind": "1",
    "loginTimes": "",
    "groupId": "",
    "distoken": "",
    "echostr": "",
    "url": "",
    "isautoauth": "",
    "notice_pic_loop2": "/portal/uploads/pc/demo2/images/bj.png",
    "notice_pic_loop1": "/portal/uploads/pc/demo2/images/logo.png",
    "userId": userId,
    "passwd": passwd,
    "remInfo": "on"
}

response = requests.post(url, headers=headers, data=payload, verify=False)

if response.status_code == 200:
    root = html.fromstring(response.content)
    
    print(root)
    element = root.xpath('//*[@id="goLoginForm"]/div[1]/div/div[2]/div[2]/div[5]/p')
    
    if element:
        text_content = element[0].text_content().strip()
        print(text_content)
    else:
        print("未找到元素")
else:
    print(f"请求失败，状态码：{response.status_code}")
