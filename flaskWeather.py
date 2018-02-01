__author__ = 'tv'

import Weather

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def getWeather():

    if request.method == 'POST':
        if request.form['location']:
            lat = request.form['location'].split(",")[0]
            lon = request.form['location'].split(",")[1]
            weather = Weather.getWeather(lat, lon)

            return render_template('index.html', weather = weather)

        return "No location?"
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)