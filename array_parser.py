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
    unidec_rows = []
    metadata_row = []

    # we're going to create two arrays from each of the inputs.

    for filename in file_list:
        if filename.find('easiest_file_single_scan_testfile-1') > -1:
            with open(filename, 'r') as rf:
                lines = rf.readlines()
                i = 0
                mid_scan = False
                while i < len(lines):
                    if not mid_scan:
                        new_scan_index = lines[i].find(searchStrings[0])
                        if new_scan_index > -1:
                            mid_scan = True
                            scan_number = lines[i][new_scan_index +
                                                   len(searchStrings[0]):].strip()
                            write_metadata(scan_number, lines[i:i+143])
                    else:
                        if lines[i].find(searchStrings[1]) > -1:
                            mz_array = lines[i+1].strip().split(" ")[2:]
                        elif lines[i].find(searchStrings[2]) > -1:
                            intensity_array = lines[i+1].strip().split(" ")[2:]
                            unidec_rows += write_unidec_rows(
                                scan_number, mz_array, intensity_array)
                            mid_scan = False
                    i += 1

            # writes unidec file
            outputCSV = '3unidec_output' + str(round(cur_time)) + '.csv'

            with open(outputCSV, 'w') as new_csv:
                csv_writer = csv.writer(new_csv, delimiter=',')
                csv_writer.writerow(outputColumns)

                for row in unidec_rows:
                    csv_writer.writerow(row)
            # print('success')
    # print(unidec_rows)


def write_unidec_rows(scan_number, mz_array, intensity_array):
    rows = []
    i = 0
    while i < len(mz_array):
        if intensity_array[i] != "0":
            rows.append([scan_number, mz_array[i], intensity_array[i]])
        i += 1
    return rows


def write_metadata(scan_number, lines):
    search_dict = {
        'MS Level': ['cvParam: ms level,', ','],
        # 'Time': ['cvParam: time array, minute', 'next_line', ']', 'array'],
        'Polarity': ['cvParam: positive scan', ':', " "],
        'SID': ['sid=', 'd=', " "],
        'MS2 precursor': ['selected ion m/z,', ',', ','],
        'HCD energy': ['collision energy,', ',', ','],
        'tic': ['cvParam: total ion current,', ',', ' ']
    }
    output_dict = {}

    for column_name, search_inst in search_dict.items():
        # output_dict[column_name] = search_inst
        i = 0
        while i < len(lines):
            search_string_idx = lines[i].find(search_inst[0])
            if search_string_idx > -1:
                start_idx = lines[i].find(search_inst[1]) + 2
                output_value = lines[i][start_idx:].strip();
                # end_idx = output_value.find(search_inst[2])
                # if end_idx > -1:
                #     output_value = output_value[:end_idx - 1]    
                output_dict[column_name] = output_value
            i += 1

    print(output_dict)

def main():
    inputfolder = input('enter path for folder containing input files:\n')

    parse_input(
        '/Users/kristinamiller/Documents/Freelancing/Genentech/first-project/test-read-folder')


main()

string = '/Users/kristinamiller/Documents/Freelancing/Genentech/first-project/test-read-folder'


# pass the next 150 lines to a helper method that will find the other data.
