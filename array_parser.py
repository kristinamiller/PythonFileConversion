import os
import csv

cur_time = os.stat('test.py').st_atime

# finds the folder I'm reading from and puts filenames into array.
file_list = (os.listdir(
    '/Users/kristinamiller/Documents/Freelancing/Genentech/first-project/test-read-folder'))
# gets inside the folder I'm reading from.
os.chdir('/Users/kristinamiller/Documents/Freelancing/Genentech/first-project/test-read-folder')

outputColumns = ['scan', 'm/z', 'intensity']
searchStrings = [
    'id: controllerType=0 controllerNumber=1 scan=', 
    'cvParam: m/z array, m/z',
    'cvParam: intensity array, number of detector counts'
    ]

output = []
rows = []

# we're going to create two arrays from each of the inputs.

for filename in file_list:
  if filename.find('easiest_file_single_scan_testfile-1') > -1:
    with open(filename, 'r') as rf:
      lines = rf.readlines()
      i = 0
      while i < len(lines):
        index = lines[i].find(searchStrings[0])
        if index > -1:
          scanNumber = lines[i][index+len(searchStrings[0]):].strip()
          output.append(scanNumber)
        elif lines[i].find(searchStrings[1]) > -1:
          array1 = lines[i+1].strip().split(" ")[2:]
          # num_items = int(array1[0][1:-1])
        elif lines[i].find(searchStrings[2]) > -1:
          array2 = lines[i+1].strip().split(" ")[2:]
        i+=1
    j = 0
    while j < len(array1):
      rows.append([scanNumber, array1[j], array2[j]])
      j += 1

# print(array2[:5])
# print(file_list)



outputCSV = 'unidec_output' + str(round(cur_time)) + '.csv'

with open(outputCSV, 'w') as new_csv:
  csv_writer = csv.writer(new_csv, delimiter=',')
  csv_writer.writerow(outputColumns)

  for row in rows:
    csv_writer.writerow(row)


# print(rows[:5])
