#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
from utils.cookie_manager import CookieManager

class DouYinCookieManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("抖音Cookies管理工具")
        self.root.geometry("600x700")
        
        self.cookie_manager = CookieManager()
        
        self.setup_ui()
        
    def setup_ui(self):
        # 创建标题标签
        title_label = tk.Label(self.root, text="抖音Cookies管理工具", font=("Arial", 16))
        title_label.pack(pady=20)
        
        # 创建说明文本
        instruction_text = """
使用说明：
1. 使用Chrome浏览器登录抖音网页版
2. 安装 'Cookie Editor' 扩展
3. 登录成功后，点击扩展图标
4. 点击 'Export' -> 'Export as JSON'
5. 复制导出的JSON内容
6. 粘贴到下方文本框中
7. 点击 '导入Cookies' 按钮
        """
        instruction_label = tk.Label(self.root, text=instruction_text, justify=tk.LEFT, font=("Arial", 10))
        instruction_label.pack(pady=10, padx=20)
        
        # 创建文本框框架
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建标签
        text_label = tk.Label(text_frame, text="请在下方粘贴 Cookie Editor 导出的 JSON 内容：", font=("Arial", 10))
        text_label.pack(anchor=tk.W)
        
        # 创建文本框
        self.cookie_text = scrolledtext.ScrolledText(text_frame, height=15, width=60, font=("Courier", 10))
        self.cookie_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # 创建导入按钮
        self.import_button = tk.Button(button_frame, text="导入Cookies", command=self.import_cookies)
        self.import_button.pack(side=tk.LEFT, padx=10)
        
        # 创建验证按钮
        self.verify_button = tk.Button(button_frame, text="验证Cookies", command=self.verify_cookies)
        self.verify_button.pack(side=tk.LEFT, padx=10)
        
        # 创建清除按钮
        self.clear_button = tk.Button(button_frame, text="清除内容", command=self.clear_text)
        self.clear_button.pack(side=tk.LEFT, padx=10)
        
        # 创建状态标签
        self.status_label = tk.Label(self.root, text="等待操作...", font=("Arial", 10))
        self.status_label.pack(pady=20)
        
    def clear_text(self):
        """清除文本框内容"""
        self.cookie_text.delete(1.0, tk.END)
        self.status_label.config(text="文本框已清空")
        
    def import_cookies(self):
        """导入Cookies"""
        try:
            # 获取文本框内容
            cookie_json = self.cookie_text.get(1.0, tk.END).strip()
            if not cookie_json:
                self.status_label.config(text="请先粘贴Cookie内容")
                messagebox.showwarning("警告", "请先粘贴Cookie内容")
                return
                
            # 解析JSON
            try:
                cookies_list = json.loads(cookie_json)
            except json.JSONDecodeError:
                self.status_label.config(text="无效的JSON格式")
                messagebox.showerror("错误", "无效的JSON格式，请确保复制了完整的JSON内容")
                return
                
            # 转换为字典格式
            cookies = {}
            for cookie in cookies_list:
                if cookie.get('domain', '').endswith('douyin.com'):
                    cookies[cookie['name']] = cookie['value']
            
            if not cookies:
                self.status_label.config(text="未找到有效的抖音Cookies")
                messagebox.showwarning("警告", "未找到有效的抖音Cookies")
                return
                
            # 保存Cookies
            if self.cookie_manager.save_cookies(cookies):
                self.status_label.config(text="Cookies导入成功！")
                messagebox.showinfo("成功", "Cookies导入成功！")
                self.cookie_text.delete(1.0, tk.END)  # 清空文本框
            else:
                self.status_label.config(text="Cookies保存失败")
                messagebox.showerror("错误", "Cookies保存失败")
                
        except Exception as e:
            print(f"导入Cookies时出错: {str(e)}")
            self.status_label.config(text="导入Cookies时出错")
            messagebox.showerror("错误", f"导入Cookies时出错: {str(e)}")
            
    def verify_cookies(self):
        """验证Cookies"""
        self.verify_button.config(state=tk.DISABLED)
        cookies = self.cookie_manager.load_cookies()
        
        if not cookies:
            self.status_label.config(text="未找到保存的Cookies")
            self.verify_button.config(state=tk.NORMAL)
            messagebox.showwarning("警告", "未找到保存的Cookies")
            return
            
        try:
            if self.cookie_manager.verify_cookies(cookies):
                self.status_label.config(text="Cookies有效")
                messagebox.showinfo("验证结果", "Cookies有效")
            else:
                self.status_label.config(text="Cookies已失效，请重新导入")
                messagebox.warning("验证结果", "Cookies已失效，请重新导入")
        except Exception as e:
            print(f"验证Cookies时出错: {str(e)}")
            self.status_label.config(text="验证Cookies时出错")
            messagebox.showerror("错误", f"验证Cookies时出错: {str(e)}")
        finally:
            self.verify_button.config(state=tk.NORMAL)
            
    def run(self):
        """运行GUI程序"""
        self.root.mainloop()

if __name__ == "__main__":
    app = DouYinCookieManager()
    app.run() 