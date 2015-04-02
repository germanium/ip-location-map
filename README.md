# ip-location-map

Plot the location of failed login attempts made to a computer with an opened ssh port.

### Dependencies:

* [matplotlib basemap](http://matplotlib.org/basemap/)
* [pyipinfodb](https://github.com/mossberg/pyipinfodb)


### Short usage guide:

* First, you need to get an API key for [ipinfodb](http://ipinfodb.com/), and insert it in **getlocation.py**.

* Set the variables `logFile` with the path to the log file, which depends on your system---for most Linux systems is 'var/log/auth.log'. Set `failStr` with is the string that appears in the line of a failed login attempt before the IP address in the log file.

* Finally, run the **getlocation.py** script. It will fetch the IP addresses from the log file and find its geolocation. It will then plot it on a map.

#### Map

Resulting map

![Map](ip_map.png)