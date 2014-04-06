import mk_sense

# NOW WITH PROPER IMPLEMENTATIONS, PURPOSE IS TO TAKE A SET OF .feel FILES AND CREATE A MUCH LARGER SET OF .impr FILES FROM THE COMPARISON BETWEEN EACH 2 INDIVIDUAL .feel FILES
EReader = [0]*30
a=0
b=0
imp_t = [0]*900
while a<30:
        EReader[a] = mk_sense.effort_reader(a)
        EReader[a].allocation_def()
        EReader[a].read_file()
	EReader[a].calc_values_per_joint()
	while b<30:
		if b>a:
			imp_t[30*a+b] = mk_sense.impression_taker(a,b)
		b = b+1
        b = 0
        a = a+1
b=0
a=0

while a<30:

#	EReader[a].get_mean_effort_per_joint()
	while b<30:
                if b>a:
			EReader[a].print_lowest_recorded_torque(a, imp_t[30*a+b])
			EReader[a].print_highest_recorded_torque(a, imp_t[30*a+b])
			EReader[a].print_mean_effort_per_joint(a, imp_t[30*a+b])
			EReader[a].get_differences_in_torque(EReader[b])
			EReader[a].print_difference_between_mean_torques(imp_t[30*a+b])
			EReader[a].print_difference_between_lowest_torques(imp_t[30*a+b])
			EReader[a].print_difference_between_highest_torques(imp_t[30*a+b])
			EReader[a].clear()
		b=b+1
        b = 0
	a = a+1
		
