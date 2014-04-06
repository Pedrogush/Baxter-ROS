#s = raw_input()
#try:
#    i = int(s)
#except ValueError:
#    i = 0
a = 0
b = 0
Means = [[[[0 for l in range(3)] for i in range (3)]for j in range(3)] for k in range(3)]
Means2 = [[[[0 for l in range(3)] for i in range (3)]for j in range(3)] for k in range(3)]
Means2[0][0][0][1] = 1
Means2[0][0][1][0] = 2
Means2[0][1][0][0] = 3
Means2[1][0][0][0] = 4
#while a<3:
#    while b<3:
 #   		Means[a][b]=[6]*3
#		b = b+1
#    a = a+1

print repr(Means)
print repr(Means2)
