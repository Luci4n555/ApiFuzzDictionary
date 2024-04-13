# -*- coding: utf-8 -*-
# @Author      :  Luci4n
# @File        :  handler_api_log.py
# @Version     :  1.0
# @Time        :  2024/04/12 20:06:20
# @Description :  处理爬取github api的日志文件，提取出所有的api，保存到github_api.txt文件中
import re

all_api_list = []

with open('./crawl_github_api_log.txt', 'r', encoding="utf-8") as f:
    for string in f.readlines():
        match = re.search(r'\[!\]爬取到API: (\[.*\])', string)
        if match:
            api_list_str = match.group(1)
            api_list = eval(api_list_str)
            all_api_list += [api.replace('\\\'', "").replace('\'', "").replace('"', "") for api in api_list]
 
all_api_list = sorted(list(set(all_api_list)))

with open('./github_api.txt', 'w', encoding="utf-8") as f:
    for api in all_api_list:
        f.write(api + '\n')

print('Done!')