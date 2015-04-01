#!/usr/bin/env python
from pyipinfodb import pyipinfodb
import re
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


ip_lookup = pyipinfodb.IPInfo(<API_KEY>)


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
    return coord_list


def getIPs(filename='/var/log/auth.log'):
    '''
    Parse IPs from /var/log/auth.log
    '''
    pattern = r'(\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b)'
    compile_obj = re.compile(pattern)

    file2read = open(filename, 'r')
    IPs = []
    for currentline in file2read:
        match_obj = compile_obj.search(currentline)
        if match_obj:
            # set addy to matched ip - change this to 2 if you use the pattern above to find Accepted password string
            IPs.append(match_obj.group(1))

    file2read.close()

    return IPs


def generateMap(coord_list):
    """
    Generate map with IP locations. 
    coord_list is a list of dictionaries with keys 'long' and 'lat'
    """

    ip_map = Basemap(projection='robin', lon_0=0, resolution='c')

    for line in coord_list:
        x, y = ip_map(float(line['long']), float(line['lat']))
        plt.plot(x,y, 'o', color='#ff0000', ms=2.7, markeredgewidth=0.5)

    ip_map.drawcountries(color='#ffffff')
    ip_map.fillcontinents(color='#cccccc', lake_color='#ffffff')

    plt.savefig('ip_map.png', dpi=600)


if __name__ == '__main__':
    IPs = getIPs()
    coord_list = geoLocate(IPs)
    generateMap(coord_list)
