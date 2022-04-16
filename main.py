import urllib.request
import base64
import sys
import datetime

import config
# config.py
# user = ""
# updater_client_key = ""
#
# hostname = ""

print("\n\nstarting at " + str(datetime.datetime.now()))

# get current ipv6
checkIPURL = "http://checkipv6.dyndns.com"
checkIPContent = urllib.request.urlopen(checkIPURL).read().decode("utf-8").strip()
print("IP check response (" + checkIPURL + "): " + checkIPContent)
myIPv6 = checkIPContent.lower().split("current ip address: ")[1].split("<")[0]
#print(myIPv6)

# create credentials header
credentials = ('%s:%s' % (config.user, config.updater_client_key))
encoded_credentials = base64.b64encode(credentials.encode('ascii'))

req = urllib.request.Request('https://members.dyndns.org/v3/update?hostname=' + config.hostname + '&myip=' + myIPv6)
req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))

# actual update
# https://help.dyn.com/remote-access-api/perform-update/
with urllib.request.urlopen(req) as response:
    responseContent = response.read().decode("utf-8").strip()
    print("Update response (" + req.full_url + "): " + responseContent)

    if responseContent == "nochg " + myIPv6:
        print("IP identical")
    elif responseContent == "good " + myIPv6:
        print("IP updated")
    else:
        print("Could not update IP!")
        sys.exit(1)

sys.exit(0)
