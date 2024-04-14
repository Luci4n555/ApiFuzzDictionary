# -*- coding: utf-8 -*-
# @Author      :  Luci4n
# @File        :  github_crawl_api.py
# @Version     :  1.0
# @Time        :  2024/04/10 15:17:18
# @Description :  通过github搜索引擎爬取项目的API，并保存到github_api.txt文件中，当做字典使用
import requests, re, time, string, datetime, codecs
from urllib.parse import quote, unquote
from html import unescape


# 获取api规则，根据字典匹配的api规则，这里匹配v0-v5和api、apis开头的api规则
def get_apis():
    apis = []
    letters = string.ascii_lowercase + '0123456' + '_'  # 所有小写字母、数字、下划线
    my_dic = ['get','set','use','admi','que','manage','sy','fil','uploa','rol','grou','downloa']  # 定义组合的api规则
    letters = my_dic + list(letters)  # 所有小写字母、数字、下划线和定义组合的api规则
    # apis = ['/[\'"]\/api\/[^\'"\/]+[\'"]/','/[\'"]\/api\/[^\'"\/]+\/[^\'"\/]+[\'"]/','/[\'"]\/api\/[^\'"\/]+\/[^\'"\/]+\/[^\'"\/]+[\'"]/','/[\'"]\/api\/[^\'"\/]+\/[^\'"\/]+\/[^\'"\/]+\/[^\'"]*[\'"]/']
    # apis = ['/[\'"]\/api\/[^\'"\/]+[\'"]/','/[\'"]\/api\/[^\'"\/]+\/[^\'"]*[\'"]/']
    for letter in letters:
        apis.append(f'/[\'"]\/api\/{letter}[^\'"\/]+[\'"]/')
        apis.append(f'/[\'"]\/api\/{letter}[^\'"\/]+\/[^\'"]*[\'"]/')
    for dic in my_dic + [""]:
        apis.append(f'/[\'"]\/apis\/{dic}[^\'"\/]+[\'"]/')
        apis.append(f'/[\'"]\/apis\/{dic}[^\'"\/]+\/[^\'"]*[\'"]/')
    for v in range(7):
        apis.append(f'/[\'"]\/api\/v{v}[^\'"\/]+[\'"]/')
        apis.append(f'/[\'"]\/api\/v{v}[^\'"\/]+\/[^\'"]*[\'"]/')
    for v in range(6):
        apis.append(f'/[\'"]\/v{v}\/[^\'"\/]+[\'"]/')
        apis.append(f'/[\'"]\/v{v}\/[^\'"\/]+\/[^\'"]*[\'"]/')
    return [quote(api) for api in apis]

# 获取路径规则，突破页数5限制，爬取更多的api
def get_paths():
    letters = string.ascii_lowercase + '_'
    letters = letters.replace('a', '').replace('u', '').replace('m', '').replace('s', '')
    paths = [quote(f'/.*\/[{letters[i:i+6]}][^\/]*$/') for i in range(0, len(letters), 6)]  # 正则匹配文件名开头[bcdefg]、[hijkln]等
    paths = paths + [quote(f'/.*\/{letter}[^\/]*$/') for letter in 'aums']  # 正则匹配文件名开头是a、u、m、s的路径，这些是重点路径，文件比较多
    return paths

# 获取语言规则
def get_languages():
    # languages = ['java', 'python', 'rust', 'go', 'javascript', 'html', 'php']
    languages = ['java']  # 只爬取java语言的api
    return languages

# 将爬取url信息写入日志文件，并打印到控制台
def write_log(msg):
    # print(msg)
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{formatted_time}] {msg}"
    with open("crawl_github_api_log.txt", "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")

# 规则匹配
def get_api(pattern, text):
    text = unescape(codecs.decode(unquote(text), 'raw_unicode_escape'))
    pattern = unquote(pattern)[1:-1]
    match = re.findall(pattern, text)
    return match

