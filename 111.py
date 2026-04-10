from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from bs4 import BeautifulSoup
import yagmail
import time
import os
from datetime import datetime

# 配置信息
USERNAME = os.getenv('HUST_USERNAME', '').strip()  # 你的学号
PASSWORD = os.getenv('HUST_PASSWORD', '').strip()  # 你的密码
LOGIN_URL = 'https://hubs.hust.edu.cn/auth/login'  # 登录页URL
SCHEDULE_URL = 'https://hubs.hust.edu.cn/basicInformation/scheduleInformation/index'  # 课表页URL

# 邮件配置
QQ_EMAIL = os.getenv('QQ_EMAIL', '').strip()  # 请通过环境变量配置
QQ_AUTH_CODE = os.getenv('QQ_AUTH_CODE', '').strip()  # 请通过环境变量配置


def validate_required_config():
    missing = []
    if not USERNAME:
        missing.append('HUST_USERNAME')
    if not PASSWORD:
        missing.append('HUST_PASSWORD')
    if not QQ_EMAIL:
        missing.append('QQ_EMAIL')
    if not QQ_AUTH_CODE:
        missing.append('QQ_AUTH_CODE')
    if missing:
        print('缺少环境变量：' + ', '.join(missing))
        print('请先配置后再运行脚本。')
        return False
    return True


if not validate_required_config():
    exit()

# 启动浏览器
try:
    service = Service('chromedriver.exe')
    options = webdriver.ChromeOptions()
    
    # 添加反爬虫措施
    options.add_argument('--disable-blink-features=AutomationControlled')  # 隐藏自动化特征
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(service=service, options=options)
    print('浏览器已启动（已启用反爬虫措施）')
    
    # 添加随机延迟
    time.sleep(2)
    driver.get(LOGIN_URL)
    print(f'已访问登录页：{LOGIN_URL}')
except Exception as e:
    print(f'启动浏览器失败：{e}')
    exit()

# 输入账号
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )
    driver.find_element(By.NAME, 'username').send_keys(USERNAME)
    print('账号已输入')
except Exception as e:
    print(f'输入账号失败：{e}')
    # 保存页面源代码用于调试
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print('页面源代码已保存到 page_source.html')
    driver.quit()
    exit()

# 输入密码
try:
    driver.find_element(By.NAME, 'password').send_keys(PASSWORD)
    print('密码已输入')
except Exception as e:
    print(f'输入密码失败：{e}')
    driver.quit()
    exit()

# 截图验证码
try:
    captcha_element = driver.find_element(By.CSS_SELECTOR, 'img[alt="验证码"]')
    captcha_element.screenshot('captcha.png')
    print('验证码已截图')
except Exception as e:
    print(f'验证码截图失败：{e}')
    # 保存整个页面截图
    driver.save_screenshot('page_screenshot.png')
    print('页面截图已保存到 page_screenshot.png')
    driver.quit()
    exit()

print('请查看当前目录下的 captcha.png，输入验证码：')
captcha_code = input('验证码：')

# 输入验证码
try:
    driver.find_element(By.NAME, 'captcha').send_keys(captcha_code)
    print('验证码已输入')
except Exception as e:
    print(f'输入验证码失败：{e}')
    driver.quit()
    exit()

# 提交登录表单
try:
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    print('登录表单已提交')
except Exception as e:
    print(f'提交登录失败：{e}')
    driver.quit()
    exit()
# 等待跳转到课表页面
time.sleep(3)
driver.get(SCHEDULE_URL)

# 获取页面源代码
time.sleep(2)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# 解析课表数据
# 这里需要根据实际页面结构调整选择器
today = datetime.now().strftime('%Y-%m-%d')
courses = []

# TODO: 根据实际页面HTML结构，提取今天的课程信息
# 示例：查找所有课程元素
course_elements = soup.find_all(class_='course-item')
for course in course_elements:
    course_info = course.get_text(strip=True)
    courses.append(course_info)

# 生成邮件内容
email_subject = f'今天的课表 - {today}'
if courses:
    email_body = f'<h3>今天的课程安排（{today}）：</h3>\n<ul>\n'
    for course in courses:
        email_body += f'<li>{course}</li>\n'
    email_body += '</ul>\n'
else:
    email_body = f'<h3>今天没有课程安排。</h3>\n'

# 发送邮件
try:
    yag = yagmail.SMTP(QQ_EMAIL, QQ_AUTH_CODE, host='smtp.qq.com')
    yag.send(to=QQ_EMAIL, subject=email_subject, contents=email_body)
    print(f'邮件已发送到 {QQ_EMAIL}')
except Exception as e:
    print(f'邮件发送失败：{e}')

# 关闭浏览器
driver.quit()