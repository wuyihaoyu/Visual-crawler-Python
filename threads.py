import re

import pandas as pd
import requests
from lxml import etree
from dask.bytes.tests.test_http import requests

from concurrent.futures import ThreadPoolExecutor


class getList2:

    def getbiglist(self, list):
        numlist = 800
        lists = list[0:numlist]
        for i in range(1, 801):
            lists[i - 1][0] = i
        name = ['排名', '类型', '小说名称', '更新章节', '状态', '字数万字', '作者', '更新时间']
        test = pd.DataFrame(columns=name, data=lists)
        # 数据源是list
        print(test)
        test.to_csv('bangdan.csv')

    def threadEX(self):
        biglist = []
        arryurl = ["https://xs.sogou.com/top/new/",
                   "https://xs.sogou.com/top/bestseller/",
                   "https://xs.sogou.com/top/free/",
                   "https://xs.sogou.com/top/done/",
                   "https://xs.sogou.com/top/search/",
                   "https://xs.sogou.com/top/collect/",
                   "https://xs.sogou.com/top/boy/",
                   "https://xs.sogou.com/top/girl/"]
        with ThreadPoolExecutor(max_workers=4) as t:
            for j in arryurl:
                t.submit(self.input, j, biglist)
            print('\n')
        self.getbiglist(biglist)
        return biglist

    def input(self, info, blist):
        # 网址
        url = info
        print(url)

        # 模拟浏览器
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0'
                          '.3683.103 Safari/537.36'}

        html = etree.HTML(requests.get(url, headers=header).text)

        rank = html.xpath('//ul[@class="list-content list-0"]//span[@class="text-num icon"]/text()')  # 序号

        type = html.xpath('//ul[@class="list-content list-0"]//a[@class="list-type"]/text()')  # 类型

        name = html.xpath('//ul[@class="list-content list-0"]//a[@class="list-name"]/text()')  # 小说名称

        section = html.xpath('//ul[@class="list-content list-0"]//a[@class="list-section"]/text()')  # 更新章节

        status = html.xpath('//ul[@class="list-content list-0"]//span[@class="list-status"]/text()')  # 状态

        count = html.xpath('//ul[@class="list-content list-0"]//span[@class="list-count"]/text()')  # 字数

        author = html.xpath('//ul[@class="list-content list-0"]//span[@class="list-author"]/text()')  # 作者

        time = html.xpath('//ul[@class="list-content list-0"]//span[@class="list-time"]/text()')  # 更新时间

        list = blist
        for i in range(0, len(name)):
            subList = []
            subList.append(rank[i])

            subList.append(re.sub('「', '', re.sub('」', '', type[i])))
            subList.append(name[i])
            subList.append(section[i])

            subList.append(status[i])

            subList.append(re.sub(',', '', re.sub('万字', '', count[i])))

            subList.append(author[i])

            subList.append(time[i])

            list.append(subList)
        print(len(list))
        # print(list)
        print("**__提取完毕__**")
