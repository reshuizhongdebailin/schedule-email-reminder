"""
交互式Cookie提取工具
从浏览器F12中复制Cookie，这个脚本会自动解析并保存
"""

import json

def extract_cookies_from_string(cookie_string):
    """从 'name=value; name2=value2' 格式解析Cookie"""
    cookies = {}
    pairs = cookie_string.split('; ')
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            cookies[key.strip()] = value.strip()
    return cookies

def main():
    print('='*60)
    print('🍪 Cookie提取工具')
    print('='*60)
    print()
    print('步骤：')
    print('1. 打开浏览器，登录课表系统')
    print('2. 按F12打开开发者工具 → Network标签')
    print('3. 找任意一个请求（如 getStudentScheduleByDate）')
    print('4. 在右侧 Request Headers 中找到 Cookie: 行')
    print('5. 复制 Cookie: 后面的所有内容（到行末）')
    print('6. 粘贴到下面的输入框')
    print()
    print('-'*60)
    
    cookie_input = input('请粘贴你复制的Cookie字符串：\n> ').strip()
    
    if not cookie_input:
        print('✗ Cookie为空，已取消')
        return
    
    # 解析Cookie
    cookies = extract_cookies_from_string(cookie_input)
    
    if not cookies:
        print('✗ 无法解析Cookie，请检查格式')
        return
    
    print()
    print('✓ Cookie解析成功！共', len(cookies), '个Cookie：')
    print()
    for key, value in cookies.items():
        # 只显示开头和结尾，中间用...代替（隐私保护）
        if len(value) > 20:
            display_value = value[:10] + '...' + value[-5:]
        else:
            display_value = value
        print(f'  • {key}: {display_value}')
    
    print()
    # 保存到文件
    cookies_file = 'cookies_auto.json'
    with open(cookies_file, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    
    print(f'✓ Cookies已保存到 {cookies_file}')
    print()
    print('='*60)
    print('下一步：运行 fetch_schedule_api.py 自动获取课表和发送邮件')
    print('='*60)

if __name__ == '__main__':
    main()
