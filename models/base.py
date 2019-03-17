# -*- coding: utf-8 -*-
import sys, os
sys.path.append('/var/lib')
from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
from models.other import list_conversion

# Set your own model path 设置模型路径
MODELDIR = "/vagrant/software/ltp_data_v3.4.0"


class LtpProcess(object):
    """创建一个类，用来进行NLP处理。

    Attributes:
                content: 要处理的文本内容

    """

    def __init__(self, content):
        self.content = content

    def ltp_word(self, ok):
        """创建一个方法，用来进行句子的分词、词性分析等处理。"""
        # 分词
        segmentor = Segmentor()
        segmentor.load(os.path.join(MODELDIR, "cws.model"))
        words = segmentor.segment(ok)
        print("*************分词*****************")
        print("\t".join(words))

        # 词性标注
        postagger = Postagger()
        postagger.load(os.path.join(MODELDIR, "pos.model"))
        postags = postagger.postag(words)
        print("*************词性标注*************")
        print(type(postags))
        print("\t".join(postags))

        # 依存句法分析
        parser = Parser()
        parser.load(os.path.join(MODELDIR, "parser.model"))
        arcs = parser.parse(words, postags)
        print("*************依存句法分析*************")
        print(type(arcs))
        print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

        # 把依存句法分析结果的head和relation分离出来
        arcs_head = []
        arcs_relation = []
        for arc in arcs:
            arcs_head.append(arc.head)
            arcs_relation.append(arc.relation)

        # 命名实体识别
        recognizer = NamedEntityRecognizer()
        recognizer.load(os.path.join(MODELDIR, "ner.model"))
        netags = recognizer.recognize(words, postags)
        print("*************命名实体识别*************")
        print("\t".join(netags))

        # 语义角色标注
        labeller = SementicRoleLabeller()
        labeller.load(os.path.join(MODELDIR, "pisrl.model"))
        roles = labeller.label(words, postags, arcs)
        print("*************语义角色标注*************")
        for role in roles:
            print(role.index, "".join(
                ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))

        segmentor.release()
        postagger.release()
        parser.release()
        recognizer.release()
        labeller.release()

        #返回一个二维列表
        words_result = [words, postags, netags, arcs_head, arcs_relation]

        return words_result


    def ltp(self):
        """创建ltp方法来处理文本"""

        # 变量paragrah保存要进行处理的文字段落
        paragraph = self.content

        # 分句
        sentence_list = SentenceSplitter.split(paragraph)

        # 循环保存并处理每一句
        ltp_result = []  # 处理结果
        sen_id_of_word_int = 0  # 词组所属的句子id
        for sentence in sentence_list:
            sen_id_of_word_int = sen_id_of_word_int + 1
            ltp_word_result = self.ltp_word(sentence)  # 调用ltp_word方法对句子进行分词、词性分析等处理
            #print('ltp_word_result')
            #print(ltp_word_result)
            list_conversion_result = list_conversion(ltp_word_result, sen_id_of_word_int)  # 调用list_conversion函数，把列表结构转化
            ltp_result = ltp_result + list_conversion_result  # 循环累加处理结果

        return ltp_result