# Networking and Security Tools

A set of tools for networking and security written in python.

## Prerequisites

These tools use [python2](https://www.python.org/downloads/) and [scapy](https://scapy.readthedocs.io/en/latest/)

After installing python2, to install scapy use pip:
```
$ pip install scapy
```

## ARP Cache Poisoning Detector - arpwatch.py

### Usage
```
$ sudo python arpwatch.py [-i interface]
	-i : specify an interface to listen on
```

### Description
If an interface is not specified, use netifaces to get all possible interfaces and select the first one.

A dictionary is created with all IP and MAC addresses in the ARP cache using the command 'arp -a'

To monitor ARP traffic, sniff for packets on the specified interface with a filter of 'arp', and whenever a packet is received, check to see if the MAC address has been changed. If it has, then output the change.