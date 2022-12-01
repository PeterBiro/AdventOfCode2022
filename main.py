from os import path as osp

INPUT_FOLDER = "input"


def read_file(file_name):
    path = osp.join(INPUT_FOLDER, file_name)
    with open(path, "r") as f:
        lines = f.readlines()
    lines = list(map(lambda x: x.strip(), lines))

    return lines


def convert_to(cls, iterable):
    if cls == int:
        result = list(map(lambda x: cls(x) if x != "" else None, iterable))
    return result


def day_01(task="task_1"):
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

    print(max(energy_list))


if __name__ == '__main__':
    day_01()