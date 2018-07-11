import codecs
from sys import argv
import os
from os.path import join
from math import log
import xml.etree.ElementTree as ET
import datetime
import sys


# will be used to make a vector of our song words.
# is a map of our source song bag of words, which count the words of the song.
our_song_word_vector = {}
# will be used to make a hashmap from song name to the vector of his song words.
# this map maps each song name to his bag of words, which count the words of the song.
hash_all_songs_to_his_words_vector = {}
# will be used to make a vector of our songs words counter
# is a map with the all the words of source song to the amount it appear in all the other songs.
songs_word_counter_vector = {}
# vector for full addresses of songs.
songs_addresses = {}
# the song path for be analyzed.
# C:\Users\Osher\Desktop\DhcsAss2\gili.txt
song_path = argv[1]
# the dir of all the tagged song to calculate words.
# C:\Users\Osher\Desktop\DhcsAss2\Tag3
tagged_dir = argv[2]
# the dir of all the xml song to take the metadata.
# C:\Users\Osher\Desktop\DhcsAss2\Ly3
xml_dir = argv[3]
# the songs separated to two groups of song and chorus.
lyrics_suffix = "_Lyrics.txt"
lyrics_suffix_len = len(lyrics_suffix)
chorus_suffix = "_Chorus.txt"
chorus_suffix_len = len(chorus_suffix)
xml_end = ".xml"
# the structure of each word in the lyrics file.
structure = ["verb", "noun", "adverb", "adjective"]
# in absence of an advanced optimization, the b parameter is 0.75
b = 0.75
# in absence of an advanced optimization, the k parameter is between [1.2, 2]
k = 1.6
# the base to calculate the log operation
log_base = 2


def print_hw2():
    print("our_song_word_vector " + our_song_word_vector.__str__())
    # for word in our_song_word_vector:
    #     print(word + " " + our_song_word_vector[word].__str__())
    # print("hash_all_songs_to_his_words_vector: " + hash_all_songs_to_his_words_vector.__str__())
    # for song in hash_all_songs_to_his_words_vector:
    #     for word in song:
    #         print(word.__str__() + " " + str(song[word]))
    print("song_word_vector: " + our_song_word_vector.__str__())
    print("song_path: " + song_path.__str__())
    print("tagged_dir: " + tagged_dir.__str__())
    print("xml_dir:" + xml_dir.__str__())
    print("b: " + str(b))
    print("k: " + str(k))
    print("log_base: " + str(log_base))
    print("HW2HW2HW2HW2HW2HW2HW2HW2HW2HW2HW2HW2HW2HW2HW2HW2HW2HW2HW2HW2HW2HW2HW2")


def print_hash_all_songs_to_his_words_vector():
    print("hash_all_songs_to_his_words_vector: ")
    sys.stdout.flush()
    keys = hash_all_songs_to_his_words_vector.keys()
    for key in keys:
        print(key.__str__() + hash_all_songs_to_his_words_vector[key].__str__())
        sys.stdout.flush()


def print_songs_word_counter_vector():
    print("songs word counter vector: " + songs_word_counter_vector.__str__())


def print_our_song_word_vector():
    print("song_word_vector: ")
    sys.stdout.flush()
    keys = our_song_word_vector.keys()
    for key in keys:
        print(key.__str__() + our_song_word_vector[key].__str__())
        sys.stdout.flush()


def clear_chorus_or_lyrics(last_word_path):
    if last_word_path.endswith(chorus_suffix):
        return last_word_path[:-chorus_suffix_len]
    if last_word_path.endswith(lyrics_suffix):
        return last_word_path[:-lyrics_suffix_len]
    return last_word_path


def get_file_name_from_file_address(file_address):
    path = file_address.__str__()
    # print("path: " + path)
    path_split = path.split('\\')
    # print("path_split: " + path_split.__str__())
    last_word_path = path_split[path_split.__len__() - 1]
    last_word = clear_chorus_or_lyrics(last_word_path)
    return last_word


def df(word):
    if word in songs_word_counter_vector:
        return songs_word_counter_vector[word]
    return 1


def c(word, dictionary):
    return hash_all_songs_to_his_words_vector[dictionary][word]


