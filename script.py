import sys
import subprocess
import os

information = open('information.data', 'r')
data = information.readlines()


IP_home = data[0].rstrip('\n')
IP_gf = data[1].rstrip('\n')

print(IP_home)
print(IP_gf)


#IP_Network = config(data[0].rstrip('\n'))
#IP_Device = config(data[1].rstrip('\n'))

proc = subprocess.Popen(['arp', '-g'], stdout = subprocess.PIPE)
#proc = subprocess.Popen(['ping', IP_home], stdout = subprocess.PIPE)

while True:
    line = proc.stdout.readline()
    # if not line:
    #     break


    # print(line)
    # connected_ip = line.decode('utf-8').split()#[3]

    if 'XXXXXXXXX' in line.decode('utf-8').upper() :
        subprocess.Popen(['wsay', 'girlfriend connected'])
        quit()

subprocess.Popen(['wsay', 'girlfriend is not connected'])
