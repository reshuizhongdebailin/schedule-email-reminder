"""
直接调用API获取课表并发送邮件
无需浏览器自动化，直接用requests库调用API
"""

import requests
import yagmail
import json
import os
from datetime import datetime

# 配置信息
API_URL = 'https://hubs.hust.edu.cn/schedule/getStudentScheduleByDate'
#这里是华科的课表API地址，直接调用这个接口就能获取课表数据

# 邮件配置
QQ_EMAIL = '自己邮箱@qq.com'
QQ_AUTH_CODE = '自己输入'

def load_cookies():
    """从文件加载Cookies"""
    cookies_file = 'cookies_auto.json'
    
    if not os.path.exists(cookies_file):
        print(f'✗ 未找到 {cookies_file} 文件')
        print('请先运行 extract_cookies.py 来提取Cookie')
        return None
    
    try:
        with open(cookies_file, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        print(f'✓ 已加载Cookies（{len(cookies)}个）')
        return cookies
    except Exception as e:
        print(f'✗ 加载Cookies失败：{e}')
        return None

def get_today_schedule(cookies):
    """获取今天的课表"""
    today_date = datetime.now()
    # Windows不支持 %-m 格式，需要手动处理
    today = f'{today_date.year}-{today_date.month}-{today_date.day}'
    
    params = {
        'DATE': today
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        print(f'正在获取 {today} 的课表...')
        response = requests.get(API_URL, params=params, cookies=cookies, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            data = response.json()
            print(f'✓ 获取成功，共 {len(data)} 节课')
            return data
        else:
            print(f'✗ 获取失败，状态码：{response.status_code}')
            return []
    except Exception as e:
        print(f'✗ 网络请求失败：{e}')
        return []

def generate_email_content(courses):
    """生成邮件内容"""
    today = datetime.now().strftime('%Y年%m月%d日')
    
    if not courses:
        return (
            f'📚 今天的课表 - {today}',
            '<h2>😊 今天没有课程安排。</h2>'
        )
    
    # 按开始时间排序
    courses.sort(key=lambda x: x.get('KSSJ', '00:00'))
    
    subject = f'📚 今天的课表 - {today}'
    
    html_content = f'''<html><body style="font-family: 微软雅黑, Arial; line-height: 1.8;">
    <h2>今天的课程安排（{today}）</h2>
    <table style="border-collapse: collapse; width: 100%;">
        <tr style="background-color: #f0f0f0;">
            <th style="border: 1px solid #ddd; padding: 10px;">节次</th>
            <th style="border: 1px solid #ddd; padding: 10px;">时间</th>
            <th style="border: 1px solid #ddd; padding: 10px;">课程名称</th>
            <th style="border: 1px solid #ddd; padding: 10px;">教室</th>
            <th style="border: 1px solid #ddd; padding: 10px;">教师</th>
        </tr>
    '''
    
    for course in courses:
        jc = course.get('JC', '-')
        time_str = f"{course.get('KSSJ', '-')}-{course.get('JSSJ', '-')}"
        course_name = course.get('KCMC', '-')
        classroom = course.get('JSMC', '-')
        teacher = course.get('JGXM', '-')
        
        html_content += f'''        <tr>
            <td style="border: 1px solid #ddd; padding: 10px;">{jc}</td>
            <td style="border: 1px solid #ddd; padding: 10px;">{time_str}</td>
            <td style="border: 1px solid #ddd; padding: 10px;">{course_name}</td>
            <td style="border: 1px solid #ddd; padding: 10px;">{classroom}</td>
            <td style="border: 1px solid #ddd; padding: 10px;">{teacher}</td>
        </tr>
    '''
    
    html_content += '''    </table>
    <p style="margin-top: 20px; color: #999; font-size: 12px;">
        自动生成的课表提醒 | 本邮件由Python脚本自动发送
    </p>
    </body></html>'''
    
    return subject, html_content

def send_email(subject, html_content):
    """发送邮件"""
    try:
        print(f'正在发送邮件到 {QQ_EMAIL}...')
        yag = yagmail.SMTP(QQ_EMAIL, QQ_AUTH_CODE, host='smtp.qq.com')
        yag.send(to=QQ_EMAIL, subject=subject, contents=html_content)
        print(f'✓ 邮件发送成功！')
        return True
    except Exception as e:
        print(f'✗ 邮件发送失败：{e}')
        return False

def main():
    """主函数"""
    print('='*50)
    print('课表提醒系统 - 直接API调用模式')
    print('='*50)
    
    # 加载cookies
    cookies = load_cookies()
    if not cookies:
        return
    
    print()
    
    # 获取课表
    courses = get_today_schedule(cookies)
    
    if courses or True:  # 即使没有课也要发邮件
        # 生成邮件
        subject, content = generate_email_content(courses)
        
        # 发送邮件
        send_email(subject, content)
    
    print('='*50)
    print('操作完成！')
    print('='*50)

if __name__ == '__main__':
    main()
