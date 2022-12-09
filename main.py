import sys
from os import path as osp
import argparse
import string
import re
from collections import deque

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

    def get_common(*args):
        common = set(args[0])
        for a in args:
            common = common.intersection(set(a))
        return list(common)[0]

    input_data = read_file("input_03.txt")

    backpacks = []
    if task == 1:
        for line in input_data:
            backpacks.append([line[:len(line)//2], line[len(line)//2:]])
    else:
        for i in range(0, len(input_data), 3):
            backpacks.append([input_data[i], input_data[i+1], input_data[i+2]])

    common_objects = []
    for bp in backpacks:
        common_objects.append(get_common(*bp))

    priority_sum = 0
    for obj in common_objects:
        priority_sum += get_priority(obj)

    return priority_sum


def day_04(task):

    def parse_input(lines):
        ret_val = []
        pattern = r"(\d*)-(\d*),(\d*)-(\d*)"
        for line in lines:
            x = re.search(pattern, line)
            ret_val.append([[int(x.group(1)), int(x.group(2))],
                            [int(x.group(3)), int(x.group(4))]])
        return ret_val

    def is_fully_intersect(a, b):
        return (a[0] <= b[0] and b[1] <= a[1]) or (b[0] <= a[0] and a[1] <= b[1])

    def is_overlap(a, b):
        return a[0] <= b[0] <= a[1] or b[0] <= a[0] <= b[1]

    def count_intersections(intervals):
        counter = 0
        for pair in intervals:
            if task == 1:
                if is_fully_intersect(*pair):
                    counter += 1
            else:
                if is_overlap(*pair):
                    counter += 1
        return counter

    input_data = read_file("input_04.txt")
    interval_pairs = parse_input(input_data)
    return count_intersections(interval_pairs)


def day_05(task):

    class Stack:
        def __init__(self, reverse):
            self.stack = []
            self.reverse = reverse

        def get_last_n(self, n):
            last_n = self.stack[-n:]
            if reverse:
                last_n.reverse()
            self.stack = self.stack[:-n]
            return last_n

        def put_on_stack(self, crates):
            self.stack.extend(crates)

    def parse_input(data_file, reverse):
        is_header = True
        moves = []
        stacks = [None]
        header = []
        stack_nr_pattern = r".*(\d+)$"
        move_pattern = r"move (\d+) from (\d+) to (\d+)"
        stack_nr = 0
        for line in data_file:
            if is_header:
                m = re.match(stack_nr_pattern, line)
                if m:
                    stack_nr = int(m.group(1))
                    is_header = False
                else:
                    header.append(line)
            else:
                m = re.match(move_pattern, line)
                if not m:
                    continue
                moves.append({"move": int(m.group(1)),
                              "from": int(m.group(2)),
                              "to":   int(m.group(3))
                              })
        for _ in range(stack_nr):
            stacks.append(Stack(reverse))
        for line in header[::-1]:
            for i, char in enumerate(line[1::4], 1):
                if char != " ":
                    stacks[i].put_on_stack([char])

        return stacks, moves

    def rearrange(stacks, moves):
        for move in moves:
            crates = stacks[move["from"]].get_last_n(move["move"])
            stacks[move["to"]].put_on_stack(crates)
        return stacks  # not necessary

    input_data = read_file("input_05.txt")
    reverse = True if task == 1 else False
    stacks, moves = parse_input(input_data, reverse)
    rearrange(stacks, moves)
    result = ""
    for i in range(1, len(stacks)):
        result += stacks[i].get_last_n(1)[0]

    return result


def day_06(task):
    class Seeker:
        def __init__(self):
            self.mask = []
            self.index = 0

        def is_unique(self, new):
            self.mask.append(new)
            self.index += 1
            if len(self.mask) == 5:
                self.mask.pop(0)
            return len(set(self.mask)) == 4

        def show_mask(self):
            return "".join(self.mask)

    input_data = read_file("input_06.txt")
    data = input_data[0]
    seeker = Seeker()
    for char in data:
        if seeker.is_unique(char):
            break
    return seeker.index


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
        4: day_04,
        5: day_05,
        6: day_06
    }

    answer = day_map[args.day](args.task)
    print(answer)


if __name__ == '__main__':
    main(sys.argv[1:])