# Returns the user's IPv4 address

import os

def get_ip():
    try:
        addr = os.popen('ipconfig').read()
        num1 = addr.find('IPv4')
        num2 = addr.find('Subnet Mask')
        ip = addr[(num1 + 36):(num2 - 4)]
        print ip
        return ip
    except:
        pass
        return 1, "Failed to get IPv4 address."

if __name__ == '__main__':
    get_ip()