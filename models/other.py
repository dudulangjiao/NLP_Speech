# -*- coding: utf-8 -*-
import re


def process_page(page_content):
    """创建一个函数，用来对文本进行删除换行符、空格等处理"""

    remove_n = re.compile('\\\\n')  # 去除换行符\n
    remove_square = re.compile('■')  # 去除■
    remove_space = re.compile(' ')  # 去除空格

    page_content = remove_n.sub('', page_content)
    page_content = remove_square.sub('', page_content)
    page_content = remove_space.sub('', page_content)

    return page_content