# 主函数
def main():
    sleep_time = 3.5  # 爬取间隔时间
    all_api = []  # 将爬取到的所有api保存到all_api中
    apis = get_apis()  # 获取api规则
    paths = get_paths()  # 获取路径规则
    languages = get_languages()  # 获取语言规则
    pages = 5  # 爬取页数，最多到5页
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54",
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Referer": "https://github.com/search",
        "X-GitHub-Target": "dotcom",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive"
    }  # 请求头设置
    # Cookie设置，这里需要登录github账号，然后将Cookie复制到这里
    headers["Cookie"] = "_gh_sess=uH%2BUDQVNFP5cymBDRVLI8ZpSJZY7EY7gmSl2diFoY68H3yWrq8Kc9%2Bx%2F2YEzNXyKLlZApqGEMSX4ZSfcFIEgyzMZkiRJAS3Uce7%2FO0RjjUR4nDnGQkf7r9SJjsVhgGMJvL0dRjJrn7HBPKTCqJeMuyZGbeFOMum3JEWLfQrX3Z1ARWALZFyYP6ME9VeV1T8KTvXv%2FnAUBhTtn%2FdZcFpvtVOh430%2BVTiqR1QjfDTuo8e31%2F%2B6pSPb3DiBP0avGZyFwXSGXdj%2BhoAyifTfpofJwWWrmhj%2FFUBmoA3DTyrAZZr1e21qKZxqt15VwNOH4OSpKZlnBB3Ww78GhqJSAhlfB75YL5XIaAn6MydqNGA5jBMx1ASZ1c%2BVQ3DLzfeJigUXT9GYmYG10uJjc5NdiDlNskuksBQSlDc35KZ2H6xwX%2F2v7J22Twb9Axlsb82C2c7PyRoy0e%2FA8I5%2BU%2FuhkELTXedF%2Flx7BH4KJ4ZwbSMQfaRnrzaume%2BwpcqTCwKRd5JTmiJHQZvagA5os8dHvtjHg6hX0hFF5knGDKdh%2FDMrcIX39Mb5w37HiWfd1aH3ID0K%2FA336eecUVjQ3rAyVZTye0%2Fh6A8%2F5JCx3etU%2FZIG8J%2FlMti0X3fW48NY9BXw82UC4UQOeorNI7TcaidvHQIWeIX9OBNEwdFAk8pXorMWYxiWGwBLsA3hMtvHVV5LYdmxZBCqYksDe2BNhwms7Aqa2CpnS203X86kz4NNFNWDnm7OhYi4K9PlKV0bMKpi%2BduJfwJ9wbChLiVWW4ZAZfnuVSakkMXd5Qv0Y39ULfrPcKO7bHG1q1AgYsm8OyQ%2Bc4upYsbnuwK9WMba%2FQzL69VsP3m8gS20Eml1gxvIWEjTL3bfOLsSlRrg%2Bf39s3JlLJDIDdT9Tgy7N1ff4S%2BE7Mt53I0FVkxRuyKmSmJSOgbLSxKTBXl%2Bn4iLxgT7JxQB1uPdlo7EP5wiO1D2e7Vsnj32sdqmwisXNcKDradYcr74g9waKUJo77iS6ZR0XYOOtM0vqxtqRg%3D%3D--9amtPnF9VK7Oge%2BX--SrqXR6UjC2sQ0y%2Bci2Ol0w%3D%3D; _octo=GH1.1.4311822.1712667910; logged_in=yes; preferred_color_mode=light; tz=Asia%2FShanghai; _device_id=a4efcbe58ce766a1e2c85082e01a83c7; has_recent_activity=1; saved_user_sessions=166487159%3A5g5PXr5gUAr9bpdRh9ffLBFN6AhThDJsRBywO39zw6btRZ_I; user_session=5g5PXr5gUAr9bpdRh9ffLBFN6AhThDJsRBywO39zw6btRZ_I; __Host-user_session_same_site=5g5PXr5gUAr9bpdRh9ffLBFN6AhThDJsRBywO39zw6btRZ_I; tz=Asia%2FShanghai; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D;"
    
    # 爬取api
    session = requests.Session()
    session.headers.update(headers)
    for api in apis:
        for path in paths:
            for language in languages:
                for page in range(1, pages + 1):
                    url = f"https://github.com/search?q={api}+path%3A{path}+language%3A{language}&type=code&p={page}"
                    msg = f"[+]正在爬取{url}"
                    write_log(msg)
                    time.sleep(sleep_time)
                    try:
                        response = session.get(url, timeout=12)
                        # print(response.text)
                        match = get_api(api, response.text)
                        # 如果没有匹配到api，则说明已经爬取完毕
                        if not match:
                            if "Search failed. Please try again" in response.text:
                                msg = f"[-]搜索失败，账号被拦截，请更换账号重试，爬取{url}失败！"
                                write_log(msg)
                                exit(0)
                            if "/signup?source=code_search_results" in response.text and '{"header_redesign_enabled":false,' in response.text :
                                msg = f"[-]登录账号的Cookie失效，爬取{url}失败！"
                                write_log(msg)
                                exit(0)
                            break
                        all_api += match
                        msg = f"[!]爬取到API: {match}"
                        write_log(msg)
                        # 如果返回结果不是100个，则说明已经爬取完毕
                        if '"result_count":100,' not in response.text:
                            break
                    except requests.exceptions.ConnectTimeout:
                        msg = f"[-]请求超时，爬取{url}失败！"
                        write_log(msg)
                        break
                    except:
                        exit(0)

    # 整理并输出api
    all_api = sorted(list(set(all_api)))
    with open("github_api.txt", "w", encoding="utf-8") as f:
        for api in all_api:
            f.write(api + "\n")
    msg = f"[+]API爬取完成，总共爬取到{len(all_api)}个API！"
    write_log(msg)

if __name__ == '__main__':
    main()
    
