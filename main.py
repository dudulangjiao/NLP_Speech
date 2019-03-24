#!/usr/bin/python3
# -*- coding: utf-8 -*-

from models.base import LtpProcess
from models.other import process_page
from pyltp import SentenceSplitter
import mysql.connector
import time

def main():
    """从讲稿数据库取出文本内容，交给ltp处理。"""
    time_start_main = time.time()
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
    for sp_id in range(row_no):
        time_start = time.time()  # 开始处理一篇文稿的时间

        sp_id = sp_id + 1    # 讲稿id
        query_speech = ('SELECT speech_content FROM speech_sheet WHERE speech_id = {0}').format(sp_id)
        cursor.execute(query_speech)
        outcome = cursor.fetchone()
        #print(type(outcome))
        data_speech_str = str(outcome['speech_content'])
        #调用函数删除“\n”“■”和空格
        data_speech = process_page(data_speech_str)
        #print(data_speech)

        #data_speech = '新华社北京3月1日电（记者吴晶、姜潇）2019年春季学期中央党校（国家行政学院）中青年干部培训班1日上午在中央党校开班。中共中央总书记、国家主席、中央军委主席习近平在开班式上发表重要讲话强调，培养选拔优秀年轻干部是一件大事，关乎党的命运、国家的命运、民族的命运、人民的福祉，是百年大计。'
        # 创建LtpProcess()实例，进行分句、分词、词性分析等一系列处理
        sentence_list = SentenceSplitter.split(data_speech)

        #print("*************总结果*************")

        # 循环进行分句处理，存入sentence_sheet表
        index_sen_in_sp = 0  # 设置句子表speech_sheet的句子在讲稿的位置索引
        for sentence_str in sentence_list:
            index_sen_in_sp = index_sen_in_sp + 1
            insert_sentence = ("INSERT INTO sentence_sheet (speech_id_of_sentence, index_sentence_in_speech, sentence_content)"
                               "VALUE ({0}, {1}, '{2}')").format(sp_id, index_sen_in_sp, sentence_str)
            cursor.execute(insert_sentence)
            cnx.commit()

            # 用类LtpProcess进行分词处理
            ltp_instance = LtpProcess(sentence_str)
            word_list = ltp_instance.ltp_word()  # word_list类型是二维列表

            # 循环进行分词、词性标记处理，存入word_sheet表
            index_w_in_sen = 0  # 设置词组表word_sheet的词组在句子的位置索引
            for word_str in word_list:
                index_w_in_sen = index_w_in_sen + 1

                insert_word = ("INSERT INTO word_sheet (speech_id_of_word, index_sentence_of_word_in_speech,"
                               "index_word_in_sentence, word_content, part_speech_tag_word,"
                               "named_entity_tag_word, depend_syntax_head_word, depend_syntax_tag_word)"
                               "VALUE ({0}, {1}, {2}, '{3}', '{4}', '{5}', {6}, '{7}')").format(sp_id, index_sen_in_sp,
                                                                                                index_w_in_sen,
                                                                                                word_str[0],
                                                                                                word_str[1],
                                                                                                word_str[2],
                                                                                                word_str[3],
                                                                                                word_str[4])

                cursor.execute(insert_word)
                cnx.commit()

        time_end = time.time()  # 结束一篇文稿处理的时间
        time_process = round((time_end - time_start)/60, 1)  # 处理一篇文稿花费的时间
        time_main = round((time_end - time_start_main)/3600, 2) # 目前程序运行的时间
        print('稿子总篇数：共' + str(row_no) + '篇。 完成进度：已完成第' + str(sp_id) + '篇。 处理该篇稿子用时' + str(time_process) +
              '分钟。 程序已运行' + str(time_main) + '小时。')

    cursor.close()
    cnx.close()

if __name__ == '__main__':
    main()