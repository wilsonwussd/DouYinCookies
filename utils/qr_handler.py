#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import qrcode
import requests
import json
import time
import random
from PIL import Image
from io import BytesIO
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class QRCodeHandler:
    def __init__(self):
        self.session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=3,  # 最大重试次数
            backoff_factor=1,  # 重试间隔
            status_forcelist=[500, 502, 503, 504]  # 需要重试的HTTP状态码
        )
        
        # 配置适配器
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.qr_id = None
        self.device_id = str(random.randint(10000000000, 99999999999))
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://www.douyin.com",
            "Referer": "https://www.douyin.com/",
            "Cookie": "",
            "Host": "www.douyin.com",
            "Connection": "keep-alive"
        }
        
    def _make_request(self, method, url, **kwargs):
        """发送请求的通用方法，包含重试逻辑"""
        kwargs.setdefault('timeout', 30)  # 设置默认超时时间为30秒
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:  # 最后一次重试
                    raise
                print(f"请求失败，正在重试 ({attempt + 1}/{max_retries}): {str(e)}")
                time.sleep(2 ** attempt)  # 指数退避
        
    def generate_qr_code(self):
        """生成登录二维码"""
        try:
            # 首先访问主页获取必要的cookies
            self._make_request("GET", "https://www.douyin.com/", headers=self.headers)
            
            # 获取二维码ID
            data = {
                "service": "https://www.douyin.com",
                "need_logo": False,
                "device_id": self.device_id,
                "aid": 1128,
                "platform": "web_pc",
                "web_timestamp": int(time.time())
            }
            
            response = self._make_request(
                "POST",
                "https://sso.douyin.com/get_qrcode/",
                headers=self.headers,
                json=data
            )
            
            try:
                data = response.json()
                print(f"获取二维码响应: {data}")
            except json.JSONDecodeError as e:
                print(f"解析响应失败: {str(e)}")
                print(f"响应内容: {response.text}")
                return None
                
            if data.get("data", {}).get("qrcode"):
                self.qr_id = data["data"]["token"]
                qr_url = data["data"]["qrcode"]
                
                if not qr_url:
                    print(f"未找到二维码URL: {data}")
                    return None
                    
                # 生成二维码图片
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_url)
                qr.make(fit=True)
                
                qr_image = qr.make_image(fill_color="black", back_color="white")
                return qr_image
            else:
                print(f"获取二维码失败: {data}")
                return None
                
        except Exception as e:
            print(f"生成二维码时出错: {str(e)}")
            return None
            
    def check_login(self):
        """检查登录状态"""
        if not self.qr_id:
            return False
            
        try:
            data = {
                "token": self.qr_id,
                "service": "https://www.douyin.com",
                "device_id": self.device_id,
                "web_timestamp": int(time.time())
            }
            
            response = self._make_request(
                "POST",
                "https://sso.douyin.com/check_qrconnect/",
                headers=self.headers,
                json=data
            )
            
            try:
                data = response.json()
                print(f"检查登录状态响应: {data}")
            except json.JSONDecodeError:
                print("解析登录状态响应失败")
                return False
                
            # 检查登录状态
            if data.get("data", {}).get("status") == "confirmed":
                return True
            elif data.get("data", {}).get("status") == "scanned":
                print("已扫码，等待确认")
            else:
                print("等待扫码")
            return False
            
        except Exception as e:
            print(f"检查登录状态时出错: {str(e)}")
            return False
            
    def get_cookies(self):
        """获取登录后的cookies"""
        if not self.session.cookies:
            return None
            
        return self.session.cookies.get_dict() 