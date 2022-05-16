import urllib.request
import base64
import sys
import datetime
import socket

import config
# config.py
# user = ""
# updater_client_key = ""
#
# hostname = ""


def get_local_ipv4():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def get_ipv6():
    ipv6l = []
    for i in socket.getaddrinfo(socket.gethostname(), 0, proto=socket.AF_INET6):
        if i[0] == socket.AddressFamily.AF_INET6:
            print("Found ipv6: " + str(i))
            ipv6l.append(i[4][0])
    return ipv6l[-1]


print("\n\nstarting at " + str(datetime.datetime.now()))

# get current ip
myIPv6 = get_ipv6()
ipSetDNS = get_local_ipv4() + "," + myIPv6
#print(myIPv6)
#print(myipv4Local)

# create credentials header
credentials = ('%s:%s' % (config.user, config.updater_client_key))
encoded_credentials = base64.b64encode(credentials.encode('ascii'))

req = urllib.request.Request('https://members.dyndns.org/v3/update?hostname=' + config.hostname + '&myip=' + ipSetDNS)
req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))

# actual update
# https://help.dyn.com/remote-access-api/perform-update/
with urllib.request.urlopen(req) as response:
    responseContent = response.read().decode("utf-8").strip()
    print("Update response (" + req.full_url + "): " + responseContent)

    if responseContent == "nochg " + ipSetDNS:
        print("IP identical")
    elif responseContent == "good " + ipSetDNS:
        print("IP updated")
    else:
        print("Could not update IP!")
        sys.exit(1)

sys.exit(0)
