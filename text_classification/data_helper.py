
# coding: utf-8

# ### 基于THU语料库的文本分类实验的数据处理util

# In[4]:

import numpy as np
import codecs
import re
import os
from sklearn.utils import shuffle
from tensorflow.contrib import learn


# In[26]:

#category = ['星座', '股票', '房产', '时尚', '体育', '社会', '家居', '游戏', '彩票', '科技', '教育', '时政', '娱乐', '财经']
category = ['体育', '股票', '科技']


# In[27]:

def split_data_and_label(corpus):
    """
    将数据划分为训练数据和样本标签
    :param corpus: 
    :return: 
    """
    input_x = []
    input_y = []

    tag = []
    if os.path.isfile(corpus):
        with codecs.open(corpus, 'r') as f:
            for line in f:
                tag.append(re.sub('[\xa0\n\r\t]+', '' , line))
                
    else:
        for docs in corpus:
            for doc in docs:
                tag.append(doc)
    tag = shuffle(tag)
    for doc in tag:
        index = doc.find(' ')
        tag= doc[:index]
        tag = re.sub('__label__', '', tag)
        try:
            i = category.index(tag)
        except ValueError:
            continue
        input_y.append(i)
        
        input_x.append(doc[index + 1 :])
    
    return [input_x, input_y]


# ### pad sequence

# In[28]:

def pad_sequence(input_x, maxlen):
    """
    对数据进行padding,短的进行填充，长的进行截取
    :param input_x: 
    :return: 转化为index的语料库以及word:id的矩阵
    """

    #  keras method for corpus preprocess...
    # tokenizer = Tokenizer(num_words=num_words)
    # tokenizer.fit_on_texts(input_x)
    # # 将原始的词语转化为index形式
    # sequences = np.array(tokenizer.texts_to_sequences(input_x))
    #
    # # for maxlen and encode text to index less using padding
    # max_len = max([len(x.split(' ')) for x in input_x])
    # if maxlen is None:
    #     maxlen = max_len
    # maxlen = min(max_len, maxlen)
    # sequences = sequence.pad_sequences(sequences, maxlen=maxlen)
    # return sequence, tokenizer.word_index

    # tf method

    max_len = max([len(x.split(' ')) for x in input_x])
    if maxlen is None:
        maxlen = max_len
    maxlen = min(max_len, maxlen)
    vocab_process = learn.preprocessing.VocabularyProcessor(max_document_length=maxlen)
    input_x = np.array(list(vocab_process.fit_transform(input_x)))
    return input_x, vocab_process.vocabulary_._mapping


# ### one-hot for category

# In[29]:

def label_one_hot(targets, nb_classes):
    """
    标签进行one-hot 处理
    :param targets: 一维的类别列表,类别标签从0开始
    :param nb_classes: 
    :return: 
    """
    return np.eye(nb_classes)[np.array(targets).reshape(-1)]


# ### 加载数据，得到处理好的数据

# In[30]:

def load_data(file_path, maxlen):
    """
    加载数据
    :param file_path: 
    :param num_words: 
    :param maxlen: 
    :return: index and padding and numpy input_x, one-hot input_y, word-index mapping 
    """
    input_x, input_y = split_data_and_label(file_path)
    input_x, words_index = pad_sequence(input_x, maxlen)

    label_ = set()
    [label_.add(y) for y in input_y]
    nb_class = len(label_)
    input_y = label_one_hot(input_y, nb_class)
    return input_x, input_y, words_index


# ### batch data generate

# In[31]:

def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    针对训练数据，组合batch iter
    :param data:
    :param batch_size: the size of each batch
    :param num_epochs: total of epochs
    :param shuffle: 是否需要打乱数据
    :return:
    """
    data = np.array(data)
    # 样本数量
    data_size = len(data)
    # 根据batch size 计算一个epoch中的batch 数量
    num_batches_per_epoch = int((len(data) - 1) / batch_size) + 1
    # generates iter for dataset.
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]


# #### load data from pkl

# In[8]:

def load_data_pkl(file_path):
    """
    从制作好的文件中读取测试集和训练集，这样可以避免在不同的实验中，shuffle到不同的train/dev数据
    :param file_path: 
    :return: 
    """
    import pickle
    if not os.path.exists(file_path):
        raise FileNotFoundError('FILE NOT FOND IN %s', file_path)
    with open(file_path, 'rb') as fd:
        input_x, input_y, word_index = pickle.load(fd)
    return input_x, input_y, word_index


# In[9]:

if __name__ == '__main__':
    
    resources = r'C:\workspace\python\MQNLP\resources'
    
    input_x, input_y, word_index = load_data_pkl(os.path.join(resources, 'thu_data_3class_3k.pkl'))


# In[11]:




# In[ ]:



