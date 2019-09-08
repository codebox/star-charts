# Star Charts

This Python script will generate SVG star charts, like the ones shown below:

<img src="https://codebox.net/assets/images/star-charts-with-python/orion.png" height="480px" width="480px" alt="Star Chart showing Orion" /><br>
<sup>The constellation Orion, showing stars down to magnitude 8 [original SVG](https://codebox.net/assets/images/star-charts-with-python/orion.svg)</sup>

The script reads data about the position and brightness of stars from a CSV file like [this one](https://raw.githubusercontent.com/codebox/star-charts/master/stardata.csv).
Each row in the CSV file contains information about a single star in 4 columns as follows:

* <b>Right-Ascension</b>: the star's angular distance eastward from the vernal equinox (0 to 24)
* <b>Declination</b>: the star's angular distance northward from the celestial equator (-90 to +90)
* <b>Magnitude</b>: the star's brightness
* <b>Label</b>: an optional field used to add labels to stars (see the Greek letters in the example chart above)

For example

```
5.91937636,+76.86957095, 8.07
5.91952477,+07.40703634, 0.45,α
5.92011402,+61.86673905, 8.60
5.92045102,-73.15075170, 7.72
```

The area to be covered by the chart is specified using a <a href="https://github.com/codebox/star-charts/blob/master/sky_area.py">SkyArea</a> object, which must be <a href="https://github.com/codebox/star-charts/blob/master/main.py#L9">referenced the main.py file</a>. A few pre-defined areas are included, such as complete northern and southern sky maps:

<img src="https://codebox.net/assets/images/star-charts-with-python/northern_sky.png" height="420px" width="420px" class="" alt="Star Chart showing the northern sky" />
<img src="https://codebox.net/assets/images/star-charts-with-python/southern_sky.png" height="420px" width="420px" class="" alt="Star Chart showing the southern sky" />

<sup>Maps of the Northern and Southern skies, showing stars down to magnitude 7 (original SVGs: [North](https://codebox.net/assets/images/star-charts-with-python/northern_sky.svg) and [South](https://codebox.net/assets/images/star-charts-with-python/southern_sky.svg)</sup>

The script is run by simply executing the main.py file, as follows:

```
python main.py
```

The SVG file will be created in the current directory, and will be named <b>star-chart.svg</b>

Please note that the script is designed to be run using <b>Python 3</b>, it will not run correctly with Python 2.
