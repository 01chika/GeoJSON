import urllib.request, urllib.parse, urllib.error
import json
import time
import ssl

api_key = False
# Enter Google API Key here if available
# api_key = 'AAQ7JS...h7UT70'
# https://developers.google.com/maps/documentation/geocoding/intro

if api_key is False:
    api_key= 42
    serviceurl = 'http://py4e-data.dr-chuck.net/json?'          #use if googele API key isn't available; service provided by Dr. Charles Severance from py4e.com
else:
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

#ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    address = input ('Enter location: ')
    print('\n')  #inserted new line for neater output
    if len(address) < 1:
        break
    parms = dict()
    parms['address'] = address
    if api_key is not False:
        parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)

    #print('Retrieving', url)                       **optional for visualization**
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    #print('Retrieved', len(data), 'characters')    **optional for visualization**

    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'status' not in js or js['status'] != 'OK':
        print('====Failure To Retrieve====')
        print(data)
        continue

    #print(json.dumps(js, indent=4))
    location = js['results'][0]['formatted_address']                                 #traverses the JSON to get the city, country info
    print ("Your location: {} \n".format(location))
    lat = js['results'][0]['geometry']['location']['lat']
    lng = js['results'][0]['geometry']['location']['lng']
    print('LATITUDE: {} LONGITUDE: {} \n'.format(lat, lng))                          #traverses the JSON to get the LAT/LNG data
    
    
    print ("<--- Would you like to save the retrieved geographical? ---> \n")
    print("Input 'YES' if you would like to save \nInput 'NO' if you don't want to save \n")

    reply = input("-> ")
    reply = reply.upper()

    if reply == "YES":
        fout = open('data.json', 'w')
        x = fout.write((json.dumps(js, indent=4)))                          #writes indented JSON data to data.json file
        fout.close()
        print("\n<---Congrats! Your file has been successfully saved as 'data.json'--->")

    elif reply == "NO":
        print ("\n<--- Would you like to perform another quick search? ---> \n")
        print("Input 0 if you want to perform another search \nInput 1 if you would like to exit the program\n")

        reply_2 = input("-> ")

        if reply_2 == "0":                                          #nested conditional determine if user
            continue                                                #wants to perform another search or exit
        elif reply_2 == "1":
            print ("\nThank you for using this program!")
            time.sleep(2)
            quit()  
    else:
        print("\nInvalid input")
        time.sleep(2)
        quit()
