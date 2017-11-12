# Networking and Security Tools

A set of tools for networking and security written in python.

## Prerequisites

These tools use [python2](https://www.python.org/downloads/) and [scapy](https://scapy.readthedocs.io/en/latest/)

After installing python2, to install scapy use pip:
```
$ pip install scapy
```

## ARP Cache Poisoning Detector - arpwatch.py
Reads the current ARP cache entries and monitors ARP traffic for any MAC address changes.

### Usage
```
$ sudo python arpwatch.py [-i interface]
	-i : specify an interface to listen on
```

### Examples
```
$ sudo python arpwatch.py
$ sudo python arpwatch.py -i eth0
```

### Description
If an interface is not specified, use netifaces to get all possible interfaces and select the first one.

A dictionary is created with all IP and MAC addresses in the ARP cache using the command 'arp -a'

To monitor ARP traffic, sniff for packets on the specified interface with a filter of 'arp', and whenever a packet is received, check to see if the MAC address has been changed. If it has, then output the change.

## TCP Service Fingerprinting - synprobe.py
Performs a TCP SYN scan for any open ports for a given IP. For every open port, print the first 1024 bytes returned by the server.

### Usage
```
$ sudo python synprobe.py [-p port_range] target
	-p     : specify port range to be scanned
	target : target server IP address
```

### Examples
```
$ sudo python synprobe.py
$ sudo python synprobe.py -p 8080
$ sudo python synprobe.py -p 20-25
```

### Description
If no ports are specified, common ports are checked: 80,22,443,465,21,20,23,53,8080.
Performs TCP SYN scan for open ports using sr1(). If NoneType is returned, port cannot be connected to. If results have TCP layer with SYN/ACK flag, then it is an open port. If there is a RST/ACK flag, then it is a closed port.

For all open ports, connect to target using a socket and and get a 1024 byte response. If there is no response, send a request ('Hi there!') and see if there is a response.