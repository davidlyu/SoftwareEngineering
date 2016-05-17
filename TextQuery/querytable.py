# encoding=utf-8

"""
FILE   : querytable
PROJECT: TextQuery
AUTHOR : bj
DATE   : 2016-05-17 00:20
"""

import sys


class QueryTable(object):
    """
    query table is data structure to store word and its position in a document.
    """
    # TableSize value maybe change in method enlarge, is a prime that greater than 100,000
    TableSize = 10007
    LOAD_FACTOR_LIMIT = 0.9

    def __init__(self):
        object.__init__(self)

        self._table = [None] * QueryTable.TableSize
        self._size = 0

        self._total_add_count = 0
        self._total_query_count = 0
        self._add_collision_count = 0
        self._query_collision_count = 0

    @property
    def collision_per_add(self):
        return self._add_collision_count / self._total_add_count

    @property
    def collision_per_query(self):
        return self._query_collision_count / self._total_query_count

    @property
    def load_factor(self):
        return self._size / QueryTable.TableSize

    @staticmethod
    def hash(word):
        if not isinstance(word, str):
            raise TypeError('Type error: word')

        size = len(word)
        hash_value = 0
        for i in range(size):
            hash_value = (hash_value << 5) + ord(word[i])

        return hash_value % QueryTable.TableSize

    def add(self, word, sentence_num, word_num):
        """
        add a word and its position into query table.
        :param word: string
        :param sentence_num: int, the position of the sentence.
        :param word_num: int, the of the word.
        :return: None
        """

        if not isinstance(word, str):
            raise TypeError('Type error: word')

        self._total_add_count += 1
        if self.size > QueryTable.LOAD_FACTOR_LIMIT * QueryTable.TableSize:
            self.enlarge()

        hash_value = self.hash(word)
        while True:
            if self._table[hash_value] is None:
                self._table[hash_value] = (word, [(sentence_num, word_num)])
                self._size += 1
                break
            elif self._table[hash_value][0] == word:
                self._table[hash_value][1].append((sentence_num, word_num))
                break
            else:
                hash_value += 1
                self._add_collision_count += 1

    def enlarge(self):
        QueryTable.TableSize = QueryTable.TableSize * 2 + 1
        old_table = self._table
        self._table = [None] * QueryTable.TableSize
        for record in old_table:
            if record is not None:
                word = record[0]
                for sentence_num, word_num in record[1]:
                    self.add(word, sentence_num, word_num)

        old_table.clear()

    @property
    def size(self):
        return self._size

    def query(self, word):
        """
        query a word
        :param word: string, the word to be queried
        :return: list of tuples, tuple form (sentence_num, word_num), None if word not exists in query table.
        """
        if not isinstance(word, str):
            raise TypeError('Type error: word')

        self._total_query_count += 1
        hash_value = self.hash(word)
        while self._table[hash_value] is not None:
            if self._table[hash_value][0] == word:
                return self._table[hash_value][1]
            else:
                hash_value += 1
                self._query_collision_count += 1
        return None


if __name__ == '__main__':
    query_table = QueryTable()

    sentence = 'Five years ago, you had to have a couple of Michelin stars your own TV show have'
    for i, word in enumerate(sentence.split(' ')):
        query_table.add(word, 1, i+1)

    for i, word in enumerate(sentence.split(' ')):
        print(word, query_table.query(word))

    query_table.enlarge()

    print('*' * 80)
    for i, word in enumerate(sentence.split(' ')):
        print(word, query_table.query(word))
    print('size ', query_table.size)

