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

for i in range(10):
  if i == 4:
    continue
  elif i % 2 == 0:
    print('found even number')
  print(i)