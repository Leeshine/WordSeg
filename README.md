简易中文分词实现，实现的算法有正向最大匹配，mmseg4j算法，隐马尔可夫算法
src/Hmm 为隐马尔可夫实现
src/mmSeg/mmseg.py 为简单正向匹配实现
src/mmSeg/complex_mmseg.py 为mmseg4j算法实现

dics中为正向匹配所用词典
icwb2-data为Hmm训练集，测试集，以及评分脚本，具体可参考：http://www.52nlp.cn/中文分词入门资源

score中为一个评分样本
