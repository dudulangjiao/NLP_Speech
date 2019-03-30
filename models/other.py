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

def list_conversion(*args):
    """创建一个函数，用来转化二维列表结构。

    把([1, 2, 3],['a', 'b', 'c'],['e', 'f', 'g']) 数组结构
    转化为：[[1, a, e],['2', 'b', 'e'],['3', 'c', 'g']] 列表结构

    """
    x = len(args[0])
    list_conversion_result = [[] for i in range(x)]
    #print(list_conversion_result)

    for v in args:
        u = 0
        for y in v:

            list_conversion_result[u].append(y)
            u = u + 1
            #print('数组结果')
            #print(list_conversion_result)

    return list_conversion_result