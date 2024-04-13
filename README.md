# ApiFuzzDictionary
红队Api接口Fuzz字典，WEB安全，渗透测试，API，字典
## 爬虫工具说明
Github爬取Api工具\github_crawl_api.py为爬虫文件，原理是通过github搜索引擎搜索项目的代码，根据API路径的规则进行匹配，最后将爬取到的所有API去重排序并保存到github_api.txt文件中，当做字典使用，需要Github Cookie才能使用且不稳定，一个号一天大概可发送1700条数据，本人断断续续挂服务器爬了几天才弄出来，最后整理出API字典
## API字典说明
目录下的API字典.txt是经过筛选文件夹下的github_api.txt后得到的，涉及比较敏感的接口，如/api/user、/api/sys、/api/admin、/api/upload等
## 使用说明
建议配合Burp Suite攻击器使用，加上常见的参数配合GET方法、POST方法进行fuzz
