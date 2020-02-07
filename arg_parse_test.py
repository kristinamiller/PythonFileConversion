import argparse


def halve(num):
    return num / 2


def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument('num', type=int, help='the number you wish to halve')

    args = parser.parse_args()

    result = halve(args.num)
    print('half of ' + str(args.num) + ' is ' + str(result))

if __name__ == '__main__':
    Main()