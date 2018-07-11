import codecs
from sys import argv
import os
from os.path import join
from math import log
import xml.etree.ElementTree as ET
lyrics_path = argv[1]
tagged_dir = argv[2]
xml_dir = argv[3]
our_song_word_vector = {}
map_song_words = {}
word_counter_vector = {}
song_path_map = {}

Parts_of_speech_structure = ["verb", "noun", "adverb", "adjective"]
b = 0.75
k = 1.5
log_base = 2


def delete_ending(last_word_path):
    if last_word_path.endswith("_Chorus.txt"):
        return last_word_path[:-11]
    if last_word_path.endswith("_Lyrics.txt"):
        return last_word_path[:-11]
    return last_word_path


def get_file_name(file_path):
    path_as_list = file_path.split('\\')
    last_word_with_ending = path_as_list[-1]
    last = delete_ending(last_word_with_ending)
    return last


def read_file(file_path, is_our_song):
    file_name = get_file_name(file_path)
    if not is_our_song:
        song_path_map[file_name] = file_path
    else:
        file_name = file_name[:file_name.index(".")]
    if file_name not in map_song_words:
        map_song_words[file_name] = {}
        word_counter_vector[file_name] = 0
    word_vector = map_song_words[file_name]
    size = word_counter_vector[file_name]

    for line in codecs.open(file_path, "r", "utf8"):
        columns = line.split(" ")
        if len(columns) > 4 and columns[4] in Parts_of_speech_structure:
            word = columns[2]
            size += 1
            if is_our_song:
                if word in our_song_word_vector:
                    our_song_word_vector[word] += 1
                    word_vector[word] += 1
                else:
                    our_song_word_vector[word] = 1
                    word_vector[word] = 1
            else:
                if word in word_vector:
                    word_vector[word] += 1
                else:
                    word_vector[word] = 1
                if word in our_song_word_vector:
                    our_song_word_vector[word] += 1
        word_counter_vector[file_name] = size


def read_dir():
    for path, directors, files in os.walk(tagged_dir):
        for file in files:
            if file == '.DS_Store':
                continue
            read_file(join(path, file), 0)


def read_our_song():
    read_file(lyrics_path, 1)


def df(word):
    if word in word_counter_vector:
        return word_counter_vector[word]
    return 1


def c(word, dictionary):
    return map_song_words[dictionary][word]


def average_file_length():
    key = "key_for_avg_songs"
    if key not in word_counter_vector:
        sums = 0
        for size in word_counter_vector.values():
            sums += size
        sums /= len(word_counter_vector)
        word_counter_vector[key] = sums
    return word_counter_vector[key]


def tf(word, dictionary):
    return c(word, dictionary) * (k + 1) / \
           (c(word, dictionary) + (k * (1 - b +
                                        (b * word_counter_vector[dictionary] / average_file_length()))))


def idf(word):
    return log((len(word_counter_vector) + 1) / df(word), b)


def sim(entry, document):
    sum_sim = 0
    for word_i in map_song_words[entry]:
        if word_i in map_song_words[document]:
            sum_sim += (tf(word_i, entry) * tf(word_i, document) * idf(word_i))
    return sum_sim


def similar_songs():
    songs_similarity = []
    song_name_with_txt = get_file_name(lyrics_path)
    song_name = song_name_with_txt[:song_name_with_txt.index(".")]
    for entry in map_song_words:  # changed till here!!
        if entry != song_name:
            songs_similarity.append((entry, sim(entry, song_name)))
    songs_similarity.sort(key=lambda x: x[1])
    return songs_similarity


def change_to_xml_path(song_name):
    song_address = song_path_map[song_name]
    song = song_address.replace(tagged_dir, xml_dir, 1)
    song = delete_ending(song)
    song += ".xml"
    return song


def print_similar_meta_data():
    similarity_matrix = similar_songs()
    for i in range(1, 11):
        print(str(i) + ":  " + "Song Matching Score: " + '%20s' % str(similarity_matrix[i][1]))
        song = change_to_xml_path(similarity_matrix[i][0])
        kind_of_tree = ET.parse(song)
        base_node = kind_of_tree.getroot()
        for elem in base_node.iter():
            if elem.tag != "" and elem.text != " " and elem.text != "missing" and elem.text != "\n":
                if elem.tag == '{http://www.tei-c.org/ns/1.0}title':
                    print("Song Name:           "+'%30s' % elem.text)
                elif elem.tag == '{http://www.tei-c.org/ns/1.0}singer':
                    print("Performer Name:      "+'%30s' % elem.text)
                elif elem.tag == '{http://www.tei-c.org/ns/1.0}writer':
                    print("Writer Name:         "+'%30s' % elem.text)
                elif elem.tag == '{http://www.tei-c.org/ns/1.0}composer':
                    print("Composer Name:       "+'%30s' % elem.text)
                elif elem.tag == '{http://www.tei-c.org/ns/1.0}album':
                    print("Album Name:          "+'%30s' % elem.text)
        print("")
    print("")


def print_most_n_repeated_words():
    sort_repetition = sorted(our_song_word_vector.items(), key=lambda x: x[1], reverse=True)
    print("Word Repetition: ")
    for i in range(0, our_song_word_vector.__len__() - 1):
        print(str(i + 1) + ": " + '%10s' % sort_repetition[i][1] + " times " + '%10s' %
              sort_repetition[i][0])


read_our_song()
read_dir()
print_most_n_repeated_words()
print_similar_meta_data()

