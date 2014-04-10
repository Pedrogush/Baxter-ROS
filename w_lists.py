from __future__ import division
import mk_sense


# NOW WITH PROPER IMPLEMENTATIONS, PURPOSE IS TO TAKE A SET OF .feel FILES AND CREATE A MUCH LARGER SET OF .impr FILES FROM THE COMPARISON BETWEEN EACH 2 INDIVIDUAL .feel FILES
# Needs to be looked at, comparison looks wobly at best, maybe just a question of having the list shift back one position
samples = raw_input('input number of samples to be read\n')
samples = int(samples)
EReader = [0]*samples
a=0
b=0
imp_t = [0]*(samples*samples)
nb = raw_input('input .feel set root file names\n')
A = 0.0
flag = 0
while a<samples:
        EReader[a] = mk_sense.effort_reader(a, nb)
        EReader[a].allocation_def()
        EReader[a].read_file()
	EReader[a].calc_values_per_joint()
	for i in range(17):
		 EReader[a].Ef_Filter[i] = filter(lambda x: x!=0, EReader[a].Ef_Filter[i])
	EReader[a].Ef_Filter = filter(lambda x: x!=[], EReader[a].Ef_Filter)
        b = 0
        a = a+1
b=0
a=0
acc=0.1
while a<30:

#	EReader[a].get_mean_effort_per_joint()
	while b<samples:
                if b>a:
			imp_t[samples*a+b] = mk_sense.impression_taker(a,b, nb)
			EReader[a].print_lowest_recorded_torque(a, imp_t[samples*a+b])
			EReader[a].print_highest_recorded_torque(a, imp_t[samples*a+b])
			EReader[a].print_mean_effort_per_joint(a, imp_t[samples*a+b])
			EReader[a].get_differences_in_torque(EReader[b])
			EReader[a].print_difference_between_mean_torques(imp_t[samples*a+b])
			EReader[a].print_difference_between_lowest_torques(imp_t[samples*a+b])
			EReader[a].print_difference_between_highest_torques(imp_t[samples*a+b])
			EReader[a].clear()
			imp_t[samples*a+b].S.close()
		b=b+1
        b = 0
	a = a+1
def rep_filter(listf, acc):
	l = filter(lambda x: (sum(listf)/len(listf))-acc<x<(sum(listf)/len(listf))+acc, listf)
	return l
# acc = 0.02 yields good results most of the time, must write code to iterate and try different values of acc
for i in range(samples):
	for j in range(14):
		acc = 0.0
		while flag==0:
			EReader[i].Ef_Filter_Clone[j] = EReader[i].Ef_Filter[j]
			EReader[i].Ef_Filter_Clone[j] = rep_filter(EReader[i].Ef_Filter_Clone[j], acc)
			if len(EReader[i].Ef_Filter_Clone[j])>0:
					flag = 1
			if len(EReader[i].Ef_Filter_Clone[j])==0:
					acc = acc+0.01
		flag=0
for m in range(14):
	for i in range(samples):
		print sum(EReader[i].Ef_Filter_Clone[m])/float(len(EReader[i].Ef_Filter_Clone[m]))
print '\n'
	
print acc

#	for i in range(len(EReader[i].Ef_Filter[0])-1):
#		A = A + EReader[i].Ef_Filter[i][0]
#	print A
