import sys
from os import path as osp
import argparse

INPUT_FOLDER = "input"


def read_file(file_name):
    path = osp.join(INPUT_FOLDER, file_name)
    with open(path, "r") as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    return lines


def convert_to(cls, iterable):
    if cls == int:
        result = list(map(lambda x: cls(x) if x != "" else None, iterable))
    return result


def day_01(task=1):

    def get_max_of_n(array, n):
        result = 0
        for _ in range(n):
            result += max(array)
            array[array.index(max(array))] = 0
        return result

    input_data = read_file("input_01.txt")
    input_data = convert_to(int, input_data)
    energy_list = []
    buffer = 0
    for snack in input_data:
        if snack:
            buffer += snack
        else:
            energy_list.append(buffer)
            buffer = 0

    n = 1 if task == 1 else 3
    return get_max_of_n(energy_list, n)


def day_02(task):

    def calc_round(code):
        decode_map = {"A": 1,  # rock
                      "B": 2,  # paper
                      "C": 3,  # scissors
                      "X": 1,  # rock
                      "Y": 2,  # paper
                      "Z": 3,  # scissors
                      }
        elfs_sign = decode_map[code[0].upper()]
        my_sign = decode_map[code[2].upper()]

        return my_sign + ((my_sign-elfs_sign + 1) % 3)*3

    input_data = read_file("input_02.txt")
    score = 0
    for game in input_data:
        score += calc_round(game)

    return score


def main(raw_args):

    print('Welcome to the Advent of Code in 2022')
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--day', type=int, required=True, help='on the day you are trying to help Santa')
    parser.add_argument('-t', '--task', type=int, default=1, help='task of the day: 1 or 2')
    args = parser.parse_args(raw_args)
    print(f'Day:{args.day:3}, Task:{args.task:2}')

    day_map = {
        1: day_01,
        2: day_02,
    }

    answer = day_map[args.day](args.task)
    print(answer)


if __name__ == '__main__':
    main(sys.argv[1:])