import subprocess
import smtplib
import sys
import time
from datetime import datetime
from email.message import EmailMessage

def send_email(text, password):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login('marus.notifications@gmail.com', password)

        msg = EmailMessage()
        msg.set_content(text)
        msg['Subject'] = 'GF wifi'
        msg['From'] = 'marus.notifications@gmail.com'
        msg['To'] = 'marus.notifications@gmail.com'

        server.send_message(msg)
        server.close()

    except:
        print(sys.exc_info()[0])

    return

def setup():
    datafile = open('information.data', 'r')
    data = datafile.readlines()

    data[1] = data[1].split(', ')
    gf_pc = data[1][0].rstrip('\n')
    gf_phone = data[1][1].rstrip('\n')
    subnet = data[0].rstrip('\n')
    passw = data[2].rstrip('\n')
    while True:
        gf = input('is gf at home right now? y/n\t')
        if gf.lower() == 'y':
            gf = True
            break
        elif gf.lower() == 'n':
            gf = False
            break

    return gf_pc, gf_phone, subnet, gf, passw

def is_gf_home(ip_pc, ip_phone, subnet):

    #print('Looking for:', '|'+gf_phone+'|', '|'+gf_pc+'|')
    p = subprocess.Popen(["nmap", "-sn", subnet], stdout=subprocess.PIPE)
    devices = 2
    while True:
        line = p.stdout.readline()
        if not line:
            break

        line = line.decode('utf-8').rstrip('\n')
        
        if 'Nmap scan report' in line:
            if ip_pc in line or ip_phone in line:
                if ip_pc in line:
                    devices -= 1
                    #print('gf connected with pc!')
                if ip_phone in line:
                    devices -= 1
                    #print('gf connected with phone!')
                if devices == 0:
                    break

    if devices == 2:
        return False
    elif devices < 2:
        return True

def check_if_gf_home(ip_pc, ip_phone, subnet):
    
    checks = []
    #check 10 times, each time waiting for 5 secs, to get the right result
    for i in range(0,10):
        test = is_gf_home(gf_pc, gf_phone, subnet)
        print('test', i, test, end = '\t')
        checks.append(test)
        time.sleep(5)
    print('')

    true = 0
    false = 0
    for check in checks:
        if check:
            true += 1
        else:
            false += 1
    
    if true > false:
        check = True
    else:
        check = False

    return check

gf_pc, gf_phone, subnet, gf_home, passw = setup()

#main loop
while True:
    
    check = check_if_gf_home(gf_pc, gf_phone, subnet)

    now = datetime.now()

    #2 options:
        #not home -> home
        #home -> not home
    if gf_home != check:
        
        #home -> not home
        if gf_home and not check:
            print(now, '- GF just left home')
            send_email(text = 'GF has left home', password = passw)
        
        #not home -> home
        else:
            print(now, '- GF just came back home')
            send_email(text = 'GF back home', password = passw)

        gf_home = check
    
    #2 options:
        #home -> home
        #not home -> not home
    else:
        
        #home -> home
        if gf_home:
            print(now, '- GF is expected to be home and is home')
        
        #not home -> not home
        else:
            print(now, "- GF is not expected to be home and isn't home")

    time.sleep(300)
    
    
    
    
    