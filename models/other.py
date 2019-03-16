# -*- coding: utf-8 -*-
import re

# 创建一个函数，用来对文本进行删除换行符、空格等处理

def process_page(page_content):
    # 去除换行符\n
    remove_n = re.compile('\\\\n')
    # 去除空格
    remove_square = re.compile('■')
    remove_space = re.compile(' ')

    page_content = remove_n.sub('', page_content)
    page_content = remove_square.sub('', page_content)
    page_content = remove_space.sub('', page_content)

    return page_content