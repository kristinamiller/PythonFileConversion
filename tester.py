import os
import csv

# x = input('enter first number')
# y = input('enter second number')
# z = int(x) + int(y)
# print(z)

sums = []

def sum_numbers(a,b):
  sums.append(a + b)

def avg_numbers(sum):
  return sum / 2

# print(avg_numbers(sum_numbers(2,3)))
# sum_numbers(4, 5)
# print(sums + [4])

# search_dict = {
#     'MS Level': ['cvParam: ms level,', 'same_line', ','],
#     # 'Time': ['cvParam: time array, minute', 'next_line', ']', 'array'],
#      'Polarity': ['cvParam: positive scan', 'positive', ':'],
#     'SID': ['sid=', 'same_line', '='],
#         'MS2 precursor': ['selected ion m/z,', 'same_line', ','],
#         'HCD energy': ['collision energy,', 'same_line', ','],
#         'tic': ['cvParam: total ion current,', 'same_line', ',']
#     }

# for column_name in search_dict:
#     print(search_dict[column_name][0])


cur_time = os.stat('test.py').st_atime

outputColumns = ['ID', 'MS Level', 'Time',
                 'scan number', 'Polarity', 'SID', 'MS2 precursor', 'HCD energy', 'tic']

def create_new_csv(column_names, type):
    outputCSV = '2' + type + str(round(cur_time)) + '.csv'

    with open(outputCSV, 'w') as new_csv:
        csv_writer = csv.writer(new_csv, delimiter=',')
        csv_writer.writerow(column_names)

    return outputCSV


def main():
  new_csv = create_new_csv(outputColumns, 'metadata')
  print(new_csv)


main()