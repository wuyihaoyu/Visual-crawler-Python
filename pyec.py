from collections import Counter
#
# from bs4 import BeautifulSoup
from pyecharts.charts import Bar, WordCloud, Pie, Page, Grid, Scatter
import re
import jieba.posseg as pseg
from pyecharts import options as opts
from pyecharts.charts import Funnel
import pandas as pd


def remove_markers(str_list):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    return [pattern.sub('', line) for line in str_list]


def run():
    # 读取数据
    csv_file = './bangdan.csv'  # 导入csv数据
    data = pd.read_csv(csv_file)

    datas = data['类型'].value_counts()
    te = pd.DataFrame(data=datas)
    te.to_csv('leixing.csv')

    datazt = data['状态'].value_counts()
    t = pd.DataFrame(data=datazt)
    t.to_csv('zhuangtai.csv')

    dataci = data['小说名称']
    # print(dataci)
    word_list = list(dataci)
    word_list = remove_markers(word_list)
    # print(word_list)

    datazzzs = data[['作者', '字数万字']]
    # datazzzs=datazzzs.groupby('作者').apply(lambda x:x['字数(万字)'].sum())
    datazzzs = datazzzs.groupby('作者').agg({'字数万字': 'sum'}).sort_values(by='字数万字', ascending=False)
    testpm = pd.DataFrame(data=datazzzs)
    testpm.to_csv('zzzs.csv')
    csvpm_file = './zzzs.csv'  # 导入csv数据
    datazzpm = pd.read_csv(csvpm_file)
    datazzpm = datazzpm.head(10)
    # print(datazzpm)

    words_list = []
    for line in word_list:
        words_list.extend(word for word, flag in pseg.cut(line, use_paddle=True) if flag in ['a', 'vd', 'n'])
    c1 = Counter(words_list)
    # print(c1)

    a = (
        Bar(init_opts=opts.InitOpts(height="450px", width="900px"))
            .add_xaxis(list(datas.index))
            .add_yaxis("类型", list(datas))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="热门小说类型统计"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
    )
    b = (
        WordCloud(init_opts=opts.InitOpts(height="450px", width="900px"))
            .add(series_name="热点分析", data_pair=c1.most_common(), word_size_range=[22, 66])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    c = (
        Pie(init_opts=opts.InitOpts(height="450px", width="600px"))
            .add(
            "",
            [list(z) for z in zip(datazt.index, list(datazt))],
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="小说状态"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )

    d = (
        Funnel(init_opts=opts.InitOpts(height="450px", width="600px"))
            .add(
            "作者",
            [list(z) for z in zip(list(datazzpm['作者']), datazzpm.index + 1)],
            sort_="ascending",
            label_opts=opts.LabelOpts(position="inside"),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="作者字数天梯榜（Top10）"),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    e = (
        Scatter(init_opts=opts.InitOpts(height="450px", width="600px"))
            .add_xaxis(
            xaxis_data=data['排名'])
            .add_yaxis(
            series_name="字数万字",
            y_axis=data['字数万字'],
            symbol_size=15,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_series_opts()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="字数-排名分析"),
            xaxis_opts=opts.AxisOpts(
                type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
        )
    )
    page = (
        Page(page_title="热门小说分析", layout=Page.SimplePageLayout)
            .add(a)
            .add(b)
            .add(c)
            .add(d)
            .add(e)
            .render("热门小说分析.html")
    )


try:
    with open("热门小说分析.html", "r+", encoding='utf-8') as html:
        html_bf = BeautifulSoup(html, 'lxml')
        divs = html_bf.select('.chart-container')
        divs[0][
            "style"] = "width:500px;height:250px;position:absolute;top:5px;left:0px;border-style:solid;border-color:#000000;border-width:0px;"
        divs[1][
            'style'] = "width:500px;height:400px;position:absolute;top:5px;left:505px;border-style:solid;border-color:#000000;border-width:0px;"
        divs[2][
            "style"] = "width:500px;height:400px;position:absolute;top:255x;left:0px;border-style:solid;border-color:#000000;border-width:0px;"
        divs[3][
            "style"] = "width:500px;height:400px;position:absolute;top:255px;left:505px;border-style:solid;border-color:#000000;border-width:0px;"
        body = html_bf.find("body")
        body["style"] = "background-color:#333333;"
        html_new = str(html_bf)
        html.seek(0, 0)
        html.truncate()
        html.write(html_new)
        html.close()
except:
    print("正常执行程序，有问题请打开pyec.py结尾")

if __name__ == '__main__':
    ui = run()
