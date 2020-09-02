"""
Short script I made to add hosts to the windows HOSTS file. This allows for IP addresses to have aliases so you don't have to memorize the address.
This may need to be run as administrator. Also, you should probably just edit the file yourself instead of with this script.

"""

from pathlib import Path

FILE = Path("C:/Windows/system32/drivers/etc/hosts")

DEFAULT_TEXT = "# Copyright (c) 1993-2009 Microsoft Corp.\n" \
             "#\n" \
             "# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.\n" \
             "#\n" \
             "# This file contains the mappings of IP addresses to host names. Each\n" \
             "# entry should be kept on an individual line. The IP address should\n" \
             "# be placed in the first column followed by the corresponding host name.\n" \
             "# The IP address and the host name should be separated by at least one\n" \
             "# space.\n" \
             "#\n" \
             "# Additionally, comments (such as these) may be inserted on individual\n" \
             "# lines or following the machine name denoted by a '#' symbol.\n" \
             "#\n" \
             "# For example:\n" \
             "#\n" \
             "#      102.54.94.97     rhino.acme.com          # source server\n" \
             "#       38.25.63.10     x.acme.com              # x client host\n\n" \
             "# localhost name resolution is handled within DNS itself.\n" \
             "#	127.0.0.1       localhost\n" \
             "#	::1             localhost\n"

with open(FILE, "r") as f:
    lines = f.readlines()

open_type = input("read, write, clear, or append?")
print(''.join(lines))
if open_type == "read":
    pass
elif open_type == "write":
    with open(FILE, "w+") as f:
        f.write(DEFAULT_TEXT)
        ip_address = input("Ip address: ")
        host_name = input("Host name: ")
        f.write("\n" + str(ip_address) + "  " + host_name)
elif open_type == "clear":
    with open(FILE, "w+") as f:
        f.write(DEFAULT_TEXT)
elif open_type == "append":
    with open(FILE, "a") as f:
        ip_address = input("Ip address: ")
        host_name = input("Host name: ")
        f.write("\n" + str(ip_address) + "  " + host_name)

with open(FILE, "r") as f:
    lines = f.readlines()
print(''.join(lines))
