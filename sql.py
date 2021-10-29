import pymysql
import pandas as pd


def runsql():
    file_path = "bangdan.csv"
    table_name = "student"
    try:
        con = pymysql.connect(host="localhost", user="root", password="123456", database="mesql")
        con.set_charset('utf8')
        cur = con.cursor()
        cur.execute("set names utf8")
        cur.execute("SET character_set_connection=utf8;")

        with open(file_path, 'r', encoding='utf8') as f:
            reader = f.readline()
            # print(1)
            str_name = '序号'
            reader = str_name + reader
            # print(reader)
            devide = reader.split(',')  # 做成列表
            devide[-1] = devide[-1].rstrip('\n')  # 去除最后的换行符
            # print(2)
            # print(devide)

        column = ''
        for dd in devide:
            # 如果标题过长，只能存成text格式
            if dd == "标题":
                column = column + dd + ' TEXT,'
            else:
                column = column + dd + ' varchar(255),'
        col = column.rstrip(',')  # 去除最后一个多余的，
        # print(2.1)
        # print(col)
        create_table_sql = '''create table if not exists {} ({}) DEFAULT CHARSET=utf8'''.format(table_name, col)
        # print(create_table_sql)
        # sqls = '''
        #          INSERT INTO student(序号,排名,类型,小说名称,更新章节,状态,字数万字,作者,更新时间) values(%s,
        #          %s,%s,%s,%s,%s,%s,%s,%s)
        #      '''
        cur.execute(create_table_sql)
        print("成功创建表")
        df = pd.read_csv('bangdan.csv')
        counts = 0
        # print(999999999999)
        for each in df.values:
            # print(each)
            # 每一条数据都应该单独添加，所以每次添加的时候都要重置一遍sql语句
            sql = 'insert into ' + table_name + ' values('
            # 因为每条数据都是一个列表，所以使用for循环遍历一下依次添加
            for i, n in enumerate(each):
                # 这个时候需要注意的是前面的数据可以直接前后加引号，最后加逗号，但是最后一条的时候不能添加逗号。
                # 所以使用if判断一下
                # print(i)
                # print(n)
                if i < (len(each) - 1):
                    # 因为其中几条数据为数值型，所以不用添加双引号
                    if i <= 1 or i == 6 :
                        sql = sql + str(n) + ','
                    else:
                        sql = sql + '"' + str(n) + '"' + ','
                else:
                    sql = sql + '"' + str(n) + '"'
            sql = sql + ');'
            # print(sql)
            # 当添加当前一条数据sql语句完成以后，需要执行并且提交一次
            cur.execute(sql)
            # 提交sql语句执行操作
            con.commit()
            # 没提交一次就计数一次
            counts += 1
            # 使用一个输出来提示一下当前存到第几条了
        print('--------------------------------------------------------- ')
        print('-----------成功添加了' + str(counts) + '条数据----------------------------- ')
        print('--------------------------------------------------------- ')
        con.commit()
        print("数据存取成功")
    except Exception as e:
        print("创建数据库失败：case%s" % e)
        con.rollback()
    finally:
        print("已关闭数据库")
        cur.close()
        con.close()
