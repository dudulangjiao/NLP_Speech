#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

# 创建一个类，用来进行NLP处理
class LtpProcess(object):
    """创建一个类，用来进行NLP处理

    Attributes:
                content: 要处理的文本内容

    """

    def __init__(self, content):
        self.content = content

    def ltp(self):
        #形成本程序文件（main.py）所在的文件目录的上一级目录：/vagrant。
        ROOTDIR = os.path.join(os.path.dirname(__file__), os.pardir)
        # sys.path是python搜索模块的路径集，对象类型是list"""
        # 这句是把/vagrant/lib路径添加到sys.path
        sys.path = [os.path.join(ROOTDIR, "lib")] + sys.path

        # Set your own model path 设置模型路径
        # ROOTDIR为/vagrant，经过拼接路径，
        # 形成ROOTDIR为/vagrant/software/ltp_data_v3.4.0
        MODELDIR=os.path.join(ROOTDIR, "software/ltp_data_v3.4.0")
        # 变量paragrah保存要进行处理的文字段落。
        paragraph = self.content

        # 分句
        sentence_list = SentenceSplitter.split(paragraph)
        sentence = sentence_list[0]
        print(type(sentence_list))

        # 分词
        segmentor = Segmentor()
        segmentor.load(os.path.join(MODELDIR, "cws.model"))
        words = segmentor.segment(sentence)
        print(type(words))
        print("**************************************")
        print("\t".join(words))

        # 词性标注
        postagger = Postagger()
        postagger.load(os.path.join(MODELDIR, "pos.model"))
        postags = postagger.postag(words)
        print("\t".join(postags))

        # 依存句法分析
        parser = Parser()
        parser.load(os.path.join(MODELDIR, "parser.model"))
        arcs = parser.parse(words, postags)
        print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

        # 命名实体识别
        recognizer = NamedEntityRecognizer()
        recognizer.load(os.path.join(MODELDIR, "ner.model"))
        netags = recognizer.recognize(words, postags)
        print("\t".join(netags))

        # 语义角色标注
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


# 创建LtpProcess()实例

ltp_speech = LtpProcess('2019年1月25日，中共中央政治局在人民日报社就全媒体时代和媒体融合发展举行第十二次集体学习。中共中央总书记习近平主持学习并发表重要讲话。')
ltp_speech.ltp()