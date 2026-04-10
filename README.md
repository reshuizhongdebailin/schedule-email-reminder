# 课表邮件提醒系统

自动爬取学校课表，每天发送课表提醒邮件。

## 功能特点

- ✓ 直接调用API，不被WAF拦截
- ✓ 每天自动运行，发送课表邮件
- ✓ 支持Windows任务计划程序定时执行
- ✓ 邮件包含课程名称、时间、教室、教师信息

## 项目结构

```
.
├── extract_cookies.py          # 第一步：提取浏览器Cookie
├── fetch_schedule_api.py       # 第二步：获取课表并发送邮件
├── run_schedule.bat            # Windows批处理文件
├── requirements.txt            # Python依赖
├── cookies_auto.json          # 存储用户Cookie（自动生成，不上传）
└── README.md                   # 本文件
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 提取Cookie

```bash
python extract_cookies.py
```

按照提示从浏览器F12中复制Cookie，脚本会自动保存到 `cookies_auto.json`。

### 3. 测试运行

```bash
python fetch_schedule_api.py
```

检查你的QQ邮箱是否收到课表邮件。

### 4. 设置自动运行（可选）

**Windows用户：**
1. 打开任务计划程序（Win + R → taskschd.msc）
2. 创建基本任务 → 触发器选择每天 → 操作选择运行程序
3. 选择 `run_schedule.bat` 文件
4. 设置时间，比如每天上午8点

## 配置说明

### `extract_cookies.py`

- 从浏览器Network中复制Cookie
- 自动解析并保存到 `cookies_auto.json`
- **一次性操作**（Cookie有效期内）

### `fetch_schedule_api.py`

核心配置项（在文件头部修改）：

```python
API_URL = 'https://hubs.hust.edu.cn/schedule/getStudentScheduleByDate'
#这里是华科的
QQ_EMAIL = '你的QQ邮箱@qq.com'
QQ_AUTH_CODE = '你的邮箱授权码'
```

**获取QQ邮箱授权码：**
1. 登录QQ邮箱
2. 设置 → 账户
3. 开启"POP3/SMTP服务"
4. 复制生成的授权码

## 使用流程

```
第一次：
  extract_cookies.py（提取Cookie）
    ↓
  fetch_schedule_api.py（手动测试）
    ↓
  run_schedule.bat（Windows任务计划程序定时运行）

后续每天：
  定时自动运行 fetch_schedule_api.py
    ↓
  发送课表邮件到你的邮箱
```

## 常见问题

**Q: Cookie过期了怎么办？**
- A: 重新运行 `extract_cookies.py` 提取新Cookie

**Q: 邮件没有发出？**
- A: 检查QQ邮箱授权码是否正确，检查网络连接

**Q: 想改变运行时间？**
- A: 在Windows任务计划程序中编辑任务的触发器

## 技术细节

- **语言：** Python 3.x
- **核心库：** requests, yagmail
- **API调用：** 直接HTTP请求，无需浏览器自动化
- **邮件格式：** HTML表格
- **定时方案：** Windows任务计划程序

## 免责声明

本项目仅供个人学习和使用，不得用于非法用途。请遵守学校信息系统使用规范。

## 作者

Created: 2026-04-10

## License

MIT License
fb36926 (Initial commit: Schedule email reminder system)