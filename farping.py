#!/usr/bin/python
# coding: utf-8


#### MODULE ####
import argparse, os
from os import geteuid

###### ARGUMENTS ######

# ARGUMENTS IN THE CONSOLE
parser = argparse.ArgumentParser()	#Parser

# Options :

# --help or -h is native
# --alive or -a
parser.add_argument("-a", "--alive", help="Show systems that are alive", action="store_true")


# Positional argument : ip
parser.add_argument("ip1", help="IP with mask or first ip of the range to scan", type=str) #IP adress with mask or first ip of the range to scan

parser.add_argument("ip2", help="Last ip of the range to scan. Obligatory for specify a ip range", type=str) #Last ip adress of the range. Obligatory for specify a ip range



args = parser.parse_args() #Take the arguments into 'args'
###### END ARGUMENTs ######



##### CHECK INSTALL OF ARPING #####

#Check if the user is root and if he have arping installed :
if geteuid() == 0:
	checkinstall = os.popen("dpkg -s arping")
	out = checkinstall.read()
	if out.find("Status: install ok installed") == -1:
		print("Error : arping package is not install please install it")
		exit(1)
#Check if the normal user have arping installed :
else :
	checkinstall = os.popen("dpkg -s arping".split(), stdout = subprocess.PIPE, stderr=subprocess.PIPE)
	out = checkinstall.read()
	if out.find("Status: install ok installed") == -1:
		print("Error : arping package seem not install try in root or install it")
		exit(1)
##### END OF CHECK INSTALL OF ARPING #####



#### HEADER ####
print(r"""      
/!\ Warning it is possible to the response not come of the targeted devices but of a proxy server /!\ 
""")
#### HEADER END ####



#### BEGIN checking ip1 argument ####

#Check if ip is specified with mask :
try:
	splited = args.ip1.split("/")
	if splited[1]:
		print("Error: you cannot specify a mask")
		exit(1)
except:
	pass
	del splited

#Check if ip1 is valid :

ip_1 = args.ip1.split(".") #Separate each byte of the ip address


#Check if the ip contain 4 bytes :
if len(ip_1) > 4 or len(ip_1) < 4 :
	print("Error: first ip address contain more or less than 4 bytes ")
	exit(1)

#Check if all the bytes of ip address are int less or equal at 255 and greater or equal at 0 :
for byte in ip_1 :
	try: 
		byte = int(byte) #Check if all bytes are int
	except ValueError:
		print("Error: first ip address contain none numeric value(s)")
		exit(1)

	if byte < 0 or byte > 255 : #Check if all bytes are greater or equal at 0 bits or less or equal at 255 bits
		print("Error: first ip address contain byte(s) less than 0 bit or greater than 255 bits")
		exit(1)


	



# At this point :
# The variable "ip_1", contain the ip address cut in 4 parts of 1 byte


#### END checking ip1 argument ####




#### BEGIN checking ip2 argument ####

#Check if ip2 contain no mask :

try:  #If mask
	splited = args.ip2.split("/")
	if splited[1]:
		print("Error : you cannot specify a mask")
		exit(1)

except: #If no mask 
	del splited
	pass
	
	

#Check if ip2 is valid :


ip_2 = args.ip2.split(".") #Separate each byte of the ip address
#Check if the ip contain 4 bytes :

if len(ip_2) > 4 or len(ip_2) < 4 :
	print("Error: second ip address contain more or less than 4 bytes ")
	exit(1)

#Check if all the bytes of ip address are int less or equal at 255 and greater or equal at 0 :
for byte in ip_2 :
	try: 
		byte = int(byte) #Check if all bytes are int
	except ValueError:
		print("Error: second ip address contain none numeric value(s)")
		exit(1)

	if byte < 0 or byte > 255 : #Check if all bytes are greater or equal at 0 bits or less or equal at 255 bits
		print("Error: second ip address contain byte(s) less than 0 bit or greater than 255 bits")
		exit(1)
#Check if ip1 and ip2 are not the same :
if ip_1 == ip_2 :
	print("Error : the two ip address are the same")
	exit(0)

#Check if ip1 are less than ip2 :
#Add some 0 at each byte who contain less of 3 digit (used for calcul)
	
#For ip_1 :
ip1_calc = []
for byte in ip_1:
	if int(byte) < 100 and int(byte) > 10:
		byte = "0" + byte
		ip1_calc.append(byte)
			
	elif int(byte) < 10 :
		byte = "00" + byte
		ip1_calc.append(byte)

	else :
		ip1_calc.append(byte)

#For ip_2 :
ip2_calc = []
for byte in ip_2:
	if int(byte) < 100 and int(byte) > 10:
		byte = "0" + byte
		ip2_calc.append(byte)
			
	elif int(byte) < 10 :
		byte = "00" + byte
		ip2_calc.append(byte)
	else :
		ip2_calc.append(byte)

	

#Check if ip1_calc is not greater than ip2_calc :
ip1_calc = int(''.join(ip1_calc))
ip2_calc = int(''.join(ip2_calc))
	
if ip1_calc > ip2_calc :
	print("Error : the first ip adress is greater than the second")
	exit(1)
		

#At this point :
# The variable "ip_2", contain the last ip address of range, cut in 4 parts of 1 byte


#### END checking ip2 argument ####




#### SCAN ####

#Function of scan :
def arping(ip):
	
	state = None;
	str(ip)
	command = "arping {} -C1 -w0.1".format(ip)
	arping = os.popen(command)
	out = arping.read()
	if args.alive == True: #If --alive is activated
		if out.find("1 packets transmitted, 1 packets received") != -1:
			print(ip)
	
	else: #If --alive is not activated
		if out.find("1 packets transmitted, 1 packets received") != -1:
			print("Alive: {}".format(ip))
		else:
			print("Timed-out : {}".format(ip))


	
# Scan the ip_1 to ip_2 range :



ip_str = [] #Transform the ip_1 array into a string

#Transform ip_1 into int array
ip1 = []
for byte in ip_1:
	ip1.append(int(byte))
	
	
#Transform ip_2 into int array
ip2 = []
for byte in ip_2:
	ip2.append(int(byte))

#Transform ip_1 in array of string
for byte in ip_1:
	ip_str.append(str(byte))

#Check if only the last byte change
if ip1[0] != ip2[0] or ip1[1] != ip2[1] or ip1[2] != ip2[2]  :
	print("Error : only the last byte of the ip address can be change")
	exit(1)


#### Checking if the first byte of each address is the same
	
#Loop of scan :
print("---- SCAN BEGIN ----")
for i in range(0, 4): 
	ip_str[i] = str(ip1[i])

ip_str = '.'.join(ip_str)

while ip1 <= ip2:
	#Call function 
	arping(ip_str)

	#Calcul
	
	ip1[3] += 1

	#ip1 is convert in str in ip_str
	ip_str=[]

	for byte in ip1: 
		ip_str.append(str(byte))
	ip_str = '.'.join(ip_str)

print("---- SCAN END ----")
exit(0)




#### END SCAN ####











	




	









	


	
	



		


	




