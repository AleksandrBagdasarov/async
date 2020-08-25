one = []
two = [2]

x = one or two
print('ex1: ', x)
print('\n')

string = 'abc'
ten = 10
print('ex2: ', string or ten)
print('ex2: ', ten or string)
print('\n')
string = ''
ten = 10
print('ex3: ', string or ten)
print('ex3: ', ten or string)
print('\n')