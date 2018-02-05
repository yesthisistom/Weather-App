__author__ = 'tv'


import Weather

from Geocode import Geocode

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def get_weather():

    geocoder = Geocode()

    if request.method == 'POST':
        if request.form['location']:

            location_in = request.form["location"]

            geocode_result = geocoder.geocode_anything(location_in)
            if geocode_result is None:
                flash("Unable to find location '{0}'".format(location_in))
                return render_template('index.html')

            location_str = geocode_result.get_address_str()
            weather = Weather.getWeather(geocode_result.latitude, geocode_result.longitude)

            if weather is None:
                flash("Unable to get weather for '{0}'".format(", ".join(location_str)))
                return render_template('index.html')

            return render_template('index.html', weather=weather, location=location_str)

        flash("Please enter a location")
        return render_template('index.html')
    else:
        ip = request.environ['REMOTE_ADDR']

        geocode_result = geocoder.geocode_ip(ip)
        if geocode_result:
            location_str = geocode_result.get_address_str()
            weather = Weather.getWeather(geocode_result.latitude, geocode_result.longitude)
            if weather:
                return render_template('index.html', weather=weather, location=location_str)

        return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'still butts'
    app.debug = True
    app.run(host='0.0.0.0', port=80)