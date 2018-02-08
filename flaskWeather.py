__author__ = 'tv'


import Weather

from Geocode import Geocode

from flask import Flask, render_template, request, redirect, url_for, flash, request

app = Flask(__name__)
app.secret_key = '0823##*_OJKH*Gjjuu&&&55(*&(*&(7^%%'

@app.route("/", methods=['GET', 'POST'])
def get_weather():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    geocoder = Geocode()

    if request.method == 'POST':
        if request.form['location']:

            location_in = request.form["location"]

            geocode_result = geocoder.geocode_anything(location_in)
            if geocode_result is None:
                flash("Unable to find location '{0}'".format(location_in))

                return render_template('index.html', ip=ip)

            weather = Weather.getWeather(geocode_result.latitude, geocode_result.longitude)

            if weather is None:
                flash("Unable to get weather for '{0}'".format(geocode_result.get_address_str()))
                return render_template('index.html', ip=ip, geocode=geocode_result)

            return render_template('index.html', weather=weather, ip=ip, geocode=geocode_result)

        flash("Please enter a location")
        return render_template('index.html')
    else:

        geocode_result = geocoder.geocode_ip(ip)
        if geocode_result:
            weather = Weather.getWeather(geocode_result.latitude, geocode_result.longitude)
            if weather:
                return render_template('index.html', weather=weather, ip=ip, geocode=geocode_result)

        return render_template('index.html', ip=ip)

if __name__ == '__main__':
    
    app.debug = True
    app.run(host='0.0.0.0', port=80)