#!/bin/env python3
#
# Author: Created by Aaron "Dirty" Bennett in 2015
# Author: Maintained by Joss Malasuk
from flask import Flask, render_template
from flask import request
import geoip2.database
import ipaddress
import json

app = Flask(__name__)
# Must download geoip binary database from the link below
# http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
reader = geoip2.database.Reader('/var/www/wherediz.com/web/GeoLite2-City.mmdb') 

txt_version = "1.0.0"
new_line = "\n"
txt_help = "/[ip] - Shows the location of the IP Address \n/json/[ip] - Provide a little more information in json format\n/help - Show this message\n/about - About this project\n"
txt_about = "Created by Aaron 'Dirty' Bennett in 2015\nFor more information please visit wherediz.com\n"

txt_error_not_valid_ip = " is not a valid IPv4 address. ?_?"
txt_error_unknown = "Unknown"

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/help")
def help():    
    return txt_help

@app.route("/about")
def about():
    return txt_about

@app.route("/version")
def version():
    return txt_version

@app.route("/debug")
def debug():
    useragent = request.headers.get('User-Agent')
    return useragent

@app.route("/<ip>")
def ipfind(ip):
    try:
        response = reader.city(ip)
        country = response.country.name
        area = response.subdivisions.most_specific.name
        city = response.city.name
        #reader.close()
        thestring = '{}, {}, {}'.format(city, area, country)
        if city is None and area is None:
            # returning only country
            return ip + ': ' + country + new_line
        else:
            return ip + ': ' + thestring + new_line
    except ValueError:
        # Not a valid IP
        return "'{}'".format(ip) + txt_error_not_valid_ip + new_line
    except:
        # Cannot find location IP.  May be an internal IP or other error
        return ip + ': ' + txt_error_unknown + new_line

@app.route("/json/<jip>")
def jsonipfind(jip):
    try:
        response = reader.city(jip)
        country = response.country.name
        state = response.subdivisions.most_specific.name
        city = response.city.name
        postal = response.postal.code

        # Validation
        if country is None:
            country = txt_error_unknown
        if state is None:
            state = txt_error_unknown
        if city is None:
            city = txt_error_unknown
        if postal is None:
            postal = txt_error_unknown
        
        jsonOutput = json.dumps({'IP':jip,'Country':country,'State':state,'City':city,'Zip':postal},indent=4, separators=(',', ': '))
        return jsonOutput + new_line
    except ValueError:
        # Not a valid IP
        return "'{}'".format(ip) + txt_error_not_valid_ip + new_line
    except:
        # Cannot find location IP.  May be an internal IP or other error
        return ip + ': ' + txt_error_unknown + new_line

if __name__ == "__main__":
    app.debug = False
    app.run(host='127.0.0.1',port=5000)
