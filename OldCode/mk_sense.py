#!/usr/bin/env python
# should output a file that gives the difference between two different .sense files, the intention is to build a database, from 0 to 1000 grams load, each file being compared to the 0 load file, that allows us to develop linear approximations for the joints, which in turn will let us guess the weight. Next step will be, if weight is accurate enough, to work with different geometries.
import os
c1=0
invert=1
Harm_N1 = [0]*17
Harm_NLest1 = [0]*17
Harm_NHest1 = [0]*17
Harm_NR = [0]*17
nb = raw_input('state the name of the output file\n')
S = open('./resources/%s.impr' %nb, 'w')
while c1<2:
        c1 = c1+1
        num = {'number' : repr(c1)}
        na = raw_input('state the name of file {number} to be compared\n'.format(**num))
	size = os.path.getsize('./resources/%s.feel' %na)
	a= 0
	b= 0
	F = open('./resources/%s.feel' %na , 'r')
        V = [0]*3
	V[c1] = memoryview(repr(F.readlines()))
	numbercount = 0
	decimals = 1
	N_num = 0
	d = 0
	allocation = 0
	x=0
        invert = -invert
	while d<size+1:
	     d = d+1
	     if V[c1][d] == '.':
		allocation = allocation + 1
	Ef1 = [0] * allocation
        d=0
	while a<size+1:
	  
	  if V[c1][a] == '(':
	     startline = 1
	  if V[c1][a] == ',':
	     decimals = 1
	     numberpass = 1
	     N_num = N_num + 1
	  if V[c1][a] == '0':
	     c = float(V[c1][a])
	     Ef1[N_num] = Ef1[N_num] + decimals*c
	     decimals = decimals*0.1 
	     numbercount = numbercount+1
	  if V[c1][a] == '1':
	     c = float(V[c1][a])
	     Ef1[N_num] = Ef1[N_num] + decimals*c
	     decimals = decimals*0.1  
	     numbercount = numbercount+1 
	  if V[c1][a] == '2':
	     c = float(V[c1][a])
	     Ef1[N_num] = Ef1[N_num] + decimals*c
	     decimals = decimals*0.1 
	     numbercount = numbercount+1
	  if V[c1][a] == '3':
	     c = float(V[c1][a])
	     Ef1[N_num] = Ef1[N_num] + decimals*c
	     decimals = decimals*0.1 
	  if V[c1][a] == '4':
	     c = float(V[c1][a])
	     Ef1[N_num] = Ef1[N_num] + decimals*c  
	     decimals = decimals*0.1 
	     numbercount = numbercount+1
	  if V[c1][a] == '5':
	     c = float(V[c1][a])
	     Ef1[N_num] = Ef1[N_num] + decimals*c  
	     decimals = decimals*0.1 
	     numbercount = numbercount+1
	  if V[c1][a] == '6':
	     c = float(V[c1][a])
	     Ef1[N_num] = Ef1[N_num] + decimals*c  
	     decimals = decimals*0.1 
	     numbercount = numbercount+1
	  if V[c1][a] == '7':
	     c = float(V[c1][a])
	     Ef1[N_num] = Ef1[N_num] + decimals*c  
	     decimals = decimals*0.1 
	     numbercount = numbercount+1
	  if V[c1][a] == '8':
	     c = float(V[c1][a])
	     Ef1[N_num] = Ef1[N_num] + decimals*c  
	     numbercount = numbercount+1
	  if V[c1][a] == '9':
	     c = float(V[c1][a])
	     Ef1[N_num] = Ef1[N_num] + decimals*c 
	     decimals = decimals*0.1   
	     numbercount = numbercount+1
	  if V[c1][a] == '.':
	     if numbercount > 1:
		Ef1[N_num] = 10*Ef1[N_num]  
		decimals = 10*decimals 
	  if V[c1][a] == ' ':
	     numbercount = 0
	  if V[c1][a] == ')':
	     N_num = N_num + 1
	  a = a+1
	Harm_N = [0]*17
	Harm_D = [0]*17
	Harm_NLest = [100]*17
	Harm_NHest = [0]*17

        a=0
	i = 0
	while b<N_num:
	     Harm_N[x] = Harm_N[x] + Ef1[b]
	     Harm_D[x] = Harm_D[x] + 1
	     if Harm_NLest[x]>Ef1[b]:
		Harm_NLest[x] = Ef1[b]
	     if Harm_NHest[x]<Ef1[b]:
		Harm_NHest[x] = Ef1[b]
	     b=b+1
	     x=x+1
	     if x>16:
		x=0
        b=0


        S.write('The mean torque for each joint in file %s.feel is: \n' %na)
	while i <16:
	      i = i+1
	      Harm_NR[i] = Harm_N[i]/Harm_D[i]
	      print Harm_NR[i]
              S.write(repr(Harm_NR[i]))
              S.write('\n')
	i = 0

	print '\n'
        S.write('The highest recorded torque for each joint in file %s.feel is: \n' %na)
	while i <16:
	      i = i+1
	      print Harm_NHest[i]
              S.write(repr(Harm_NHest[i]))
              S.write('\n')
	i = 0

	print '\n'
        S.write('The lowest recorded torque for each joint in file %s.feel is: \n' %na)
	while i <16:
	      i = i+1
	      print Harm_NLest[i]
              S.write(repr(Harm_NLest[i]))
              S.write(' \n')
	i = 0
          
	print '\n'

        while i<16:
              Harm_N1[i] = Harm_N1[i]-Harm_NR[i]*invert
              Harm_NLest1[i] = Harm_NLest1[i]-Harm_NLest[i]*invert
              Harm_NHest1[i] = Harm_NHest1[i]-Harm_NHest[i]*invert 
              i = i+1 
        i=0
S.write('The difference between the mean torques in file 1 and file 2 is: \n')
while i<16:
      if Harm_N1[i]!=0:  
         print Harm_N1[i]
         S.write(repr(Harm_N1[i]))
         S.write(' \n')
      i = i+1
i=0

print '\n'
S.write('The difference between the lowest recorded torques in file 1 and file 2 is: \n')
while i<16:
      if Harm_NLest1[i]!=0:  
         print Harm_NLest1[i]
         S.write(repr(Harm_NLest1[i]))
         S.write(' \n')
      i = i+1
i=0

print '\n'
S.write('The difference between the highest recorded torques in file 1 and file 2 is: \n')
while i<16:
      if Harm_NHest1[i]!=0:      
         print Harm_NHest1[i]
         S.write(repr(Harm_NHest1[i]))
         S.write(' \n')
      i = i+1
i=0

