# -*- coding: utf-8 -*-
__author__ = 'zxm'


from search_engine import SearchEngine

import xml.etree.ElementTree as ET
import configparser

config = configparser.ConfigParser()
config.read('../config.ini', 'utf-8')
dir_path = config['DEFAULT']['doc_dir_path']
db_path = config['DEFAULT']['db_path']

def search(keys):
    try:
        if keys not in ['']:
            flag,doc_id = searchidlist(keys)
            if flag==0:
                return 'no result'
            docs = find(doc_id)
            return docs
        else:
            return 'no search keys'
    except:
        return 'search error'

def searchidlist(key, selected=0):
    se = SearchEngine('../config.ini', 'utf-8')
    flag, id_scores = se.search(key, selected)
    # 返回docid列表
    doc_id = [i for i, s in id_scores]
    return flag,doc_id
# 将需要的数据以字典形式打包传递给search函数
def find(docids):
    docs = []
    for docid in docids:
        root = ET.parse(dir_path + '%s.xml' % docid).getroot()
        title = root.find('title').text
        body = root.find('body').text
        doc = {'title': title, 'description': body,'id': docid}
        docs.append(doc)
    return docs
if __name__ == '__main__':
    keys='洪都拉斯'
    print(search(keys))