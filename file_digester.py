import os
import re

os.chdir('/Users/kristinamiller/Documents/Freelancing/Genentech/first-project/test-save-folder')

# looking for lines with more than 20 integers in it and excluding that from the output file.

# match = re.compile('\d{20}')
pattern = '\d{10}'
test = '1234.asdfasdfasdf 123412341234h 1234qw'
# pattern = '[a-zA-Z]{3}'

testArray = ['12344567123456783456789234', '123', 'abc']

# if re.search(pattern, test):
#   print(re.sub(pattern, '', test))
# else:
#   print('no match')

# going to only print out lines that contain some alphabetic character.


# with open('easiest_file_single_scan_testfile-1.txt', 'r') as rf:
#   with open('test_summary.txt', 'w') as wf:
#     i = 0
#     while i < 2:
#       for line in rf:
#         if re.search(pattern, line):
#           replaced = re.sub(pattern, '', line)
#           zeros = re.sub('0*', '', replaced)
#           zeros1 = re.sub(' . ', '', zeros)
#           zeros2 = re.sub(pattern, '', zeros1)
#           print(re.sub('\.{2}', '', zeros2))
#     i+=1

# cuts out the extraneous numbers and saves the output to the txt file I selected.
with open('single_MSlevel_multiplescans_testfile_2.txt', 'r') as rf:
    with open('test_summary.txt', 'w') as wf:
        for line in rf:
            if re.search('\d{6}', line):
              replaced = re.sub(' ', '', line)
              replaced1 = re.sub('\.', '', replaced)
              if re.search(pattern, replaced1):
                replaced2 = re.sub(pattern, '', replaced1)
                line = replaced2
            wf.write(line)
    wf.close()

# new idea: if we see a colon ':', print the 50 characters before and after it.

# with open('easiest_file_single_scan_testfile-1.txt', 'r') as rf:
#   with open('test_summary.txt', 'w') as wf:
#     i = 0
#     for line in rf:
#       line = line.strip()
#       index = line.find(':')
#       if index > -1:
#         print(line[(index - 20):(index + 60)])
