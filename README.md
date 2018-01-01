# Txt-Loc-Viz
Visualizing Locations in text

## Overview

### This Flask application performs the following:
Input text from screen, file or website is processed using NLTK Stanford NER Tagger to identify and tag Locations.
The tagged locations are then chunked, in cases where the location is a multi word term (“New York City” for example).
This output is processed to produce an HTML file where locations are <mark>ed to create a visualization of locations highlighted in the text.
Each location is also sent to a geolocator that returns its coordinates. The coordinates are sent through Google maps API to produce a map with the locations pinned.


## Installing the application and dependencies

Download and install python 2.7 - https://www.python.org/downloads/

Install Flask - http://flask.pocoo.org/docs/0.12/installation/#installation

Install NLTK - http://www.nltk.org/install.html

Install Stanford NER Tagger - https://nlp.stanford.edu/software/stanford-ner-2017-06-09.zip
(unzip and note the folder where the tagger is installed for the update required below)

Install geopy - https://pypi.python.org/pypi/geopy

Get Google API key: https://developers.google.com/maps/documentation/javascript/get-api-key
(note the API key you obtained for the update required below)

Download the Txt-Loc-Viz application code from github <link>

Unzip into a folder

## Updates

Enter the directory where you installed tagger in step 4 into the parameter stanford_dir in the file Run27geo.py where marked

Enter the API key you obtained in step 6 into these files where marked: R_url.html, R_file.html, R_text.html

## Usage

Open terminal/command prompt

Navigate to the folder

Run the application
```bash
python Run27geo.py
```

In a browser go to: localhost:5000 to use the application

### In case the geolocator sends an error (connection blocked or timeout)
Please try again. If you still get an error, please navigate your browser to localhost:5000/map and you can see the results that were received until the service sent an error. (This is a free service and it sometimes blocks or times out despite us following the terms of service.)


## Team members contributions 

### Hadas
Project idea and proposal, datasets, NLTK tokenizing, entity tagging, and chunking, Flask application (URL component), UI design and CSS, HTML and text visualization, integration, testing, bug fixes, documentation and presentation.
### QuanXin
Datasets, Flask application (text and file components), NLTK tokenizing, entity tagging, and chunking, Python code, Geopy geolocator, Google map API and map visualization, testing, bug fixes, documentation.
