#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
from datetime import datetime

class CookieManager:
    def __init__(self):
        self.cookie_file = "data/cookies.json"
        self.verify_url = "https://www.douyin.com/user/self"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        }
        
        # 确保data目录存在
        os.makedirs(os.path.dirname(self.cookie_file), exist_ok=True)
        
    def save_cookies(self, cookies):
        """保存cookies到文件"""
        try:
            cookie_data = {
                "cookies": cookies,
                "timestamp": datetime.now().isoformat()
            }
            
            with open(self.cookie_file, "w", encoding="utf-8") as f:
                json.dump(cookie_data, f, ensure_ascii=False, indent=2)
            return True
            
        except Exception as e:
            print(f"保存cookies时出错: {str(e)}")
            return False
            
    def load_cookies(self):
        """从文件加载cookies"""
        try:
            if not os.path.exists(self.cookie_file):
                return None
                
            with open(self.cookie_file, "r", encoding="utf-8") as f:
                cookie_data = json.load(f)
            return cookie_data["cookies"]
            
        except Exception as e:
            print(f"加载cookies时出错: {str(e)}")
            return None
            
    def verify_cookies(self, cookies):
        """验证cookies是否有效"""
        try:
            session = requests.Session()
            session.cookies.update(cookies)
            
            response = session.get(
                self.verify_url,
                headers=self.headers,
                allow_redirects=False,
                timeout=10
            )
            
            print(f"验证响应状态码: {response.status_code}")  # 添加调试信息
            
            # 如果返回200且不是重定向，说明cookies有效
            return response.status_code == 200
            
        except Exception as e:
            print(f"验证cookies时出错: {str(e)}")
            return False 