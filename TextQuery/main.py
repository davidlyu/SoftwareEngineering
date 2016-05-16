# encoding=utf-8

"""
FILE   : main
PROJECT: TextQuery
AUTHOR : bj
DATE   : 2016-05-15 12:20
"""

import sys
import os
import profile

import querytable


SENTENCE_ENDING = ('.', '?', '!')


def split_sentence(document):
    """
    Split a document to sentences.
    :param document: string
    :return: list of string
    """
    check_string(document)
    sentences = []
    i = 0
    j = 0
    length = len(document)
    while j != length:
        if document[i] not in SENTENCE_ENDING and document[j] in SENTENCE_ENDING:
            sentences.append(document[i:j])
            i = j
            j += 1
        elif document[i] in SENTENCE_ENDING:
            i = j
            j += 1
        elif document[i] not in SENTENCE_ENDING and document[j] not in SENTENCE_ENDING:
            j += 1
    return sentences


def split_word(sentence):
    """
    Split a sentence to words.
    :param sentence: string
    :return: list of string
    """
    check_string(sentence)
    words = []
    i = 0
    j = 1
    length = len(sentence)
    while j != length:
        if sentence[i].isalpha() and not sentence[j].isalpha():
            words.append(sentence[i:j])
            i = j
            j = i + 1
        elif sentence[i].isalpha() and sentence[j].isalpha():
            j += 1
        elif not sentence[i].isalpha():
            i = j
            j += 1
    if sentence[i:j].isalpha():
        words.append(sentence[i:j])

    return words


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


def split_word_and_add(query_table, document):
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


def main():
    args = sys.argv
    if len(args) < 3:
        return 0
    document_filename = args[1]
    query_filename = args[2]
    document = read_document(document_filename)

    for query in read_query(query_filename):
        table = split_document_to_table_generator(document)
        occ = query_word_in_table(table, query)
        if not len(occ):
            print('None')
        else:
            print(','.join(occ))

    return 0


def query_table_test():
    args = sys.argv
    if len(args) < 3:
        return 0

    document_filename = args[1]
    query_filename = args[2]
    document = read_document(document_filename)

    qt = querytable.QueryTable()
    split_word_and_add(qt, document)
    for query in read_query(query_filename):
        print(query, qt.query(query))

if __name__ == '__main__':

#     document = """
#     Five years ago, you had to have a couple of Michelin stars, your own TV show, or have concocted the next big food trend to earn a publishing deal that launched your new cookbook.
# Now it's all about your followers on social media.
# Thirteen-year-old Californian food blogger Chase Bailey - who has autism - has just written his first cookbook after gaining more than 200,000 views for his YouTube page, Chase 'N Yur Face.
# His weekly posts see him cooking new recipes, working with established chefs and teaching his thousands of subscribers to cook soups and macaroni cheese dishes.
# "Food influencers like Chase have definitely changed how we look for new authors," Chase's publisher, James Fraioli of Culinary Book Creations, tells the BBC."""

    # sentences = split_sentence(document)
    # print('\n'.join(sentences))
    # print(len(sentences))
    # sys.exit(main(sys.argv[1:]))

    # query_list = []
    # query_list = read_query('query.txt')
    # print('\n'.join(map(lambda s: '"' + s + '"', query_list)))

    # word_list = ['on', 'social', 'media', 'social']
    # word = 'social'
    # print(query_word(word_list, word))
    # print(query_word(word_list, 'hello'))

    # print(' '.join(query_word_in_document(document, 'have')))
    # profile.run("main()")
    # main()
    # print(query_word_in_list(['a', 'b', 'hel', 'fuc', 'b', 'hel', 'fuc', 'e','e'], ''))
    # for word_list in split_document_to_table(document):
    #     print(word_list)
    # table = split_document_to_table(document)
    # print(query_word_in_table(table, 'have'))

    # query_table = querytable.QueryTable()
    # split_word_and_add(query_table, document)
    # print('Five', query_table.query('Five'))

    query_table_test()
