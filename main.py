import sys
from os import path as osp
import argparse
import string

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
        decode_map = {"rock": 1,
                      "paper": 2,
                      "scissors": 3,
                      }
        elfs_sign = decode_map[code[0]]
        my_sign = decode_map[code[1]]

        return my_sign + ((my_sign-elfs_sign + 1) % 3)*3

    def translate_data(data, task):
        decode_map = {"A": "rock", "B": "paper", "C": "scissors",
                      "X": "rock", "Y": "paper", "Z": "scissors"}
        win_lose_table = {
            # lose
            "X": {"A": "C", "B": "A", "C": "B"},
            # draw
            "Y": {"A": "A", "B": "B", "C": "C"},
            # win
            "Z": {"A": "B", "B": "C", "C": "A"}
            }

        temp_result = []
        if task == 2:
            for elem in data:
                temp_result.append((elem[0], " ", win_lose_table[elem[2]][elem[0]]))
        else:
            temp_result = data
        result = []
        for elem in temp_result:
            result.append([decode_map[elem[0]], decode_map[elem[2]]])
        return result

    input_data = read_file("input_02.txt")
    score = 0
    translated_data = translate_data(data=input_data, task=task)

    for game in translated_data:
        score += calc_round(game)

    return score


def day_03(task):
    alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)

    def get_priority(obj):
        nonlocal alphabet
        return alphabet.index(obj) + 1

    input_data = read_file("input_03.txt")
    backpacks = []
    for line in input_data:
        backpacks.append([line[:len(line)//2], line[len(line)//2:]])
    common_objects = []
    for bp in backpacks:
        common_objects.append(list(set(bp[0]).intersection(set(bp[1])))[0])  # Yikes
    priority_sum = 0
    for obj in common_objects:
        priority_sum += get_priority(obj)

    return priority_sum



def day_04(task):
    pass


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
        3: day_03,
        4: day_04
    }

    answer = day_map[args.day](args.task)
    print(answer)


if __name__ == '__main__':
    main(sys.argv[1:])