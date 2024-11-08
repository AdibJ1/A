import pexpect
import re

ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
password_enable = 'class123!'

# Hardening checklist with regex patterns
hardening_checklist = {
    'SSH enabled': r'ip ssh version 2',  # Search for exact SSH version 2 command
    'Telnet disabled': r'no service telnet',  # Telnet should be disabled
    'Password encryption': r'service password-encryption',  # Check for encrypted passwords
    'Logging enabled': r'logging buffered',  # Ensure logging is enabled
    'NTP configured': r'ntp server',  # Look for NTP server configuration
}

# Function to check the running config against the hardening checklist
def check_hardening(show_running_config):
    for check, rule in hardening_checklist.items():
        # Search for the pattern in the running config
        if re.search(rule, show_running_config, re.IGNORECASE):  # Perform case-insensitive search
            print(f'[SUCCESSFUL] {check}')
        else:
            print(f'[FAILURE] {check}')

# Start SSH session
session = pexpect.spawn(f'ssh {username}@{ip_address}', encoding='utf-8', timeout=20)

# Expect Password prompt
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print(f'--- FAILURE! creating session for: {ip_address}')
    exit()

session.sendline(password)

# Expect '>' prompt for user mode
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print(f'--- FAILURE! entering password: {password}')
    exit()

# Enter enable mode
session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering enable mode')
    exit()

# Send enable password
session.sendline(password_enable)
result = session.expect([r'#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering enable mode after sending password')
    exit()

# Enter configuration mode
session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering config mode')
    exit()

# Set hostname
session.sendline('hostname R1')
result = session.expect([r'R1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! setting hostname')

# Exit configuration mode
session.sendline('exit')

# Show running configuration
session.sendline('show running-config')
result = session.expect([r'#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! showing running config')
    exit()

# Capture the running config output
show_running_config = session.before.decode('utf-8')  # Decode the byte string to a normal string

# Check hardening against the running config using regex patterns
check_hardening(show_running_config)

# Save configuration
session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering config mode')
    exit()

session.sendline('copy running-config startup-config')
session.sendline('enter')  # Simulate pressing Enter after command
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! saving configuration')
else:
    print('--- SUCCESS saving configuration')

# Exit configuration mode
session.sendline('exit')

# Exit the session
session.sendline('exit')

# Print success message
print('---------------------------------------')
print('')
print(f'-- Success connecting to: {ip_address}')
print(f'--- Username: {username}')
print(f'--- Password: {password}')
print('---------------------------------------')

# Close the session
session.close()
