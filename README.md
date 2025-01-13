# 抖音Cookies管理工具

这是一个简单易用的抖音Cookies管理工具，可以帮助用户导入和管理抖音网页版的登录凭证，并支持解析抖音分享链接获取视频ID。

## 功能特点

- 📋 支持直接粘贴Cookies
- 🔄 自动转换Cookies格式
- 💾 自动保存Cookies
- ✅ 验证Cookies有效性
- 📎 一键复制有效Cookies
- 🔍 解析抖音分享链接
- 📝 自动提取视频ID
- 📋 一键复制视频ID
- 🔒 安全的本地存储

## 使用方法

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 准备工作：
- 使用Chrome浏览器访问抖音网页版
- 在Chrome商店安装 "Cookie Editor" 扩展
- 登录抖音网页版

3. 获取Cookies：
- 登录成功后，点击Cookie Editor扩展图标
- 点击 "Export" -> "Export as JSON"
- 全选并复制导出的JSON内容

4. 运行程序：
```bash
python main.py
```

5. 导入Cookies：
- 将复制的JSON内容粘贴到文本框中
- 点击 "导入Cookies" 按钮
- 等待导入完成

6. 验证和使用Cookies：
- 点击 "验证Cookies" 按钮检查有效性
- 点击 "复制Cookies" 按钮获取格式化的Cookies字符串
- 复制的Cookies可直接用于浏览器或其他工具

7. 解析视频链接：
- 从抖音APP或网页版获取视频分享链接
- 将分享链接粘贴到输入框中
- 点击 "解析链接" 按钮
- 自动提取并显示视频ID
- 点击 "复制ID" 按钮获取视频ID

## 项目结构

- `main.py`: 主程序入口
- `utils/`: 工具函数目录
  - `cookie_manager.py`: Cookie管理模块
- `data/`: 数据存储目录

## 技术架构

- 使用`tkinter`提供图形界面
- 使用`requests`库处理HTTP请求
- 使用`json`处理Cookie数据
- 使用`re`模块解析分享链接

## 注意事项

- 请勿将cookies分享给他人
- 建议定期更新cookies
- 遵守抖音平台的使用规范 