def average_document_length():
    str_key = "key_for_avg_songs"
    if str_key not in songs_word_counter_vector:
        sum_of_all_songs = 0
        for size in songs_word_counter_vector.values():
            sum_of_all_songs = sum_of_all_songs + size
        sum_of_all_songs = sum_of_all_songs / len(songs_word_counter_vector)
        songs_word_counter_vector[str_key] = sum_of_all_songs
        print("songs_word_counter_vector[str_key]: " + str(songs_word_counter_vector[str_key]))
    return songs_word_counter_vector[str_key]


def tf(word, dictionary):
    return c(word, dictionary) * (k + 1) / \
           (c(word, dictionary) + (k * (1 - b +
                                        (b * songs_word_counter_vector[dictionary] / average_document_length()))))


def idf(word):
    return log((len(songs_word_counter_vector) + 1) / df(word), b)


def sim(dictionary, document):
    sum_of_symmetry = 0
    for word_i in hash_all_songs_to_his_words_vector[dictionary]:
        if word_i in hash_all_songs_to_his_words_vector[document]:
            sum_of_symmetry = sum_of_symmetry + (tf(word_i, dictionary) * tf(word_i, document) * idf(word_i))
    return sum_of_symmetry


def read_file(file_address):
    # print("file_address: " + file_address.__str__())
    file_name = get_file_name_from_file_address(file_address)
    # print("file_name: " + file_name)
    songs_addresses[file_name] = file_address
    if file_name not in hash_all_songs_to_his_words_vector:
        hash_all_songs_to_his_words_vector[file_name] = {}
        songs_word_counter_vector[file_name] = 0
    file_vector = hash_all_songs_to_his_words_vector[file_name]
    size = songs_word_counter_vector[file_name]
    for line in codecs.open(file_address, "r", "utf8"):
        columns = line.split(" ")
        if len(columns) > 4 and columns[4] in structure:
            word = columns[2]
            size = size + 1
            if word in file_vector:
                file_vector[word] = file_vector[word] + 1
            else:
                file_vector[word] = 1
            if word in our_song_word_vector:
                our_song_word_vector[word] = our_song_word_vector[word] + 1
            # print("number: " + size.__str__() + " word: " + word + " size:" + file_vector[word].__str__())
    songs_word_counter_vector[file_name] = size
    # print("\n\n\n##############################")
    # print_hw2()
    # print("##############################\n")


def read_dir():
    for path, directors, files in os.walk(tagged_dir):
        # current_dir = ""
        # current_letter = ""
        for file in files:
            if file == '.DS_Store':
                continue
            # if current_dir != path:
            #     current_dir = path
            #     current_dir_names = current_dir.split('\\')
            #     current_dir_name = current_dir_names[current_dir_names.__len__() - 1]
            #     if current_letter != current_dir_name[0]:
            #         current_letter = current_dir_name[0]
            #         print(current_letter)
            #     print(current_dir_name, end=' ')
            read_file(join(path, file))


def read_document():
    # print("document_address: " + song_path.__str__())
    document_name_draft = get_file_name_from_file_address(song_path)
    document_name = document_name_draft.split('.')[0]
    size = 0
    hash_all_songs_to_his_words_vector[document_name] = {}
    songs_word_counter_vector[document_name] = 0
    for line in codecs.open(song_path, "r", "utf8"):
        columns = line.split(" ")
        if len(columns) > 4 and columns[4] in structure:
            word = columns[2]
            size = size + 1
            if word in our_song_word_vector:
                our_song_word_vector[word] = our_song_word_vector[word] + 1
                hash_all_songs_to_his_words_vector[document_name][word] = \
                    hash_all_songs_to_his_words_vector[document_name][word] + 1
            else:
                our_song_word_vector[word] = 1
                hash_all_songs_to_his_words_vector[document_name][word] = 1
    songs_word_counter_vector[document_name] = size
    # print("\n\n\nread_document_read_document_read_document_read_document_read_document_read_document_")
    # print_hw2()
    # print("##############################\n\n\n")


