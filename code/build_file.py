# -*- coding: utf-8 -*-
"""

"""
import pymysql

import xml.etree.ElementTree as ET
import configparser
from datetime import timedelta, date





def crawl_news(doc_dir_path, doc_encoding):
    # 打开数据库连接
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='123',
                         database='db_baike')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT item,title,description,tags FROM baike_docs")
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()
    # 关闭数据库连接
    db.close()

    delta = timedelta(days=-5)
    end_date = date.today()
    start_date = str(end_date + delta)
    i=1
    for news in data:
        try:
            body =news[2]
            doc = ET.Element("doc")
            ET.SubElement(doc, "id").text = "%d" % (i)
            ET.SubElement(doc, "url").text = news[3]
            if len(news[1])>0:
                ET.SubElement(doc, "title").text = news[0]
            elif len(news[0])>0:
                ET.SubElement(doc, "title").text = news[1]
            else:
                print('no title')
                continue

            ET.SubElement(doc, "datetime").text = start_date
            ET.SubElement(doc, "body").text = body
            tree = ET.ElementTree(doc)
            tree.write(doc_dir_path + "%d.xml" % (i), encoding=doc_encoding, xml_declaration=True)
            i += 1
        except:
            print('raise error')





if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('../config.ini', 'utf-8')


    crawl_news(config['DEFAULT']['doc_dir_path'], config['DEFAULT']['doc_encoding'])
    print('done!')