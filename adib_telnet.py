import pexpect

ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'

session = pexpect.spawn('telnet ' + ip_address, encoding='utf-8',timeout=20)
result = session.expect(['Username:', pexpect.TIMEOUT])

if result != 0:
    print('--- FAILURE! creating session for: ', ip_address)
    exit()

session.sendline(username)
result = session.expect(['Password:', pexpect.TIMEOUT])

if result != 0:
    print('--- FAILURE! entering username: ',username)
    exit()

session.sendline(password)
result = session.expect(['#', pexpect.TIMEOUT])

if result != 0:
    print('--- FAILURE! entering passsword: ',password)
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


print('--------------------------------------------')
print('')
print('--- SUCCESS connecting to: ', ip_address)
print('---              Username: ', username)
print('---              Password: ', password)
print('')
print('--------------------------------------------')

session.sendline('quit')
session.close()