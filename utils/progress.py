import os

from utils.input_output import read_file, write_file


def read_progress_file():
    if os.path.exists('progress.txt') == False:
        res = ["results.json -1"]
        write_progress_file(res)
    else:
        res = read_file("progress.txt")
        if len(res) == 0:  # empty file
            res = ["results.json -1"]
            write_progress_file(res)

    return res


def update_progress_bar(filename, id_num):
    res = read_progress_file()

    for i, r in enumerate(res):
        t = r.split(" ")
        if t[0] == filename:
            res[i] = "{} {}".format(filename, id_num)

    write_progress_file(res)


def get_progress_value(filename):
    res = read_progress_file()

    for r in res:
        t = r.split(" ")
        if t[0] == filename:
            return int(t[1])

    return -1


def write_progress_file(res):
    write_file("progress.txt", res)
