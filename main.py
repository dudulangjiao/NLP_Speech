#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

# 创建一个类，用来进行NLP处理
class LtpProcess(object):

    def __init__(self, content):
        self.content = content

    def ltp(self):
# 用拼接文件路径函数os.path.join()，形成本程序文件（main.py）所在的文件目录os.path.dirname(__file__)的上一级目录：/vagrant。
        ROOTDIR = os.path.join(os.path.dirname(__file__), os.pardir)
# sys.path是python搜索模块的路径集，对象类型是list
# 这句是把/vagrant/lib路径添加到sys.path
        sys.path = [os.path.join(ROOTDIR, "lib")] + sys.path

# Set your own model path 设置模型路径
# ROOTDIR为/vagrant，经过拼接路径，ROOTDIR为/vagrant/software/ltp_data_v3.4.0
        MODELDIR=os.path.join(ROOTDIR, "software/ltp_data_v3.4.0")
# 变量paragrah保存要进行处理的文字段落。
        paragraph = self.content

# 调用分词方法split对文字段落进行分句处理，并把第一句话保存到变量sentence。
        sentence_list = SentenceSplitter.split(paragraph)
        sentence = sentence_list[0]
        print(type(sentence_list))


        segmentor = Segmentor() # 创建Segmentor实例
        segmentor.load(os.path.join(MODELDIR, "cws.model")) # 加载分词模型
        words = segmentor.segment(sentence) # 调用segment方法进行分词
        print(type(words))
        print("**************************************")
        print("\t".join(words))

        postagger = Postagger()
        postagger.load(os.path.join(MODELDIR, "pos.model"))
        postags = postagger.postag(words)
# list-of-string parameter is support in 0.1.5
# postags = postagger.postag(["中国","进出口","银行","与","中国银行","加强","合作"])
        print("\t".join(postags))

        parser = Parser()
        parser.load(os.path.join(MODELDIR, "parser.model"))
        arcs = parser.parse(words, postags)

        print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

        recognizer = NamedEntityRecognizer()
        recognizer.load(os.path.join(MODELDIR, "ner.model"))
        netags = recognizer.recognize(words, postags)
        print("\t".join(netags))

        labeller = SementicRoleLabeller()
        labeller.load(os.path.join(MODELDIR, "pisrl.model"))
        roles = labeller.label(words, postags, arcs)

        for role in roles:
            print(role.index, "".join(
                  ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))

        segmentor.release()
        postagger.release()
        parser.release()
        recognizer.release()
        labeller.release()