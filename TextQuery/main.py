# encoding=utf-8

"""
FILE   : main
PROJECT: TextQuery
AUTHOR : bj
DATE   : 2016-05-15 12:20
"""

import sys

import querytable


SENTENCE_ENDING = ('.', '?', '!')


def split_sentence(document):
    """
    Split a document to sentences.
    :param document: string
    :return: list of string
    """
    check_string(document)
    i = 0
    j = 0
    length = len(document)
    while j != length:
        if document[i] not in SENTENCE_ENDING and document[j] in SENTENCE_ENDING:
            yield document[i:j]
            i = j
            j += 1
        elif document[i] in SENTENCE_ENDING:
            i = j
            j += 1
        elif document[i] not in SENTENCE_ENDING and document[j] not in SENTENCE_ENDING:
            j += 1


def split_word(sentence):
    """
    Split a sentence to words.
    :param sentence: string
    :return: list of string
    """
    check_string(sentence)
    i = 0
    j = 1
    word_list = []
    length = len(sentence)
    while j != length:
        if sentence[i].isalpha() and not sentence[j].isalpha():
            word_list.append(sentence[i:j])
            i = j
            j = i + 1
        elif sentence[i].isalpha() and sentence[j].isalpha():
            j += 1
        elif not sentence[i].isalpha():
            i = j
            j += 1
    if sentence[i:j].isalpha():
        word_list.append(sentence[i:j])

    return word_list


def check_string(filename):
    if not isinstance(filename, str):
        raise TypeError('Type error: str')


def process_text_file(filename):
    """
    read a text file, convert to lower case, remove space characters
    :param filename: string
    :return: list of string
    """
    check_string(filename)
    with open(filename, 'r') as f:
        text_list = f.readlines()
    text_list = [s.strip().lower() for s in text_list]
    return text_list


def read_document(filename):
    """
    read a document file by a filename
    :param filename: string
    :return: string
    """
    check_string(filename)
    sentences = process_text_file(filename)
    return ''.join(sentences)


def read_query(filename):
    """
    read a query file by a filename.
    :param filename: string
    :return:  a list string.
    """
    check_string(filename)
    return process_text_file(filename)


def query_word_in_list(word_list, word):
    """
    query a word in a word list
    :param word_list: list of string
    :param word: string
    :return: int, the sequence number of the word in the word list. start at 1
    """
    check_string(word)
    occurrences = []
    # for i, w in enumerate(word_list):
    #     if word == w:
    #         occurrences.append(i + 1)
    # return occurrences
    start = 0
    try:
        while True:
            pos = word_list[start:].index(word) + 1
            occurrences.append(pos + start)
            start += pos
    except ValueError:
        return occurrences


def split_document_to_table(document):
    """
    split a document to a list of lists
    :param document: string consist of many sentences
    :return: a list of lists, the inner list contains words in a sentences.
        the outer list contains the word lists.
    """
    word_lists = []
    for sentence in split_sentence(document):
        word_lists.append(split_word(sentence))

    return word_lists


def build_table(query_table, document):
    """
    split document into words and add to query_table.
    :param document: string
    :param query_table: QueryTable instance,
        query table is data structure to store word and its position in a document.
    :return: None
    """
    check_string(document)

    for sentence_num, sentence in enumerate(split_sentence(document)):
        for word_num, word in enumerate(split_word(sentence)):
            query_table.add(word, sentence_num+1, word_num+1)


def split_document_to_table_generator(document):
    for sentence in split_sentence(document):
        yield split_word(sentence)


def query_word_in_table(table, word):
    check_string(word)
    occurrences = []
    for row, word_list in enumerate(table):
        result = query_word_in_list(word_list, word)
        if len(result):
            occurrences.extend(['%s/%s' % (row+1, n) for n in result])
    return occurrences


def query_word_in_sentence(sentence, word):
    start = 0
    length = len(word)
    occurrences = []
    while True:
        pos = sentence.find(word, start)
        if pos == -1:
            break


def query_table_test():
    args = sys.argv
    if len(args) < 3:
        return 0

    document_filename = args[1]
    query_filename = args[2]
    document = read_document(document_filename)

    qt = querytable.QueryTable()
    build_table(qt, document)
    for query in read_query(query_filename):
        print(query, qt.query(query))

    print('collision per add: {cpa}'.format(cpa=qt.collision_per_add))
    print('collision per query: {cpq}'.format(cpq=qt.collision_per_query))
    print('the length of query table: {len}'.format(len=qt.TableSize))
    print('load factor: {lf}'.format(lf=qt.load_factor))

if __name__ == '__main__':
    query_table_test()
