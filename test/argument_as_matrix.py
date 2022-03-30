
a = 1
b = 2
print("Test for print (", a, ",", b, ") num with word")

for i in range(5):
    for j in range(6):
        x = i+j
        print('{:03d}'.format(x), end=' ')
    print('')