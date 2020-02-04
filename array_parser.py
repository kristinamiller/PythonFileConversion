import os
import csv


def parse_input(inputfolder):
    cur_time = os.stat('test.py').st_atime

    # # finds the folder I'm reading from and puts filenames into array.
    # file_list = (os.listdir(
    #     '/Users/kristinamiller/Documents/Freelancing/Genentech/first-project/test-read-folder'))
    # # gets inside the folder I'm reading from.
    # os.chdir(
    #     '/Users/kristinamiller/Documents/Freelancing/Genentech/first-project/test-read-folder')

    file_list = (os.listdir(inputfolder))
    os.chdir(inputfolder)


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
        if filename.find('.txt') > -1:
            with open(filename, 'r') as rf:
                lines = rf.readlines()
                i = 0
                while i < len(lines):
                    index = lines[i].find(searchStrings[0])
                    if index > -1:
                        scanNumber = lines[i][index +
                                              len(searchStrings[0]):].strip()
                    elif lines[i].find(searchStrings[1]) > -1:
                        array1 = lines[i+1].strip().split(" ")[2:]
                    elif lines[i].find(searchStrings[2]) > -1:
                        array2 = lines[i+1].strip().split(" ")[2:]
                    i += 1
            j = 0
            while j < len(array1):
              if array2[j] != "0":
                  rows.append([scanNumber, array1[j], array2[j]])
              j += 1

    outputCSV = 'unidec_output' + str(round(cur_time)) + '.csv'

    with open(outputCSV, 'w') as new_csv:
        csv_writer = csv.writer(new_csv, delimiter=',')
        csv_writer.writerow(outputColumns)

        for row in rows:
            csv_writer.writerow(row)
    print('success')

def main():
  inputfolder = input('enter path for folder containing input files:\n')

  parse_input(inputfolder)


main()
# print(rows[:5])
