# -*- coding: utf-8 -*-
from pyltp import Segmentor
segmentor = Segmentor()
segmentor.load("/vagrant/software/ltp_data_v3.4.0/cws.model")
words = segmentor.segment("很高兴再次来到“彩虹之国”，同大家相聚在风景秀丽的约翰内斯堡。")
str1 = "|"
print (str1.join(words))
segmentor.release()