# for i in range(10):
#   j = 0
#   while j < 3:
#     if j == 2:
#       break
#     print(j, end=', ')

#     j+=1

# string = "2-10-test-file.txt"
# print(string.split('.')[0])

# print(int(float('7.0430144e07')))

# for i in range(10):
#   if i == 4:
#     continue
#   elif i % 2 == 0:
#     print('found even number')
#   print(i)
# def convert(n):
#   return int(n)


# array = ['1', '2']
# converted = []
# for n in array:
#   converted.append(int(n))

# print(converted)

import os
import csv

metadata_columns = ['scan number', 'MS Level', 'Time',
                    'Polarity', 'SID', 'MS2 precursor', 'HCD energy', 'tic']

path = '/Users/kristinamiller/Documents/Freelancing/Genentech/first-project/automated-file-parser/new_auto_folder1'

try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)

os.chdir(path)

outputCSV = 'test-file.csv'

with open(outputCSV, 'w') as new_csv:
    csv_writer = csv.writer(new_csv, delimiter=',')
    csv_writer.writerow(metadata_columns)
