from __future__ import division
import mk_sense
from pylab import *
import numpy as np

# take a list and return the n most common elements near a certain value:
def return_common_elements(listf, value, nc, precision):
	cel = [0]*nc
	cel_count = [0]*nc
	a = 0;
	for i in range(len(listf)):
			if abs(listf[i]-value)<precision and listf[i] not in cel and listf.count(listf[i])>cel_count[a]:
						cel[a] = listf[i]
						cel_count[a] = listf.count(cel[a])
						a=cel_count.index(min(cel_count))
	cel_p_c = zip(cel_count, cel)
	cel_p_c.sort(); cel_p_c.reverse()
	return cel_p_c

# take a list and return a list containing only elements within a certain distance of the mean value
def rep_filter(listf, acc):
	l = filter(lambda x: -acc<x<+acc, listf)
	return l
# take a list and return a list containing only elements outside a certain distance of the mean value
def rep_reject_filter(listf, acc):
	l = filter(lambda x: (sum(listf)/len(listf))-acc>x or x>(sum(listf)/len(listf))+acc, listf)
	return l

# auxiliary for fft_filter()
def filter_rule(x,freq, band):
    if abs(freq)>0+band or abs(freq)<0-band:
        return 0
    else:
        return x
# auxiliary for fft_filter_band_reject()
def filter_rule_band_reject(x, freq, band):
	if band>abs(freq)>-band or freq==band:
		return 0
	else:
		return x

# take a certain number floats and return 
def return_average(args):
	n = [0]*len(args[0])*len(args)
	for i in range(len(args)):
		for j in range(len(args[i])):
			n[j] += abs(args[i][j])		
	return n

# accept a band centered around 0 in the transform
def fft_filter(ListA, dt, band):
	F = rfft(ListA, n=3000)
	f = fftfreq(len(F),dt)
	F_filtered = array([filter_rule(x,freq, band) for x,freq in zip(F,f)])
	print F_filtered
	return F_filtered
def filter_phase(ListA, dt, band):
	F = rfft(ListA, n=3000)
	f = fftfreq(len(F),dt)
	for i in range(len(F)):
		F[i] = abs(F[i])
	F_filtered = array([filter_rule(x,freq, band) for x,freq in zip(F,f)])
	F_filtered = irfft(F_filtered)
	print F_filtered
	return F_filtered

# reject a certain band centered around 0 in the transform
def fft_filter_band_reject(ListA, dt, band):
	F = fft(ListA, n=1024)
	f = fftfreq(len(F),dt)
	F_filtered = array([filter_rule_band_reject(x,freq, band) for x,freq in zip(F,f)])
	F_filtered = ifft(F_filtered)
	return F_filtered
# find first n fundamental frequencies in the transform.
def fft_filter_find_fundamentals(ListA, dt, n):
	F = fft(ListA, n=1024)
	f = fftfreq(len(F),dt)
	m = 0; a=0
	for j in range(n):
		m = filter(lambda x: x!=0 and x>m, f)
		for i in range(len(m)):
			m[i] = abs(m[i])
		m = min(m)
	F_filtered = array([filter_rule(x,freq, m) for x,freq in zip(F,f)])
	F_filtered = ifft(F_filtered)
	return F_filtered
# find last n fundamental frequencies in the transform.
def fft_filter_find_last_fundamentals(ListA, dt, n):
	F = fft(ListA, n=1024)
	f = fftfreq(len(F),dt)
	m = 0	
	for j in range(n):
		m = filter(lambda x: x!=0 and x>m, f)
		for i in range(len(m)):
			m[i] = abs(m[i])
		m = min(m)

	F_filtered = array([filter_rule_band_reject(x,freq, m) for x,freq in zip(F,f)])
	F_filtered = ifft(F_filtered)
	return F_filtered
# plot a given figure
def show_fig(F_filtered, dt, l):
	s_time = [k*dt for k in range(len(F_filtered))]
	figure()
	subplot(1,1,1)
	plot(s_time,F_filtered,'r')
	number = {'i': l}
	xlabel('{i}, time [s]'.format(**number))
	show()
def show_power_spectrum(F_filtered, dt, l):
	F = fft(F_filtered, n=1024)
	f = fftfreq(len(F), dt)
	F2 = log10(np.abs(F)**2)
	idx = argsort(f)
	figure()
	subplot(1,1,1)
	plot(f[idx],F2[idx],'r')
	number = {'i': l}
	xlabel('{i}, freq [hz]'.format(**number))
	show()

def show_phase_spectrum(F_filtered, dt, l):
	F = fft(F_filtered, n=1024)
	f = fftfreq(len(F), dt)
	F2 = np.angle(F)
	idx = argsort(f)
	figure()
	subplot(1,1,1)
	plot(f[idx],F2[idx],'r')
	number = {'i': l}
	xlabel('{i}, freq [hz]'.format(**number))
	show()


# Moving averages method for a rectangular window

def moving_average(ListA, window, dt, l):
#	np = hanning(len(ListA)-window)
	internal_window = 0
	average = [0.0 for i in range(len(ListA))]
	average_rec = [0.0 for i in range(len(ListA)-window)]
	s_time = [k*dt for k in range(len(ListA)-window)]
	for i in range(len(ListA)-window):
		for k in range(window):
			try:
				internal_window = internal_window+ListA[i+k]
			except IndexError:
				internal_window = internal_window
		average[i] = internal_window/window
		internal_window = 0 
	for i in range(window):
		average.pop()
	return average

		
# auxiliary functions for break_list_and_append_to
def function_a(fua, foo):
	for i in range(len(fua)):
		foo.append(fua[i])
def function_a2(fuda, foo):
	for i in range(len(fuda)):
		for j in range(len(fuda[i])):
			foo.append(fuda[i][j])
def function_a3(flima, foo):
	for i in range(len(flima)):
		for j in range(len(flima[i])):
			for k in range(len(flima[i][j])):
				foo.append(flima[i][j][k])
def function_a4(flemba, foo):
	for i in range(len(flemba)):
		for j in range(len(flemba[i])):
			for k in range(len(flemba[i][j])):
				for m in range(len(flemba[i][j][k])):
					foo.append(flemba[i][j][k][m])
# takes a list and removes up to 3 dimensions from it, creating a list of single elements
def break_list_and_append_to(listA, foo):
	try:
		function_a4(listA, foo)
	except TypeError:
		try: 
			function_a3(listA, foo)
		except TypeError:
			try:
				function_a2(listA, foo)
			except TypeError:
				function_a(listA, foo)



		
	
