import os
import csv
import argparse

cur_time = os.stat('test.py').st_atime

metadata_dict = {
    'MS Level': ['cvParam: ms level,', ',', ','],
    'Time': ['cvParam: scan start time', ',', ','],
    'Polarity': ['cvParam: positive scan', ':', " "],
    'SID': ['sid=', 'd=', " "],
    'MS2 precursor': ['selected ion m/z,', ',', ','],
    'HCD energy': ['collision energy,', ',', ','],
    'tic': ['cvParam: total ion current,', ',', ' ']
}

metadata_columns = ['scan number', 'MS Level', 'Time',
                    'Polarity', 'SID', 'MS2 precursor', 'HCD energy', 'tic']

unidec_dict = {
    'scan': 'id: controllerType=0 controllerNumber=1 scan=',
    'm/z': 'cvParam: m/z array, m/z',
    'intensity': 'cvParam: intensity array, number of detector counts'
}


def parse_input(inputfolder, conditionals):
    file_list = (os.listdir(inputfolder))
    os.chdir(inputfolder)

    for filename in file_list:
        if is_valid_file(filename):
            read_file(filename, conditionals)


def is_valid_file(filename):
    if filename.find('2-13-test-file.txt') > -1:
        return True
    else:
        return False


def read_file(filename, conditionals):
    output = []
    unidec_rows = []
    metadata_row = []
    cur_hcd = 0

    with open(filename, 'r') as rf:
        lines = rf.readlines()
        i = 0
        mid_scan = False
        first_scan = True
        while i < len(lines):
            if not mid_scan:
                new_scan_index = lines[i].find(unidec_dict['scan'])
                if new_scan_index > -1:  # we know we've hit a new scan
                    mid_scan = True
                    scan_number = lines[i][new_scan_index +
                                           len(unidec_dict['scan']):].strip()
                    if int(scan_number) < conditionals['scan_range'][0]:
                        mid_scan = False
                        i += 1
                        continue
                    if conditionals['scan_range'][1] != 0 and int(scan_number) > conditionals['scan_range'][1]:
                        mid_scan = False
                        i += 1
                        continue
                    metadata_row = write_metadata_row(
                        scan_number, lines[i:i+143])  # improve precision here
                    if int(float(metadata_row['tic'])) < conditionals['tic_min']:
                        mid_scan = False
                        i += 1
                        continue
                    if first_scan or (conditionals['hcd'] == 'true' and cur_hcd != metadata_row['HCD energy']):
                        unidec_csv = create_new_csv('unidec',
                                                    unidec_dict.keys(), filename, scan_number, metadata_row['HCD energy'], metadata_row['MS Level'])
                        metadata_csv = create_new_csv('metadata',
                                                      metadata_columns, filename, scan_number, metadata_row['HCD energy'], metadata_row['MS Level'])
                        first_scan = False
                    cur_hcd = metadata_row['HCD energy']
                    append_rows(metadata_csv, [metadata_row.values()])
            else:
                if lines[i].find(unidec_dict['m/z']) > -1:
                    mz_array = lines[i+1].strip().split(" ")[2:]
                elif lines[i].find(unidec_dict['intensity']) > -1:
                    intensity_array = lines[i+1].strip().split(" ")[2:]
                    unidec_rows += write_unidec_rows(
                        scan_number, mz_array, intensity_array)
                    mid_scan = False
                    append_rows(unidec_csv, unidec_rows)
                    unidec_rows = []
            i += 1

    print('success')


def append_rows(input_csv, rows):
    with open(input_csv, 'a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for row in rows:
            csv_writer.writerow(row)


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
    # once we find the item for a column it breaks out of the inner loop and starts looking for the next one.
    for column_name, search_inst in metadata_dict.items():
        i = 0
        while i < len(lines):
            search_string_idx = lines[i].find(search_inst[0])
            if search_string_idx > -1:
                start_idx = lines[i].find(search_inst[1]) + 2
                output_value = lines[i][start_idx:].strip()
                output_value = output_value.split(search_inst[2])[0]
                output_dict[column_name] = output_value
                break
            i += 1

    return(output_dict)


def create_new_csv(type, column_names, filename, scan_number, hcd_energy, ms_level):
    filename_trimmed = filename.split('.')[0]
    title_elements = ['27', filename_trimmed, scan_number,
                      hcd_energy, ms_level, type, str(round(cur_time)), '.csv']
    s = '_'
    outputCSV = s.join(title_elements)

    with open(outputCSV, 'w') as new_csv:
        csv_writer = csv.writer(new_csv, delimiter=',')
        csv_writer.writerow(column_names)

    return outputCSV


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, default='/Users/kristinamiller/Documents/Freelancing/Genentech/first-project/2-13-testing',
                        help='the folder to select files from')
    parser.add_argument('--hcd', type=str, default='false',
                        help='True or False to export to new file when HCD value changes')
    parser.add_argument('--tic_min', type=str, default='1e4',
                        help='the minimum value for the total ion current, below which scans will be excluded from the results')
    parser.add_argument('--scan_range', type=str, default='0-0',
                        help='min and max scan number to start and end with, e.g. 2-12. 0-0 will export all scans. 2-0 will start at 2 and go to the end.')
    args = parser.parse_args()
    scan_range = args.scan_range.split("-")
    scan_range_integers = []
    for n in scan_range:
        scan_range_integers.append(int(n))

    conditionals = {'hcd': args.hcd, 'tic_min': int(
        float(args.tic_min)), 'scan_range': scan_range_integers}
    parse_input(args.folder, conditionals)


if __name__ == '__main__':
    main()
