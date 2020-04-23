# -*- coding: utf-8 -*-
# @Title: tf_idf.py
# @Package
# @Description:

import jieba
import os

from operator import itemgetter

class tf_idf:

    def __init__(self):
        self.files = {}
        self.corpus = {}
        self.stop_words = set(())
        content = open('./dictionary/stop_words.txt', 'rb').read().decode('utf-8')
        for line in content.splitlines():
            self.stop_words.add(line)

    # 给定一个文件夹路径进行分析
    def process(self, file_dir):
        dir = os.path.dirname(__file__)
        folder = os.path.join(dir, '../data/' + folder_name)
        # num_of_files = len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))]) + 1

        for root, dirs, files in os.walk(file_dir):
            for filename in files:
                file_path = root + "/" + filename
                self.add_file(file_path)

        pass


    # 统计每个文件的tf值
    def add_file(self, file_path):
        # Load data and cut
        content = open(file_path, 'rb').read() if file_name[0] == '/' or file_name[0] == 'C' else open(
            '../data/' + file_path, 'rb').read()
        words = jieba.cut(content)
        file_name = file_path.split("/")[-1]

        # Build dictionary
        # 统计每个单词在文档出现的次数
        dictionary = {}
        for w in words:
            if len(w.strip()) < 2 or w.lower() in self.stop_words:
                continue
            dictionary[w] = dictionary.get(w, 0.0) + 1.0
            self.corpus[w] = self.corpus.get(w, 0.0) + 1.0

        # Get term frequency
        total = sum(dictionary.values())
        for k in dictionary:
            dictionary[k] /= total

        # Add tf to the corpus
        self.files[file_name] = dictionary


    def get_tf_idf(self, file_name, top_k):
        # Get inverse document frequency
        tf_idf_of_file = {}

        # 统计含有关键词的文档数
        for w in self.corpus.keys():
            w_in_f = 1.0 # 初始值设置为1
            for f in self.files:
                if w in self.files[f]:
                    w_in_f += 1.0
            # Get tf-idf
            if w in self.files[file_name]:
                tf_idf_of_file[w] = log(len(self.files) / w_in_f) * self.files[file_name][w]
        # Top-K result of tf-idf
        tags = sorted(tf_idf_of_file.items(), key=itemgetter(1), reverse=True)
        return tags[:top_k]


    def similarities(self, list_of_words):
        # Building the query dictionary
        query_dict = {}
        for w in list_of_words:
            query_dict[w] = query_dict.get(w, 0.0) + 1.0

        # Normalizing the query
        length = float(len(list_of_words))
        for k in query_dict:
            query_dict[k] = query_dict[k] / length

        # Get the list of similarities
        sims = []
        for f in self.files:
            score = 0.0
            for k in query_dict:
                if k in self.files[f]:
                    score += (query_dict[k] / self.corpus[k]) + (self.files[f][k] / self.corpus[k])
            sims.append([f, score])

        return sorted(sims, key=itemgetter(1), reverse=True)


if __name__ == '__main__':
    t = tf_idf()
    table = tf_idf()
    folder_name = 'huawei mobile'

    for x in range(1, num_of_files):
        file_name = folder_name + '/' + str(x).zfill(2) + '.txt'
        table.add_file(file_name)

    top_k = 40
    # for x in range(1, num_of_files):
    #     target_file = folder_name + '/' + str(x).zfill(2) + '.txt'
    #     print('Top ' + str(top_k) + ' of tf-idf in ' + target_file + ' : ')
    #     print(table.get_tf_idf(target_file, top_k))
    #     print()
    #
    # key_word = 'huawei'
    # print('tf-idf of key word "' + key_word + ' : ')
    # print(table.similarities([key_word]))