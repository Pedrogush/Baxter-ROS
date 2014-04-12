from __future__ import division
import mk_sense
from pylab import *
import nonlinear_filter
import fourier_filter

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
F = 0
f = 0
F_filtered = 0


while a<samples:
        EReader[a] = mk_sense.effort_reader(a, nb, nb)
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
def filter_rule(x,freq):
    band = 0.01
    if abs(freq)>0+band or abs(freq)<0-band:
        return 0
    else:
        return x
# acc = 0.02 yields good results most of the time, must write code to iterate and try different values of acc
# need to throw this to one of the classes, most likely effort_reader in module mk_sense
#for i in range(samples):
#	for j in range(14):
#		acc = 0.0
#		while flag==0:
#			EReader[i].Ef_Filter_Clone[j] = EReader[i].Ef_Filter[j]
#			EReader[i].Ef_Filter_Clone[j] = rep_filter(EReader[i].Ef_Filter_Clone[j], acc)
#			if len(EReader[i].Ef_Filter_Clone[j])>0:
#					flag = 1
#			if len(EReader[i].Ef_Filter_Clone[j])==0:
#					acc = acc+0.01
#		flag=0
#for m in range(14):
#	for i in range(samples):
#		print sum(EReader[i].Ef_Filter_Clone[m])/float(len(EReader[i].Ef_Filter_Clone[m]))
dt = 0.01
s_time = [0]*samples
print '\n'
#for i in range(samples):
#	s_time[i] = [k*dt for k in range(len(EReader[i].Ef_Filter[1]))]#
#
#	F = fft(EReader[i].Ef_Filter[1])
#	f = fftfreq(len(F),0.01)
#	F_filtered = array([filter_rule(x,freq) for x,freq in zip(F,f)])
#	F_filtered = ifft(F_filtered)
#	F = ifft(F)
#	print f
#	print F_filtered
#	figure()
#	subplot(1,1,1)
#	plot(s_time[0],F_filtered,'r')
#	plot(s_time[0],F,'b')
#	xlabel('time [s]')
#	show()
sum_of_Ef = [[] for i in range(14)];
for i in range(14):
	for j in range(samples):
		nonlinear_filter.break_list_and_append_to(EReader[j].Ef_Filter[i],sum_of_Ef[i])
#	
#fourier_filter.moving_average(sum_of_Ef[2], 2, 0.01)
#for i in range(14):
#	sum_of_Ef[i] = fourier_filter.moving_average(sum_of_Ef[i], 50,0.01)
for i in range(7):

	sum_of_Ef[i] = rep_filter(sum_of_Ef[i], 0.08)
	sum_of_Ef[i] = fourier_filter.fft_filter(sum_of_Ef[i], 0.01, 0.1)
#	sum_of_Ef[i] = fourier_filter.moving_average(sum_of_Ef[i], 75,0.01, i)
#	sum_of_Ef[i] = fourier_filter.moving_average(sum_of_Ef[i], 100,0.01, i)
#	sum_of_Ef[i] = fourier_filter.moving_average(sum_of_Ef[i], 125,0.01, i)
#	sum_of_Ef[i] = fourier_filter.moving_average(sum_of_Ef[i], 150,0.01, i)
#	sum_of_Ef[i] = fourier_filter.moving_average(sum_of_Ef[i], 175,0.01, i)
#	sum_of_Ef[i] = fourier_filter.moving_average(sum_of_Ef[i], 1000,0.01, i)
	fourier_filter.show_fig(sum_of_Ef[i], 0.01, i)
	print sum(sum_of_Ef[i])/len(sum_of_Ef[i])
	print (max(sum_of_Ef[i]) - min(sum_of_Ef[i]))/2
#	print 100*((max(sum_of_Ef[i]) - min(sum_of_Ef[i]))/2)/(sum(sum_of_Ef[i])/len(sum_of_Ef[i]))
#fourier_filter.moving_average(sum_of_Ef[0], 99, 0.01)
#for i in range(14):
#	print sum_of_Ef[i][0]		
#	for i in range(len(EReader[i].Ef_Filter[0])-1):
#		A = A + EReader[i].Ef_Filter[i][0]
#	print A

 
#
 
