#!/usr/bin/python3
# -*- coding: utf-8 -*-

from models.base import LtpProcess
from models.other import process_page
import mysql.connector

def main():
    """从讲稿数据库取出文本内容，交给ltp处理。

    cnx = mysql.connector.connect(user='root', password='314159',
                                  host='localhost',
                                  database='SpeechCollection')
    cursor = cnx.cursor(dictionary=True)
    query_speech = 'SELECT speech_content FROM speech_sheet WHERE speech_id = 2'
    cursor.execute(query_speech)
    outcome = cursor.fetchall()
    #print(type(outcome))
    data_speech_str = str(outcome[0])
    #调用函数删除“\n”“■”和空格
    data_speech = process_page(data_speech_str)
    print(data_speech)

    """

    data_speech = '中共中央总书记、国家主席、中央军委主席习近平在开班式上发表重要讲话强调，培养选拔优秀年轻干部是一件大事，关乎党的命运、国家的命运、民族的命运、人民的福祉，是百年大计。中共中央政治局常委、中央书记处书记王沪宁出席开班式。谢谢大家！'
    # 创建LtpProcess()实例
    ltp_speech = LtpProcess(data_speech)
    rrr = ltp_speech.ltp()

    print("*************总结果*************")
    print(rrr)



if __name__ == '__main__':
    main()