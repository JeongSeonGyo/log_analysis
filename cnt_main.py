import os
import sys
import re
import datetime

def parsing():
	global flag
	flag=0

	open('log_grouping.txt','w')
	pars = []
	with open('log_contents.txt','r') as f:
		for line in f.readlines():
			pars.append(line.split(' '))

	
	'''
	pars[0] =  clientIP
	pars[1] =  client Information
	pars[2] =  user ID
	pars[3] =  end Time
	pars[4] =  method
	pars[5] =  request Source
	pars[6] =  protocol
	pars[7] =  status code 1
	pars[8] =  status code 2
	pars[9] =  size
	pars[10] =  reference header
	pars[11] =  user agent header
	'''
	
	for a in pars:	
		if len(a) > 3 and a[1] != '':
			
			if a[3][0] == '[':
				a[3] = a[3][1:]
				
			if a[4][-1] ==']':
				a[4] = a[4][:-1]

			if a[5][0] == '"':
				a[5] = a[5][1:]

			if a[7][-1] == '"':
				a[7] = a[7][:-1]

			if a[10][0] == '"':
				a[10] = a[10][1:]

			if a[10][-1] == '"':
				a[10] = a[10][:-1]

			if a[11][0] == '"':
				a[11] = a[11][1:]

	
	cnt_one(pars,2) #user ID
	cnt_one(pars,0) #IP	
	cnt_one(pars,6) #access file

	cnt_two(pars,2,6)
	cnt_two(pars,0,6)
	cnt_two(pars,6,2)
	cnt_two(pars,6,0)
			

	max_size(pars) #size
	max_date(pars)
	
def max_date(log):
	#print "\nfirst %s" %log
	for a in log:
		if len(a) > 3 and a[3] != '':
			day = a[3][0:2]
			month = a[3][3:6]
			year = a[3][7:11]
			hour = a[3][12:14]

	count_date(log,day,"day")
	count_date(log,month,"month")
	count_date(log,year,"year")
	count_date(log,hour,"hour")

def count_date(log,day,word):
	date ={}
	for a in log:
		if len(a)>3 and a[3]!='':
			if day in date:
				date[day] += 1
			else:
				date[day] = 1

	#print date

	max_cnt=0
	max_day = []
	for a in date:
		if max_cnt <= date.get(a):
			if max_cnt < date.get(a):
				del max_day[:]
			max_cnt = date.get(a)
			max_day.append(a)
	for i in max_day:
		write(1, i, str(0), max_cnt)

def max_size(log):
	max_cnt=0
	for a in log:
		if len(a) > 1:
			if max_cnt <= a[9]:
				max_cnt = a[9]

	write(1,str(0),str(0),max_cnt)

def cnt_one(log,num):
	user = []
	#count access number for each user
	user = cnt_max(log, num)
	#print '{}'.format(user) + "is the most approached\n" 
	#write( '{}'.format(user) + "is the most approached\n" )
	for i in user:
		write(1,i,str(0),max_access)
	return user

def cnt_max(log, num):
	user = {}
	global max_access
	max_access = 0
	
	user_id = []

	for a in log:
		if len(a) > 1:
			if a[num] in user:
				user[a[num]] +=1
			else:
				user[a[num]] = 1
		
	for a in user:
		if max_access <= user.get(a):
			if max_access < user.get(a):
				del user_id[:]
			max_access = user.get(a)
			user_id.append(a)

	return user_id

def cnt_two(log, first, second):
	
	user = []
	user = cnt_max(log, first)

	path = {}
	max_path = []

	#save the data
	for i in user:
		for j in log:
			if len(j) > 1:
				if j[first] == i:
					name = i+' '+j[second]
					if name in path:
						path[name] +=1
					else:
						path[name] = 1
	#count max
	max_cnt = 0
	for k in path:
		if max_cnt <= path.get(k):
			if max_cnt < path.get(k):
				del 	max_path[:]
			max_cnt = path.get(k)
			max_path.append(k)

	for j in max_path:
		write(1,j.split(' ')[0], j.split(' ')[1], max_cnt)

def write(num, standard, by ,acc_num):
	global flag
	res = open('result.txt','a')
	if flag == 0:
		res.write(str(datetime.datetime.now()) + '\n')
		res.write('{:<20}'.format("Standard"))
		res.write('{:<42}'.format("By"))
		res.write('{:<2}'.format("Access number\n"))
		res.write('{:-<100}'.format(' ')+'\n')
		flag = flag+1

	i=0
	while(1):		
		if i == num:
			break

		if type(standard) == 'list':
			res.write('{:<15}'.format(standard[i]))
			
		else:
			if standard == str(0):
				res.write('{: <15}'.format('-'))
			else:
				res.write('{:<15}'.format(standard))
		res.write(' \t ')
		
		if type(by) == 'list':
			res.write('{:<40}'.format(by[i]))
		else:
			if by == str(0):
				res.write('{: <40}'.format('-'))
			else:
				res.write('{:<40}'.format(by))
		res.write(' \t ')

		if type(acc_num) == 'list':
			res.write('{:<2}'.format(acc_num[i]))
			
		else:
			if acc_num == str(0):
				res.write('{: <2}'.format('-'))
			else:
				res.write('{: <2}'.format(str(acc_num)))	
		res.write(' \n')

		i = i+1
		
def main():
	res = open('result.txt','a')
	#os.system( "cd /var/log/apache2")
	os.system("cd ~/anal_log")
	os.system ("ls access* > log_title.txt")
	contents = open('log_contents.txt','w')	#for init

	with open('log_title.txt','rb')  as file:
		lines = file.readlines()	#lines -> list
		for a in lines:
			a = a[:-1]	#extract \n
			#os.system("cp /var/log/apache2/"+a+ "/home/starmichelle/log/"+'temp.txt')
			os.system("cp ~/anal_log/" +a+ " ~/anal_log/"+'temp.txt')
			with open('temp.txt','r') as f:
				contents = open('log_contents.txt','a')
				contents.write(f.read())
			
			contents.close()
	os.system("rm temp.txt")

	parsing()
	res.write('{:=<100}'.format('')+'\n')
	os.system("rm log_title.txt")		


if __name__ == '__main__':
	main()
