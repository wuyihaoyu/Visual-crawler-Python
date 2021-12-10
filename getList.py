import re
import pymysql

import pandas as pd
import requests
from lxml import etree
from dask.bytes.tests.test_http import requests


class getList:
    def input(self, listcv):
        ###网址

        print('============这里是生成数据树=============')

        y1 = ['no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no',
              'no',
              'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no',
              'no',
              'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no',
              'no',
              'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no',
              'no',
              'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no',
              'no',
              'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no']

        y2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        print('这里是url判断。')

        if int(listcv[8]) == 9:
            # 新书榜https://xs.sogou.com/top/new/
            print('9')
            url = "https://xs.sogou.com/top/new/"
        elif int(listcv[8]) == 10:
            # 畅销榜
            print('10')
            url = "https://xs.sogou.com/top/bestseller/"

        elif int(listcv[8]) == 11:
            # 男生版
            print('11')
            url = "https://xs.sogou.com/top/boy/"
        else:
            # 女生版
            print('12')
            url = "https://xs.sogou.com/top/girl/"

        ###模拟浏览器
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

        html = etree.HTML(requests.get(url, headers=header).text)

        rank = html.xpath('//ul[@class="list-content list-0"]//span[@class="text-num icon"]/text()')  # 序号
        if int(listcv[1]):
            type = html.xpath('//ul[@class="list-content list-0"]//a[@class="list-type"]/text()')  # 类型
        else:
            type = y1
        name = html.xpath('//ul[@class="list-content list-0"]//a[@class="list-name"]/text()')  # 小说名称

        if int(listcv[3]):
            section = html.xpath('//ul[@class="list-content list-0"]//a[@class="list-section"]/text()')  # 更新章节
        else:
            section = y1
        if int(listcv[4]):
            status = html.xpath('//ul[@class="list-content list-0"]//span[@class="list-status"]/text()')  # 状态
        else:
            status = y1

        if int(listcv[5]):
            count = html.xpath('//ul[@class="list-content list-0"]//span[@class="list-count"]/text()')  # 字数
        else:
            count = y1

        if int(listcv[6]):
            author = html.xpath('//ul[@class="list-content list-0"]//span[@class="list-author"]/text()')  # 作者
        else:
            author = y1
        if int(listcv[7]):
            time = html.xpath('//ul[@class="list-content list-0"]//span[@class="list-time"]/text()')  # 更新时间
        else:
            time = y1

        list = []
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
        numlist = 100
        lists = list[0:numlist]
        name = ['排名', '类型', '小说名称', '更新章节', '状态', '字数万字', '作者', '更新时间']
        test = pd.DataFrame(columns=name, data=lists)
        # 数据源是list
        print(test)
        test.to_csv('bangdan.csv')
        return lists
