# -*- coding: utf-8 -*-
import sys, os


# 创建一个类，用来进行NLP处理
class LtpProcess(object):
    """创建一个类，用来进行NLP处理。

    Attributes:
                content: 要处理的文本内容

    """

    def __init__(self, content):
        self.content = content

    def ltp(self):
        """创建ltp方法来处理文本"""
        sys.path.append('/var/lib')
        from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

        # Set your own model path 设置模型路径
        MODELDIR = "/vagrant/software/ltp_data_v3.4.0"

        # 变量paragrah保存要进行处理的文字段落。
        paragraph = self.content

        # 分句
        sentence_list = SentenceSplitter.split(paragraph)
        sentence = sentence_list[7]


        # 分词
        segmentor = Segmentor()
        segmentor.load(os.path.join(MODELDIR, "cws.model"))
        words = segmentor.segment(sentence)

        print("*************分词*****************")
        print("\t".join(words))

        # 词性标注
        postagger = Postagger()
        postagger.load(os.path.join(MODELDIR, "pos.model"))
        postags = postagger.postag(words)
        print("*************词性标注*************")
        print("\t".join(postags))

        # 依存句法分析
        parser = Parser()
        parser.load(os.path.join(MODELDIR, "parser.model"))
        arcs = parser.parse(words, postags)
        print("*************依存句法分析*************")
        print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

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