import os
import csv

cur_time = os.stat('test.py').st_atime

# finds the folder I'm reading from and puts filenames into array.
file_list = (os.listdir('/Users/kristinamiller/Documents/Freelancing/Genentech/first-project/test-read-folder'))
print(file_list)

# gets inside the folder I'm reading from.
os.chdir('/Users/kristinamiller/Documents/Freelancing/Genentech/first-project/test-read-folder')

outputColumns = ['ID', 'MS Level', 'Time',
                 'scan number', 'Polarity', 'SID', 'MS2 precursor', 'HCD energy', 'tic']
searchStrings = ['cvParam: ms level,', 'cvParam: total ion current,']
rows = []
# guide: [columnHead, searchString, linePlacement, followsCharacter, dataType]
outputPairs = [
  ['ID', ''],
  ['MS Level', 'cvParam: ms level,', 'same_line', ','],
  ['Time', 'cvParam: time array, minute', 'next_line', ']', 'array'],
  ['scan number', 'id: controllerType=0 controllerNumber=1 scan=', 'same_line', '='],
  ['Polarity', 'cvParam: positive scan', 'positive', ':'],
  ['SID', ''],
  ['MS2 precursor', ''],
  ['HCD energy', ''],
  ['tic', 'cvParam: total ion current,', 'same_line', ',']
]

columnNames = []
searchStrings = []

for pair in outputPairs:






for filename in file_list:
  if filename.find('.txt') > -1:
    with open(filename, 'r') as rf:
      lines = rf.readlines()
      row = []
      i = 0
      while i < len(searchStrings):
        for line in lines:
          if line.find(searchStrings[i]) > -1:
            outputValue = [line[line.find(',') + 2:].strip()]
            row += outputValue
        i += 1
    rows.append(row)

print(rows)


outputCSV = 'output' + str(round(cur_time)) + '.csv'

with open(outputCSV, 'w') as new_csv:
  csv_writer = csv.writer(new_csv, delimiter=',')
  csv_writer.writerow(outputColumns)

  for row in rows:
    csv_writer.writerow(row)
