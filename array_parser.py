import os
import csv

cur_time = os.stat('test.py').st_atime

metadata_dict = {
    'MS Level': ['cvParam: ms level,', ',', ','],
    # 'Time': ['cvParam: time array, minute', 'next_line', ']', 'array'],
    'Polarity': ['cvParam: positive scan', ':', " "],
    'SID': ['sid=', 'd=', " "],
    'MS2 precursor': ['selected ion m/z,', ',', ','],
    'HCD energy': ['collision energy,', ',', ','],
    'tic': ['cvParam: total ion current,', ',', ' ']
}

metadata_columns = ['scan number', 'MS Level', 'Polarity', 'SID', 'MS2 precursor', 'HCD energy', 'tic']

unidec_dict = {
    'scan': 'id: controllerType=0 controllerNumber=1 scan=',
    'm/z': 'cvParam: m/z array, m/z',
    'intensity': 'cvParam: intensity array, number of detector counts'
}


def parse_input(inputfolder):
    file_list = (os.listdir(inputfolder))
    os.chdir(inputfolder)

    for filename in file_list:
        if is_valid_file(filename):
            read_file(filename)
    # raise RuntimeError('this is an error because I say so')


def is_valid_file(filename):
    # if filename.find('single_MSlevel_multiplescans_testfile_2') > -1:
    if filename.find('easiest_file_single_scan_testfile-1') > -1:
        return True
    else:
        return False


def read_file(filename):
    output = []
    unidec_rows = []
    metadata_row = []
    unidec_csv = create_new_csv(unidec_dict.keys(), 'unidec')
    metadata_csv = create_new_csv(
        metadata_columns, 'metadata')

    with open(filename, 'r') as rf:
        lines = rf.readlines()
        i = 0
        mid_scan = False
        while i < len(lines):
            if not mid_scan:
                new_scan_index = lines[i].find(unidec_dict['scan'])
                if new_scan_index > -1:
                    mid_scan = True
                    scan_number = lines[i][new_scan_index +
                                           len(unidec_dict['scan']):].strip()
                    metadata_row = write_metadata_row(
                        scan_number, lines[i:i+143])
                    # append_rows(metadata_csv, [metadata_row])
                    with open(metadata_csv, 'a') as metadata_csv:
                        csv_writer = csv.writer(metadata_csv, delimiter=',')
                        csv_writer.writerow(metadata_row.values())
            else:
                if lines[i].find(unidec_dict['m/z']) > -1:
                    mz_array = lines[i+1].strip().split(" ")[2:]
                elif lines[i].find(unidec_dict['intensity']) > -1:
                    intensity_array = lines[i+1].strip().split(" ")[2:]
                    unidec_rows += write_unidec_rows(
                        scan_number, mz_array, intensity_array)
                    mid_scan = False
                    # append_rows(unidec_csv, unidec_rows)
                    with open(unidec_csv, 'a') as unidec_csv:
                        csv_writer = csv.writer(unidec_csv, delimiter=',')
                        for row in unidec_rows:
                            csv_writer.writerow(row)
            i += 1

    print('success')


def write_unidec_rows(scan_number, mz_array, intensity_array):
    rows = []
    i = 0
    while i < len(mz_array):
        if intensity_array[i] != "0":
            rows.append([scan_number, mz_array[i], intensity_array[i]])
        i += 1
    return rows


def write_metadata_row(scan_number, lines):
    output_dict = {'scan number': scan_number}

    for column_name, search_inst in metadata_dict.items():
        i = 0
        while i < len(lines):
            search_string_idx = lines[i].find(search_inst[0])
            if search_string_idx > -1:
                start_idx = lines[i].find(search_inst[1]) + 2
                output_value = lines[i][start_idx:].strip()
                output_value = output_value.split(search_inst[2])[0]
                output_dict[column_name] = output_value
            i += 1

    return(output_dict)

def append_rows(csv, rows):
    with open(csv, 'a') as csv:
        csv_writer = csv.writer(csv, delimiter=',')
        for row in rows:
            csv_writer.writerow(row)


def create_new_csv(column_names, type):
    outputCSV = '8' + type + str(round(cur_time)) + '.csv'

    with open(outputCSV, 'w') as new_csv:
        csv_writer = csv.writer(new_csv, delimiter=',')
        csv_writer.writerow(column_names)

    return outputCSV


def main():
    inputfolder = input('enter path for folder containing input files:\n')

    parse_input(
        '/Users/kristinamiller/Documents/Freelancing/Genentech/first-project/test-read-folder')


if __name__ == '__main__':
    main()
