#!/usr/bin/python3
# -*- coding: utf-8 -*-

from models.base import LtpProcess
from models.other import process_page
import mysql.connector

def main():
    """从讲稿数据库取出文本内容，交给ltp处理。"""

    cnx = mysql.connector.connect(user='root', password='314159',
                                  host='localhost',
                                  database='SpeechCollection')
    cursor = cnx.cursor(dictionary=True)
    query_speech = 'SELECT speech_content FROM speech_sheet WHERE speech_id = 1 or speech_id = 2'
    cursor.execute(query_speech)
    outcome = cursor.fetchall()
    print(type(outcome))
    data_speech_str = str(outcome[0])
    #调用函数删除“\n”和空格
    data_speech = process_page(data_speech_str)
    print(data_speech)

    # 创建LtpProcess()实例
    ltp_speech = LtpProcess(data_speech)
    ltp_speech.ltp()


if __name__ == '__main__':
    main()