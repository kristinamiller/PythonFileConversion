import argparse


def halve(num):
    return num / 2


def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num', type=int, help='the number you wish to halve')
    parser.add_argument('string', type=str, help='the string you wish to split')

    args = parser.parse_args()

    result = args.string.split("l")
    print(result)
    # print('half of ' + str(args.num) + ' is ' + str(result))

if __name__ == '__main__':
    Main()