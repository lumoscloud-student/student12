#!/usr/bin/python

# This file was meant to be run in the Python Interactive Interpreter
# While you can run this file from CLI just as a single python file by using the CLI command 'python ./push-T5-apic-json-w-detailed-comments.py',
# try running it from the Python Interactive Interpreter first, then delete your tenant and try it from the CLI using the above command, as well
# As you first run through this using the Python Interactive Interpreter, take your time and only copy one line at a time
# This isn't a rush to get the lab done, it's a learning experience, so take your time and learn (and re-learn!)
# Try things twice if you need/want to -- see what happens!


# Begin by opening PuTTY to your ubuntu dev bare VM, and typing 'python' and hit enter
# Now you are in the Python Interactive Interpreter
# Next continue by copying only ONE line at a time, and pasting it into the Interpreter
# If you copy too many lines at once, you will miss your chance to input data that Python is asking you to input, and the program simply won't work at all


# You do NOT need to paste any line that begins with a '#' -- Those are comments, and Python ignores them completely
# Those are just for you and me to read
# BTW, commenting the heck out of your Python scripts is a FANTASTIC way not to come back to a program 
# you wrote 6 months ago and not have a CLUE what you were thinking or trying to accomplish
# GET IN THE PRACTICE OF COMMENTING A LOT WHEN BEGINNING TO WRITE CODE!!!


# Go ahead, start copying and pasting ONE line at a time.


# Import the 'sys' python module and ask the user which aci pod, then store that information in the variable 'acipod'
import sys
acipod = raw_input('Which ACI Pod # are you trying to push data to? ')
print acipod


# Use the value from the acipod variable to populate the last digit of the third octet - which correlates to the aci pod #
apic = '10.101.2.10{0}'.format(acipod)
print apic


# Ask the user what their admin username is, then store that information in the variable 'username'
username = raw_input('What is your student admin username (e.g. student1, student2, etc)? ')
print username


# Import the 'getpass' python module so we can ask the user secret info and not broadcast it to the screen
# Ask the user what their admin password, then store that information in the variable 'password'
from getpass import getpass
password = getpass('What is your student password? ')
print password
# I said we obtained the password in secret, I didn't say we encrypted it
# This is obviously stored in clear text
# There are much more advanced ways of encrypting it, but we won't go into them in this class


# Using what we have now gathered from the user, populate our standard auth JSON file, using variables
auth = {'aaaUser': {'attributes': {'name': username, 'pwd': password } } }
print auth
# Notice how the data inside the JSON has automatically been expanded to include the values of the variables 'username' and 'password'?
# Also notice how the order is messed up (e.g. 'pwd' comes before 'name')?
# This is due to the way Python dictionarys or 'dict' data types work
# We'll talk a little more about them in the next lab


# Import the python module 'requests' for making HTTP(S) GETs and POSTs which we will use to send RESTful API calls
import requests
# Import the python module 'json' so that we can use REST to send and receive JSON data and know how to handle it
import json


# Create a 'requests' session, and store that session object as variable 's'
s = requests.Session()
print s


# Send an HTTPS POST to authenticate using the session that we just created and stored as variable 's', 
# and send the 'auth' variable which is our JSON auth data
#
# Using the variable 's' with a '.' and another word is simply calling a object/method in a class from the requests python module, 
# but as an extension of an already-created session
r = s.post('https://{0}/api/mo/aaaLogin.json'.format(apic), data=json.dumps(auth), verify=False)
print r


# The variable 'r' now is packed with a lot of good information
# Find out what the HTTP Status is, and pack that info in the variable 'status'
status = r.status_code
# Print to stdout (screen) what we just learned and stored in 'status'
# What is the difference between printing 'r' to screen and printing 'status' (which was really 'r.status_code') to screen?
# The answer? The variable data type
# To find out what the two different data types are, enter these next two commands one at a time
type(r)
# We see that 'r' is a 'Class' data type (and what Class it is)
type(status)
# And we see that 'status' or really 'r.status_code' is an 'int' or integer, which is one of the values stored in the returned information from that 'r' Class
# This is VERY, VERY import information to know for any future coding we might want to do inside this Python program, as we need to know how to query variables and work properly with what data type a variable is


