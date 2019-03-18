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

    # 计算讲稿数量
    count_row_speech = 'SELECT COUNT(speech_id) FROM speech_sheet'
    cursor.execute(count_row_speech)
    row_no_dict = cursor.fetchone()
    row_no = row_no_dict['COUNT(speech_id)']

    # 循环读取稿子
    sen_id = 0  # 设置句子表的句子id计数器
    for sp_id in range(row_no):
        sp_id = sp_id + 1    # 讲稿id

        query_speech = ('SELECT speech_content FROM speech_sheet WHERE speech_id = {0}').format(sp_id)
        cursor.execute(query_speech)
        outcome = cursor.fetchall()
        #print(type(outcome))
        data_speech_str = str(outcome[0])
        #调用函数删除“\n”“■”和空格
        data_speech = process_page(data_speech_str)
        print(data_speech)

        # data_speech = '中共中央总书记、国家主席、中央军委主席习近平在开班式上发表重要讲话强调，培养选拔优秀年轻干部是一件大事，关乎党的命运、国家的命运、民族的命运、人民的福祉，是百年大计。中共中央政治局常委、中央书记处书记王沪宁出席开班式。谢谢大家！'
        # 创建LtpProcess()实例，进行分句、分词、词性分析等一系列处理
        ltp_speech = LtpProcess(data_speech)
        sentence_result, word_result = ltp_speech.ltp()  # sentence_result类型是一维列表, word_result类型是二维列表

        print("*************总结果*************")

        # 循环读取分句处理结果，存入sentence_sheet表
        for sen_re_str in sentence_result:
            sen_id = sen_id + 1
            insert_sentence = ("INSERT INTO sentence_sheet (sentence_id, speech_id_of_sentence, sentence_content)"
                               "VALUE ({0}, {1}, '{2}')").format(sen_id, sp_id, sen_re_str)
            cursor.execute(insert_sentence)
            cnx.commit()

        """
        # 循环读取分词、词性标记等，存入word_sheet表
        wor_id = 0
        for w_list in word_result:
            wor_id = wor_id +1
            insert_word = ("INSERT INTO word_sheet (word_id, sentence_id_of_word, ) VALUE ({0}, '{1}')").format(sen_id, sen_re_str)
        """
        cursor.close()
        cnx.close()

if __name__ == '__main__':
    main()