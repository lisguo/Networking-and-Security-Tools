# Check arguments and set interface to listen on
import netifaces
def printUsageAndExit():
	print("Invalid arguments.")
	print("USAGE: python arpwatch.py [-i interface]")
	sys.exit()

def checkArgs(args):
	if len(args) != 1 and len(args) != 3:
		printUsageAndExit()
	if len(args) > 1:
		if args[1] != '-i':
			printUsageAndExit()
		return args[2]
	else:
		# Select default interface
		return netifaces.interfaces()[0]


import sys
interface = checkArgs(sys.argv)


# Create dictionary with current ARP cache entries
import re
import os

def createDictFromCache(arp_cache):
	addrs = {}
	arp_cache = arp_cache.splitlines()
	for line in arp_cache:
		# Get IP
		ip_addrs_obj = re.search(r'\d+\.\d+\.\d+\.\d+', line)
		ip_addr = ip_addrs_obj.group()
		
		# Get MAC
		mac_obj = re.search(r'.{2}:.{2}:.{2}:.{2}:.{2}:.{2}', line)
		mac = mac_obj.group()
		
		# Add to addrs
		addrs[ip_addr] = mac
	return addrs

arp_cache = os.popen('arp -a').read()
cache_dict = createDictFromCache(arp_cache)

# Listen to packets whenever there is a different MAC address, print it
from scapy.all import *

# Function to check for correct MAC while sniffing
def checkAddr(pkt):
	if pkt[ARP].op == 2: # Response packet
		# Lookup IP in dict and check for correct MAC
		ip = pkt[ARP].psrc
		mac = pkt[ARP].hwsrc
		if ip in cache_dict:
			correct_mac = cache_dict[ip]
			if correct_mac != mac:
				return str(ip + " changed from " + correct_mac + " to " + mac)

print("Monitoring ARP traffic on interface " + interface)
pkts = sniff(prn=checkAddr, iface=interface, filter="arp")