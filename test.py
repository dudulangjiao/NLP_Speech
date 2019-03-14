#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os

ROOTDIR = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path = [os.path.join(ROOTDIR, "lib")] + sys.path

# Set your own model path 设置模型路径
MODELDIR=os.path.join(ROOTDIR, "/vagrant/software/ltp_data_v3.4.0")

from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

paragraph = '这里，我结合当前福州发展情况，就市职教社的今后工作谈几点个人想法。'

sentence = SentenceSplitter.split(paragraph)[0]

segmentor = Segmentor()
segmentor.load(os.path.join(MODELDIR, "cws.model"))
words = segmentor.segment(sentence)
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