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
sum_numbers(4, 5)
print(sums + [4])

