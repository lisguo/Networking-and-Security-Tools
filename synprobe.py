from scapy.all import *
import socket
from time import sleep
import sys

open_ports = []
target = sys.argv[-1]

if sys.argv[1] == '-p':
	# Specify port
	port_rng = sys.argv[2].split('-')
	port1 = int(port_rng[0])
	if len(port_rng) > 1:
		port2 = int(port_rng[1])
	else:
		port2 = port1
	search_ports = list(range(port1, port2+1))
else:
	# Check common ports
	search_ports = [80,22,443,465,21,20,23,53,8080]

# Check ports if they are open
for port in search_ports:
	print("")
	print("Checking port " + str(port))
	scan_results = sr1(IP(dst=target)/TCP(dport=port,flags="S"), timeout=2)
	if(str(type(scan_results)) == "<type 'NoneType'>"):
		print("Cannot connect to port " + str(port))
	elif(scan_results.haslayer(TCP)):
		if(scan_results.getlayer(TCP).flags == 0x12):
			open_ports.append(port)
		elif(scan_results.getlayer(TCP).flags == 0x14):
			print("Closed Port: " + str(port))

# No open ports, exit program
if len(open_ports) == 0:
	print("Could not find an open port.")
	sys.exit()

# All open ports found
print("")
print("Open ports:", open_ports)

# For each open port, connect through a socket and get 1024 bytes
for open_port in open_ports:
	print("")
	print("Open Port: " + str(open_port))
	print("Connecting to server...")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(5)
	try:
		s.connect((target, open_port))
	except socket.timeout:
		print("Connection timed out.")
		continue
	print("Connected.")

	# Print 1024 bytes
	success = False
	for i in range(0,5):
		try:
			reply = s.recv(1024)
			print(reply)
			if len(reply) > 1:
				success = True
				break
		except socket.timeout:
			# Send request
			s.send('Hi there!')
			print("Request Sent.")
			sleep(1)
	s.close()

	if not success:
		print("No response.")