# Let's get more info out of our 'r' variable. We need to get the 'cookies' or 'token' out of 'r' and store it in the variable 'cookies'
# We will send back to the APIC these cookies every subsequent time we send an HTTP POST, so that we do not have to keep authenticating
cookies = r.cookies
# Print to stdout (screen) what we just learned and stored in 'cookies'
print cookies
# Ah, another Class stored inside that same 'r' variable. Seems 'r' has quite a LOT of info in it!
# 'r' is basically what your Web Browser would get back if you browsed to a web page
# Only not only what you the human user would see, but what the browser would see and need to know and use to make the page work properly
# In fact far more information than you would see even if you did a 'View Page Source'


# We don't need the information about the HTTP Headers that we received, but I included this anyhow just to demo extra info that 'r' is holding on to
headers = r.headers
# Print to stdout (screen) what we just learned and stored in 'headers'
print headers
# That's a lot of information just in the headers alone. Let's look at just a very small subset of that info
print headers['content-type']
type(headers)


# Grab the full text response (HTML Body) that we got when we tried to authenticate
# If we failed to auth, and got back a status of something other than '200', this will hopefully help us know what went wrong
text = r.text
# Print to stdout (screen) what we just learned and stored in 'text'
print text
# Um, What??
# That is very NON-Pretty JSON
# Let's Pretty it up a bit, shall we?
from pprint import pprint
# This is the same as importing 'pprint', but instead of importing the entire Python module, we only import what we need, 
# and thus not simplify how we write our code, but also consume less memory from the host running the Python program
pprint(text)
# That didn't seem to help much at all, I wonder why not?
# If we take a look at the data type of 'text', it might give us more of a clue
type(text)
# Ah, we see that it is 'Unicode' (very similar to text or a 'string', but much a more specific text/string type)
# Let's see if we can turn it into another data type
# Let's see if we can extract the JSON out of it in a Python 'dict' or Dictionary format
jsondata = r.json()
type(jsondata)
# Now let's try to Pretty Print that
pprint(jsondata)
# Now, while there was still a TON of information on that page, it is MUCH cleaner and easier to read, especially if you back your PuTTY font size way off
# That could be useful to us later on, but for now, let's press on, shall we?


# Now here is where we have a all of the JSON data that at one time was captured from the API Inspector
# This includes 14 separate API calls that create everything in the Fabric Access Policies
# We wiped our ACI Fabric clean, so now we need to do a bunch of HTTPS REST POSTs to push all that data back to ACI
# These 15 JSON file include ONLY the Fabric Access Policies
# They included NONE of the Tenant configuration
# That will be the last thing in the file
#
# Notice that there are essentially two lines to each REST API call
# The first line packs all the JSON data into the variable 'jsonddata'
# The second line performs an HTTP POST and sends the data using the requests session that we've already set up
# Notice that every time we run the second line and POST data, we first state the HTTP Method (GET, POST), 
# then as an argument we pass the URL in, then we pass the auth token/cookie, then we pass in the JSON data,
# then finally tell the python requests module that we don't care if the APIC HTTP certificate is self-signed or not
#
# Go ahead, run these one at a time
# Make sure you have your APIC WebUI open to Fabric Access Policies, and have everything you see below expanded, so you can see it created in real-time

