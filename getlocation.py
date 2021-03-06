#!/usr/bin/env python
import re
import sys
import time
import matplotlib.pyplot as plt
from pyipinfodb import pyipinfodb
from mpl_toolkits.basemap import Basemap
from KEY import API_KEY


ip_lookup = pyipinfodb.IPInfo(API_KEY)
logFile = '/var/log/auth.log'   # Default log file
failStr = 'Failed password'     # String in the log file indicating a failed login attempt


def geoLocate(IPs):

    coord_list = []     # List of tuples containing coordinates as (Longitude, Latitude)
    cache = {}          # Dict containing data from IPs that have already been requested from the API

    for ip in IPs:

        if ip not in cache:
            print('Getting location for {}'.format(ip))
            ip_data = ip_lookup.get_city(ip)
            cache[ip] = ip_data
        else:
            ip_data = cache[ip]

        coord_list.append({'IP': ip,
                           'long': ip_data['longitude'],
                           'lat': ip_data['latitude']})
        time.sleep(0.01)    # If it fetches too fast it gives error
    return coord_list


def getIPs(filename=logFile, matchStr=failStr):
    '''
    Parse IPs from log logfile
    '''
    pattern = r'(?<='+matchStr+r').*(\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b)'
    compile_obj = re.compile(pattern)

    file2read = open(filename, 'r')
    IPs = []
    for currentline in file2read:
        match_obj = compile_obj.search(currentline)
        if match_obj:
            IPs.append(match_obj.group(1))

    file2read.close()

    return IPs


def generateMap(coord_list):
    '''
    Generate map with IP locations.
    coord_list is a list of dictionaries with keys 'long' and 'lat'
    '''

    ip_map = Basemap(projection='robin', lon_0=0, resolution='c')

    for line in coord_list:
        x, y = ip_map(float(line['long']), float(line['lat']))
        plt.plot(x, y, 'o', color='#ff0000', ms=2.7, markeredgewidth=0.5)

    ip_map.drawcountries(color='#ffffff')
    ip_map.fillcontinents(color='#cccccc', lake_color='#ffffff')

#    plt.savefig('ip_map.png', dpi=600)
    plt.show()


if __name__ == '__main__':
    print("""Usage: First argument should be a log file.
        By default it uses %s""" % logFile)
    if len(sys.argv) == 2:          # Use input source
        logFile = sys.argv[1]
        print("Using %s" % logFile)
    IPs = getIPs(filename=logFile)
    coord_list = geoLocate(IPs)
    generateMap(coord_list)
