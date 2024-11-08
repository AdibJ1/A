import pexpect
import re

ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
password_enable = 'class123!'

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

session = pexpect.spawn('ssh ' + username + '@' + ip_address, encoding='utf-8', timeout=20)
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('--- FAILURE! creating session for: ', ip_address)
    exit()

session.sendline(password)
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering password: ', password)
    exit()

session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering enable mode')
    exit()

session.sendline(password_enable)
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering enable mode after sending password')
    exit()

session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! entering config mode')
    exit()

session.sendline('hostname R1')
result = session.expect([r'R1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('--- FAILURE! setting hostname')
    
session.sendline('exit')

session.sendline('show running-config')
result = session.expect([r'#', pexpect.TIMEOUT,pexpect.EOF])
if result != 0:
    print('--- FAILURE! showing running config')
    exit()
show_running_config = session.before
print('----- Raw Running Config ---')
print(show_running_config)
print('----------------------------')
check_hardening(show_running_config)


    
session.sendline('exit')
session.sendline('exit')

print('---------------------------------------')
print('')
print('-- Success connecting to:  ', ip_address)
print('---             Username:  ', username)
print('---             Password:  ', password)
print('--')
print('---------------------------------------')

session.close()