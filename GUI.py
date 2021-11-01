import webbrowser
from threading import Thread
from tkinter import *
from tkinter import ttk
import tkinter as tk
import wx

import sql
import datetime

from getList import getList
from pyec import run


def thread_it(func, *args):
    '''
    将函数打包进线程
    '''
    # 创建
    # strtimer1=func()
    t = Thread(target=func, args=args)
    # 守护
    t.setDaemon(True)
    # 启动
    t.start()


class uiob:

    def clear_tree(self, tree):
        '''
        清空表格
        '''
        x = tree.get_children()
        for item in x:
            tree.delete(item)

    def add_tree(self, list, tree):
        '''
        新增数据到表格
        '''
        i = 0
        for subList in list:
            tree.insert('', 'end', values=subList)
            i = i + 1
        tree.grid()

    def searh(self):

        self.clear_tree(self.treeview)  # 清空表格
        self.B_0['text'] = '正在努力搜索'

        starttime = datetime.datetime.now() # 起始时间

        getob = getList()
        lists = getob.input()

        endtime = datetime.datetime.now()  # 结束时间
        Clientlog = open('spider_log.txt', 'ba+')
        Clientlog.write(str("\t*****爬虫日志*****\t\n").encode('utf-8'))
        Clientlog.write(str("[开始时间]" + str(starttime.strftime('%Y/%m/%d %H:%M:%S')) + '\n').encode('utf-8'))
        Clientlog.write(str("[结束时间]" + str(endtime.strftime('%Y/%m/%d %H:%M:%S')) + '\n').encode('utf-8'))
        Clientlog.write(str("[线程数]" + str(1) + '\n').encode('utf-8'))
        Clientlog.write(str("[爬取数据量]" + str(len(lists)) + '\n').encode('utf-8'))
        Clientlog.write(str("[总耗时]" + str((endtime - starttime).microseconds/1000) + 'ms\n').encode('utf-8'))
        strtime = '耗时'+str((endtime - starttime).microseconds/1000) + 'ms '+'抓取'+str(len(lists))+'条数据'
        print(strtime)
        self.add_tree(lists, self.treeview)  # 将数据添加到tree中
        wx.MessageBox(strtime,caption="抓取成功")

        self.B_0['state'] = NORMAL
        self.B_0['text'] = '更新榜单'
        sql.runsql()
        run()
        # return strtime

    def center_window(self, root, w, h):
        """
        窗口居于屏幕中央
        :param root: root
        :param w: 窗口宽度
        :param h: 窗口高度
        :return:
        """
        # 获取屏幕 宽、高
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()

        # 计算 x, y 位置
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def click(self):
        webbrowser.open(
            "http://localhost:63342/wuyi-master/%E7%83%AD%E9%97%A8%E5%B0%8F%E8%AF%B4%E5%88%86%E6%9E%90.html")

    # http://localhost:63342/duoduo/%E7%83%AD%E9%97%A8%E5%B0%8F%E8%AF%B4%E5%88%86%E6%9E%90.html
    def ui_process(self):
        root = Tk()
        self.root = root

        root.title("图书信息爬取")
        self.center_window(root, 900, 350)
        root.resizable(0, 0)
        root['highlightcolor'] = 'yellow'

        labelframe = LabelFrame(root, width=900, height=350, background="white")
        labelframe.place(x=5, y=5)
        self.labelframe = labelframe
        # 图片
        photo = tk.PhotoImage(file="duoduo.png")
        Lab = tk.Label(root, image=photo, )
        Lab.place(x=10, y=10)





        B_1 = Button(labelframe, text="数据分析", background="white")
        B_1.place(x=500, y=25, width=150, height=50)
        self.B_1 = B_1
        B_1.configure(command=lambda: thread_it(self.click()))  # 按钮绑定单击事件
        # 查询按钮
        B_0 = Button(labelframe, text="更新榜单", background="white")
        B_0.place(x=700, y=25, width=150, height=50)
        self.B_0 = B_0
        B_0.configure(command=lambda: thread_it(self.searh))  # 按钮绑定单击事件
        # 框架布局，承载多个控件
        frame_root = Frame(labelframe)
        frame_l = Frame(frame_root)
        frame_r = Frame(frame_root)
        self.frame_root = frame_root
        self.frame_l = frame_l
        self.frame_r = frame_r

        # 表格
        columns = ("序号", "类型", "小说名称", "更新章节", "状态", "字数(万字)", "作者", "更新时间")
        treeview = ttk.Treeview(frame_l, height=10, show="headings", columns=columns)
        treeview.column("序号", width=50, anchor='center')
        treeview.column("类型", width=50, anchor='center')
        treeview.column("小说名称", width=200, anchor='center')
        treeview.column("更新章节", width=200, anchor='center')
        treeview.column("状态", width=50, anchor='center')
        treeview.column("字数(万字)", width=75, anchor='center')
        treeview.column("作者", width=75, anchor='center')
        treeview.column("更新时间", width=150, anchor='center')

        treeview.heading("序号", text="序号")  # 显示表头
        treeview.heading("类型", text="类型")
        treeview.heading("小说名称", text="小说名称")
        treeview.heading("更新章节", text="更新章节")
        treeview.heading("状态", text="状态")
        treeview.heading("字数(万字)", text="字数(万字)")
        treeview.heading("作者", text="作者")
        treeview.heading("更新时间", text="更新时间")

        # 垂直滚动条
        vbar = ttk.Scrollbar(frame_r, command=treeview.yview)
        treeview.configure(yscrollcommand=vbar.set)

        treeview.pack()
        self.treeview = treeview
        vbar.pack(side=RIGHT, fill=Y)
        self.vbar = vbar

        # 框架的位置布局
        frame_l.grid(row=0, column=0, sticky=NSEW)
        frame_r.grid(row=0, column=1, sticky=NS)
        frame_root.place(x=10, y=100)

        root.mainloop()
