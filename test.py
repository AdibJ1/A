import pexpect
import re

# Configuration parameters
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
password_enable = 'class123!'

# Hardening checklist (unchanged)
hardening_checklist = {
    'SSH enabled': r'ip ssh version 2',
    'Telnet disabled': r'no service telnet',
    'Password encryption': r'service password-encryption',
    'Logging enabled': r'logging buffered',
    'NTP configured': r'ntp server',
}

def check_hardening(show_running_config):
    for check, rule in hardening_checklist.items():
        if rule in show_running_config:
            print(f'[SUCCESSFUL] {check}')
        else:
            print(f'[FAILURE] {check}')

# Start an SSH session
session = pexpect.spawn('ssh ' + username + '@' + ip_address, encoding='utf-8', timeout=20)
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('--- FAILURE! creating session for: ', ip_address)
    exit()

# Send the login password
session.sendline(password)
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering password: ', password)
    exit()

# Enter enable mode
session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering enable mode')
    exit()

# Send the enable password
session.sendline(password_enable)
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering enable mode after sending password')
    exit()

# Enter configuration mode
session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering config mode')
    exit()

# Set the hostname
session.sendline('hostname R1')
result = session.expect([r'R1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! setting hostname')

# Create a loopback interface and assign IP
session.sendline('interface loopback 0')  # Create Loopback 0
result = session.expect([r'R1\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering loopback interface config mode')
    exit()

session.sendline('ip address 10.10.10.13 255.255.255.0')  # Assign IP address to loopback
result = session.expect([r'R1\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! assigning IP to loopback interface')
    exit()

session.sendline('no shutdown')  # Enable the interface
result = session.expect([r'R1\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! bringing loopback interface up')
    exit()

# Exit from interface configuration mode
session.sendline('exit')

# Enable OSPF
session.sendline('router ospf 1')  # Enable OSPF process 1
result = session.expect([r'R1\(config-router\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering OSPF router config mode')
    exit()

# Set OSPF router ID (we use the loopback address here for simplicity)
session.sendline('router-id 10.10.10.13')  # Set router ID (you can choose another ID)
result = session.expect([r'R1\(config-router\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! setting OSPF router ID')
    exit()

session.sendline('network 10.10.10.13 0.0.0.255 area 0')  # Advertise the loopback network
result = session.expect([r'R1\(config-router\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! advertising network in OSPF')
    exit()

# Exit from OSPF router config mode
session.sendline('exit')

# Show running-config to check hardening
session.sendline('show running-config')
result = session.expect([r'#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! showing running config')
    exit()
show_running_config = session.before
check_hardening(show_running_config)

# Save configuration
session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering config mode')
    exit()

session.sendline('copy running-config startup-config')
session.sendline('enter')
result = session.expect([r'R1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! saving configuration')
else:
    print('--- SUCCESS saving configuration')

# Exit from configuration mode
session.sendline('exit')
session.sendline('exit')

# Print success message
print('---------------------------------------')
print('')
print('-- Success connecting to:  ', ip_address)
print('---             Username:  ', username)
print('---             Password:  ', password)
print('--')
print('---------------------------------------')

# Close the session
session.close()
