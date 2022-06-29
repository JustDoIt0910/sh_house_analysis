import requests
from requests.cookies import RequestsCookieJar
from conf import cfg
from lxml import etree
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher


class Cas:

    def __init__(self):
        self.loginTicketId = None
        self.publicKey = None
        self.encodeVersion = "1"

    # 获取 loginTicket 和 公钥，由于后续密码加密
    def auth_initialize(self):
        ini_data = {
            "service": "https://www.lianjia.com/user/checklogin?redirect=https%3A%2F%2Faq.lianjia.com%2Fchengjiao%2F",
            "context": {
                "deviceId": "default",
                "sign": "default"
            },
            "version": "2.0"
        }
        cas_ini_url = cfg.cfg["application"]["cas_initialize"]

        ini_resp = requests.post(cas_ini_url, json=ini_data)
        resp_data = ini_resp.json()
        self.loginTicketId = resp_data["loginTicketId"]
        self.publicKey = resp_data["publicKey"]["key"]
        self.encodeVersion = resp_data["publicKey"]["version"]

        jar = RequestsCookieJar()
        for k, v in ini_resp.cookies.items():
            jar.set(k, v)
        return jar

    # 登录，获取 TGT
    def auth_authenticate(self, jar):
        if self.encodeVersion == "1":
            pwd = self.rsa_encrypt()
        else:
            pwd = self.rsa2_encrypt()
        auth_data = {
            "mainAuthMethodName": "username-password",
            "credential": {
                "username": "18753103857",
                "password": pwd,
                "ioaRunState": False,
                "ioaMid": "{}",
                "alertSt": "",
                "ioaStateVersion": 2,
                "encodeVersion": self.encodeVersion
            },
            "srcId": "eyJ0Ijoie1wiZGF0YVwiOlwiZDM2MTgyYmMxZDcxYzA1ODlmODA3NThlYzZjMGJhZWVhNzdiNzcwMDczZDY0MmYwYThjMWQ0ZWEzNmVlMzE2NzczYWRkNTBmMGU3NTkzYzIxNTNmM2NhZjViODUyNzc3MGQ0NmIzOWNlYjliZWIxNDZkNzU2ZTBiMGFhNTkxNTMwYmE2ODYxMThmYjk4MDM0ODM0MTMyZGRlYTc5M2ZkNDYwYTU5Y2M1MDI3MzQzY2ViNTJhNjkyMzFkOGZlOGU3YTg1MTE4NDVkOTlmZTcyMzNhNGM0NDEwNjRjNDkzNTU0NmI1OWJlMjlhYTk1OTQwZmNmNDg2MmZkNGZhYjhkYlwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI1Y2I3Njg3YVwifSIsInIiOiJodHRwczovL2Nsb2dpbi5saWFuamlhLmNvbS9sb2dpbj9zZXJ2aWNlPWh0dHBzJTNBJTJGJTJGd3d3LmxpYW5qaWEuY29tJTJGdXNlciUyRmNoZWNrbG9naW4lM0ZyZWRpcmVjdCUzRGh0dHBzJTI1M0ElMjUyRiUyNTJGYXEubGlhbmppYS5jb20lMjUyRmNoZW5namlhbyUyNTJGIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=",
            "context": {
                "msg": "{}",
                "deviceId": "default",
                "sign": "default"
            },
            "version": "2.0",
            "accountSystem": "customer",
            "service": "https://www.lianjia.com/user/checklogin?redirect=https%3A%2F%2Faq.lianjia.com%2Fchengjiao%2F",
            "loginTicketId": self.loginTicketId
        }

        cas_auth_url = cfg.cfg["application"]["cas_authenticate"]
        resp = requests.post(cas_auth_url, json=auth_data, cookies=jar)
        jar = RequestsCookieJar()
        for k, v in resp.cookies.items():
            jar.set(k, v)
        return jar

    # 调用一个在线 rsa2 加密的网页
    def rsa2_encrypt(self):
        rsa_post_data = {
            "key": self.publicKey,
            "content": cfg.cfg["account"]["password"]
        }
        rsa_encrypt_url = cfg.cfg["application"]["rsa_encrypt_url"]
        rsa_resp_html = requests.post(rsa_encrypt_url, data=rsa_post_data).text
        doc = etree.HTML(rsa_resp_html, etree.HTMLParser())
        password = doc.xpath("//textarea[@id='rsa_result']/text()")[0]
        return password

    def rsa_encrypt(self):
        key = "-----BEGIN RSA PUBLIC KEY-----\n" + self.publicKey + "\n-----END RSA PUBLIC KEY-----"
        cipher = PKCS1_cipher.new(RSA.importKey(key.encode()))
        pwd = cfg.cfg["account"]["password"]
        encrypt_text = base64.b64encode(cipher.encrypt(pwd.encode("utf-8")))
        return encrypt_text.decode('utf-8')

    # 登录
    def login(self):
        _cookie = self.auth_initialize()
        return self.auth_authenticate(_cookie)


if __name__ == '__main__':
    cas = Cas()
    cookie = cas.login()
    print(cookie)