def similarity():
    print("\nThe similarity START time is: " + datetime.datetime.now().__str__())
    sys.stdout.flush()
    songs_similarity = []
    song_name_draft = get_file_name_from_file_address(song_path)
    song_name = song_name_draft.split('.')[0]
    for dictionary in hash_all_songs_to_his_words_vector:
        # print(dictionary.__str__())
        # sys.stdout.flush()
        if dictionary != song_name:
            songs_similarity.append((dictionary, sim(dictionary, song_name)))
    songs_similarity.sort(key=lambda x: x[1])
    songs_similarity.reverse()
    print("The similarity END time is: " + datetime.datetime.now().__str__() + "\n")
    # sys.stdout.flush()
    return songs_similarity


def change_to_xml_path(song_name):
    song_address = songs_addresses[song_name]
    song = song_address.replace(tagged_dir, xml_dir, 1)
    song = clear_chorus_or_lyrics(song)
    song = song + ".xml"
    return song


def print_top_10_songs_similarity(similarity_matrix):
    print("print_top_10_songs_similarity: ")
    sys.stdout.flush()
    for i in range(1, 10):
        print(str(i) + similarity_matrix[i].__str__())
        sys.stdout.flush()


def print_meta_data():
    similarity_matrix = similarity()
    similarity_matrix.reverse()
    # print_top_10_songs_similarity(similarity_matrix)
    for i in range(1, 10):
        print('%36s' % u'\u202B' "שיר תואם מספר: " u'\u202C' + u'\u202B' + str(i) + u'\u202C')
        song = change_to_xml_path(similarity_matrix[i][0])
        tree = ET.parse(song)
        root = tree.getroot()
        for element in root.iter():
            if element.tag != "" and element.text != " " and element.text != "missing" and element.text != "\n":
                str_to_print = ""
                to_print = 0
                if element.tag == '{http://www.tei-c.org/ns/1.0}title':
                    to_print = 1
                    str_to_print = u'\u202B' "שם השיר:       " u'\u202C'
                if element.tag == '{http://www.tei-c.org/ns/1.0}singer':
                    to_print = 1
                    str_to_print = u'\u202B' "שם הזמר:       " u'\u202C'
                if element.tag == '{http://www.tei-c.org/ns/1.0}writer':
                    to_print = 1
                    str_to_print = u'\u202B' "שם הכותב:      " u'\u202C'
                if element.tag == '{http://www.tei-c.org/ns/1.0}composer':
                    to_print = 1
                    str_to_print = u'\u202B' "שם המלחין:     " u'\u202C'
                if element.tag == '{http://www.tei-c.org/ns/1.0}album':
                    to_print = 1
                    str_to_print = u'\u202B' "שם האלבום:     " u'\u202C'
                str_to_print = str_to_print + '%30s' % element.text
                if to_print == 1:
                    print(str_to_print)
        print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
    print("")


def print_most_n_repeated_words(n):
    len_to_print = min(n, our_song_word_vector.__len__()-1)
    words_sorted_by_value = sorted(our_song_word_vector.items(), key=lambda kv: kv[1])
    print("print most " + str(len_to_print) + " repeated words: ")
    sys.stdout.flush()
    words_sorted_by_value.reverse()
    for i in range(0, len_to_print):
        print(u'\u202B' + str(i+1) + ": " + '%10s' % words_sorted_by_value[i][1].__str__() + " פעמים " + '%10s' % words_sorted_by_value[i][0].__str__() + u'\u202C')
        sys.stdout.flush()


# print("The Start time is:               " + datetime.datetime.now().__str__())
# print("read document start is:          " + datetime.datetime.now().__str__())
read_document()
# print("read document end is:            " + datetime.datetime.now().__str__())
# print("read dir start is:               " + datetime.datetime.now().__str__())
read_dir()
# print("read dir end is:                 " + datetime.datetime.now().__str__())
# print("printing hash start is:          " + datetime.datetime.now().__str__())
# print_songs_word_counter_vector()
# print_our_song_word_vector()
# print_hash_all_songs_to_his_words_vector()
# print("printing hash end is:            " + datetime.datetime.now().__str__())
# print("\nmeta data start is:              " + datetime.datetime.now().__str__())
print_meta_data()
print_most_n_repeated_words(1500)
# print("\nmeta data end is:                " + datetime.datetime.now().__str__())
# print("The End")