# This first one creates the VMM Domain
acipodvcenter = '10.29.10{0}.45'.format(acipod)
jsondata = {"vmmDomP":{"attributes":{"dn":"uni/vmmp-VMware/dom-T5-vCenter","enfPref":"hw","mcastAddr":"0.0.0.0","mode":"default","name":"T5-vCenter","ownerKey":"","ownerTag":""},"children":[{"vmmRsDefaultStpIfPol":{"attributes":{"tnStpIfPolName":"default"}}},{"vmmRsDefaultFwPol":{"attributes":{"tnNwsFwPolName":"default"}}},{"vmmRsDefaultLldpIfPol":{"attributes":{"tnLldpIfPolName":"default"}}},{"vmmCtrlrP":{"attributes":{"dvsVersion":"5.5","hostOrIp":acipodvcenter,"inventoryTrigSt":"untriggered","mode":"default","msftConfigIssues":"","name":"T5-VCSA","port":"0","rootContName":"Tenant5","scope":"vm","statsMode":"disabled"},"children":[{"vmmRsAcc":{"attributes":{"tDn":"uni/vmmp-VMware/dom-T5-vCenter/usracc-T5-admin"}}}]}},{"infraRsVlanNs":{"attributes":{"tDn":"uni/infra/vlanns-[T5-VMM-VLAN-Pool]-dynamic"}}},{"vmmRsDefaultCdpIfPol":{"attributes":{"tnCdpIfPolName":"default"}}},{"vmmRsDefaultLacpLagPol":{"attributes":{"tnLacpLagPolName":"default"}}},{"vmmRsDefaultL2InstPol":{"attributes":{"tnL2InstPolName":"default"}}},{"vmmUsrAccP":{"attributes":{"descr":"","name":"T5-admin","ownerKey":"","ownerTag":"","usr":"root"}}}]}}
r = s.post('https://{0}/api/node/mo/uni/vmmp-VMware/dom-T5-vCenter.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
print r.status_code
print r.text

# This next one creates the Interface Policy for 'CDP Disable' just in case we need it
jsondata = {"cdpIfPol":{"attributes":{"adminSt":"disabled","descr":"","dn":"uni/infra/cdpIfP-T5-CDP-disable","name":"T5-CDP-disable","ownerKey":"","ownerTag":""}}}
r = s.post('https://{0}/api/node/mo/uni/infra/cdpIfP-T5-CDP-disable.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
print r.status_code
print r.text

# This one creates the Interface Policy for 'CDP Enable' for our ESXi vSwitch from the Blade Servers up to the FIs
jsondata = {"cdpIfPol":{"attributes":{"adminSt":"enabled","descr":"","dn":"uni/infra/cdpIfP-T5-CDP-enable","name":"T5-CDP-enable","ownerKey":"","ownerTag":""}}}
r = s.post('https://{0}/api/node/mo/uni/infra/cdpIfP-T5-CDP-enable.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
print r.status_code
print r.text

# This one creates the Interface Policy for 'LLDP Disable' just in case we need it
jsondata = {"lldpIfPol":{"attributes":{"adminRxSt":"disabled","adminTxSt":"disabled","descr":"","dn":"uni/infra/lldpIfP-T5-LLDP-disable","name":"T5-LLDP-disable","ownerKey":"","ownerTag":""}}}
r = s.post('https://{0}/api/node/mo/uni/infra/lldpIfP-T5-LLDP-disable.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
print r.status_code
print r.text

# This one creates the Interface Policy for 'LLDP Enable' for our vPC from the Leafs down to the FIs
jsondata = {"lldpIfPol":{"attributes":{"adminRxSt":"enabled","adminTxSt":"enabled","descr":"","dn":"uni/infra/lldpIfP-T5-LLDP-enable","name":"T5-LLDP-enable","ownerKey":"","ownerTag":""}}}
r = s.post('https://{0}/api/node/mo/uni/infra/lldpIfP-T5-LLDP-enable.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
print r.status_code
print r.text

# This one creates the Interface Policy for 'LACP Active' for our vPC from the Leafs down to the FIs
jsondata = {"lacpLagPol":{"attributes":{"ctrl":"fast-sel-hot-stdby,graceful-conv,susp-individual","descr":"","dn":"uni/infra/lacplagp-T5-LACP-Active","maxLinks":"16","minLinks":"1","mode":"active","name":"T5-LACP-Active","ownerKey":"","ownerTag":""}}}
r = s.post('https://{0}/api/node/mo/uni/infra/lacplagp-T5-LACP-Active.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
print r.status_code
print r.text

# This one creates the Interface Policy for 'LACP MAC Pinning' for our ESXi vSwitch from the Blade Servers up to the FIs
jsondata = {"lacpLagPol":{"attributes":{"ctrl":"fast-sel-hot-stdby,graceful-conv,susp-individual","descr":"","dn":"uni/infra/lacplagp-T5-LACP-MacPinning","maxLinks":"16","minLinks":"1","mode":"mac-pin","name":"T5-LACP-MacPinning","ownerKey":"","ownerTag":""}}}
r = s.post('https://{0}/api/node/mo/uni/infra/lacplagp-T5-LACP-MacPinning.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
print r.status_code
print r.text

# This one creates the first Interface Policy Group for our vPC from both Leafs down to FI-A
jsondata = {"infraAccBndlGrp":{"attributes":{"descr":"","dn":"uni/infra/funcprof/accbundle-T5-vPC-FI-A-PG","lagT":"node","name":"T5-vPC-FI-A-PG","ownerKey":"","ownerTag":""},"children":[{"infraRsMonIfInfraPol":{"attributes":{"tnMonInfraPolName":""}}},{"infraRsLldpIfPol":{"attributes":{"tnLldpIfPolName":"T5-LLDP-enable"}}},{"infraRsStpIfPol":{"attributes":{"tnStpIfPolName":""}}},{"infraRsL2IfPol":{"attributes":{"tnL2IfPolName":""}}},{"infraRsCdpIfPol":{"attributes":{"tnCdpIfPolName":"T5-CDP-enable"}}},{"infraRsMcpIfPol":{"attributes":{"tnMcpIfPolName":""}}},{"infraRsAttEntP":{"attributes":{"tDn":"uni/infra/attentp-T5-VMM-AEP"}}},{"infraRsLacpPol":{"attributes":{"tnLacpLagPolName":"T5-LACP-Active"}}},{"infraRsStormctrlIfPol":{"attributes":{"tnStormctrlIfPolName":""}}},{"infraRsHIfPol":{"attributes":{"tnFabricHIfPolName":""}}}]}}
r = s.post('https://{0}/api/node/mo/uni/infra/funcprof/accbundle-T5-vPC-FI-A-PG.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
print r.status_code
print r.text

# This one creates the first Interface Policy Group for our vPC from both Leafs down to FI-B
jsondata = {"infraAccBndlGrp":{"attributes":{"descr":"","dn":"uni/infra/funcprof/accbundle-T5-vPC-FI-B-PG","lagT":"node","name":"T5-vPC-FI-B-PG","ownerKey":"","ownerTag":""},"children":[{"infraRsMonIfInfraPol":{"attributes":{"tnMonInfraPolName":""}}},{"infraRsLldpIfPol":{"attributes":{"tnLldpIfPolName":"T5-LLDP-enable"}}},{"infraRsStpIfPol":{"attributes":{"tnStpIfPolName":""}}},{"infraRsL2IfPol":{"attributes":{"tnL2IfPolName":""}}},{"infraRsCdpIfPol":{"attributes":{"tnCdpIfPolName":"T5-CDP-disable"}}},{"infraRsMcpIfPol":{"attributes":{"tnMcpIfPolName":""}}},{"infraRsAttEntP":{"attributes":{"tDn":"uni/infra/attentp-T5-VMM-AEP"}}},{"infraRsLacpPol":{"attributes":{"tnLacpLagPolName":"T5-LACP-Active"}}},{"infraRsStormctrlIfPol":{"attributes":{"tnStormctrlIfPolName":""}}},{"infraRsHIfPol":{"attributes":{"tnFabricHIfPolName":""}}}]}}
r = s.post('https://{0}/api/node/mo/uni/infra/funcprof/accbundle-T5-vPC-FI-B-PG.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
print r.status_code
print r.text

# This one creates the first Interface Profile and Interface Selector for our vPC from port eth1/11 down to FI-A that will eventually be mapped to both Leaf Switch Nodes
jsondata = {"infraAccPortP":{"attributes":{"descr":"","dn":"uni/infra/accportprof-T5-L101-L102-FI-A_ifselector","name":"T5-L101-L102-FI-A_ifselector","ownerKey":"","ownerTag":""},"children":[{"infraHPortS":{"attributes":{"descr":"","name":"T5-FI-A-Port11","ownerKey":"","ownerTag":"","type":"range"},"children":[{"infraRsAccBaseGrp":{"attributes":{"fexId":"101","tDn":"uni/infra/funcprof/accbundle-T5-vPC-FI-A-PG"}}},{"infraPortBlk":{"attributes":{"descr":"","fromCard":"1","fromPort":"9","name":"block2","toCard":"1","toPort":"9"}}}]}}]}}
r = s.post('https://{0}/api/node/mo/uni/infra/accportprof-T5-L101-L102-FI-A_ifselector.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
print r.status_code
print r.text

# This one creates the first Interface Profile and Interface Selector for our vPC from port eth1/12 down to FI-B that will eventually be mapped to both Leaf Switch Nodes
jsondata = {"infraAccPortP":{"attributes":{"descr":"","dn":"uni/infra/accportprof-T5-L101-L102-FI-B_ifselector","name":"T5-L101-L102-FI-B_ifselector","ownerKey":"","ownerTag":""},"children":[{"infraHPortS":{"attributes":{"descr":"","name":"T5-FI-B-Port12","ownerKey":"","ownerTag":"","type":"range"},"children":[{"infraRsAccBaseGrp":{"attributes":{"fexId":"101","tDn":"uni/infra/funcprof/accbundle-T5-vPC-FI-B-PG"}}},{"infraPortBlk":{"attributes":{"descr":"","fromCard":"1","fromPort":"10","name":"block2","toCard":"1","toPort":"10"}}}]}}]}}
r = s.post('https://{0}/api/node/mo/uni/infra/accportprof-T5-L101-L102-FI-B_ifselector.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
print r.status_code
print r.text

# This one creates the Dyanmic VLAN Pool
jsondata = {"fvnsVlanInstP":{"attributes":{"allocMode":"dynamic","descr":"","dn":"uni/infra/vlanns-[T5-VMM-VLAN-Pool]-dynamic","name":"T5-VMM-VLAN-Pool","ownerKey":"","ownerTag":""},"children":[{"fvnsEncapBlk":{"attributes":{"allocMode":"inherit","descr":"","from":"vlan-2150","name":"","to":"vlan-2159"}}}]}}
r = s.post('https://{0}/api/node/mo/uni/infra/vlanns-[T5-VMM-VLAN-Pool]-dynamic.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
print r.status_code
print r.text

# This one creates the Switch Profile for the switch block range of Node 101 to Node 102 and maps the both Interface Profiles down to FI-A and FI-B, respectively
jsondata = {"infraNodeP":{"attributes":{"descr":"","dn":"uni/infra/nprof-T5-L101-L102-FI-A-and-B_swprof","name":"T5-L101-L102-FI-A-and-B_swprof","ownerKey":"","ownerTag":""},"children":[{"infraLeafS":{"attributes":{"descr":"","name":"T5-L101-L102-FI-A-and-B_swsel","ownerKey":"","ownerTag":"","type":"range"},"children":[{"infraNodeBlk":{"attributes":{"descr":"","from_":"101","name":"0e4c30acf5d779c5","to_":"102"}}}]}},{"infraRsAccPortP":{"attributes":{"tDn":"uni/infra/accportprof-T5-L101-L102-FI-A_ifselector"}}},{"infraRsAccPortP":{"attributes":{"tDn":"uni/infra/accportprof-T5-L101-L102-FI-B_ifselector"}}}]}}
r = s.post('https://{0}/api/node/mo/uni/infra/nprof-T5-L101-L102-FI-B-SP.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
print r.status_code
print r.text

# This one creates the AEP and maps the vCenter to it, as well as creates the vSwitch Override Policy so that CDP Enabled, LLDP Disabled and MAC Pinning are all used
jsondata = {"infraAttEntityP":{"attributes":{"descr":"","dn":"uni/infra/attentp-T5-VMM-AEP","name":"T5-VMM-AEP","ownerKey":"","ownerTag":""},"children":[{"infraRsDomP":{"attributes":{"tDn":"uni/vmmp-VMware/dom-T5-vCenter"}}},{"infraAttPolicyGroup":{"attributes":{"descr":"","name":""},"children":[{"infraRsOverrideCdpIfPol":{"attributes":{"tnCdpIfPolName":"T5-CDP-enable"}}},{"infraRsOverrideLacpPol":{"attributes":{"tnLacpLagPolName":"T5-LACP-MacPinning"}}},{"infraRsOverrideLldpIfPol":{"attributes":{"tnLldpIfPolName":"T5-LLDP-disable"}}}]}}]}}
r = s.post('https://{0}/api/node/mo/uni/infra.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
print r.status_code
print r.text


# Before you do anything else, switch over to the Tenant tab, and MAKE SURE your Tenant is DELETED!

# This next one is the big'n
# No seriously, you have no idea how big this seemingly simple JSON data next line really is
# In fact, please take a moment to see how big it is
# Put your cursor right before the first curly brace, and SHIFT+END or whatever, but select and copy that whole line
# Next, open another Sublime Text tab with CTRL+N, and paste the whole thing
# Finally run JSON Pretty Print
# See at the bottom right, how many lines it is?
# 5,486 lines is what I count
# This is what an entire tenant (with NOT a ton of information in it contains)
# This tenant only has a few BDs, Subnets, EPGs, VRFs, etc
# However, it does have a few L4-7 Service Graphs created and deployed, with full parameters
# Go ahead, run it, and then explore ALL of what was created in the APIC
# Make sure you explore all of the L4-7 stuff, including expanding the EPGs and seeing the 'L4-7 Parameters' that are all populated there
# (Not all EPGs have L4-7 Params, so check them all)

# BTW, this one will take a LONG time to paste (like upwards of over a minute), and it is actually entirely possible that it will fail
# simply due to copy/paste buffer overflow
# If this happens, then now would be a good time to close the file, SSH into your Ubuntu Linux box,
# make sure it is git cloned to your /home/student directory, and run it using the CLI command
# 'python ./push-T6-apic-json-w-detailed-comments.py'  (without any quotes)

# That's it - you're done! 
