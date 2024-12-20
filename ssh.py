# Import required modules/packages/library
import pexpect

# Define Variables
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
password_enable = 'class123!'

# Create the ssh session
session = pexpect.spawn('ssh ' + username + '@' + ip_address,encoding='utf-8',timeout=20)
result = session.expect(['Password:',pexpect.TIMEOUT,pexpect.EOF])

# Check for error
if result != 0:
    print('--- FAILURE! creating session for: ', ip_address)
    exit()

# Session expecting password , enter details
session.sendline(password)
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])

# check for error , if exists then display error and exit
if result != 0:
    print('--- FAILURE! entering password: ', password)
    exit()

# Enter enable mode
session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

# check for error , if exists then display error and exit
if result != 0:
    print('--- FAILURE! entering enable mode')
    exit()

# Session enable password details
session.sendline(password_enable)
result = session.expect(['#', pexpect.TIMEOUT,pexpect.EOF])

# check for error , if exists then display error and exit
if result != 0:
    print('--- FAILURE! entering enable mode after sending password')
    exit()

# enter configuration mode
session.sendline('configure terminal')
result = session.expect([r' . \(config\)#',pexpect.TIMEOUT,pexpect.EOF])

# check for error , if exists then display error and exit
if result != 0:
    print('--- FAILURE! entering config mode')
    exit()

# change the hostname to R1
session.sendline('hostname R1')
result = session.expect([r'R1\(config\)#',pexpect.TIMEOUT,pexpect.EOF])

# check for error , if exists then display error and exit
if result != 0:
    print('--- FAILURE! setting hostname')
    exit()

#Exit config mode 
session.sendline('exit')

#Exit enable mode
session.sendline('exit')

# Display a success message if it works
print('------------------------------------------')
print('')
print('--- Success! connecting to: ',ip_address)
print('--- Success! connecting to: ', username)
print('--- Success! connecting to: ', password)
print('')
print('------------------------------------------')

# Terminate SSH session 
session.close()