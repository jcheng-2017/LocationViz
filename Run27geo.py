import os
import time
import urllib2
import nltk
from nltk.tag import StanfordNERTagger
from flask import Flask, render_template, request, redirect, url_for
from itertools import groupby
from geopy.geocoders import Nominatim
from HTMLParser import HTMLParser

'''
************************************************************************************
The user needs to set up the path to local directory where Stanford-NER is installed
for example: stanford_dir = '/Users/<username>/stanford-ner-2017-06-09/'
************************************************************************************
'''
stanford_dir = '/Users/hadas/stanford-ner-2017-06-09/'
jarfile = stanford_dir + 'stanford-ner.jar'
modelfile = stanford_dir + 'classifiers/english.all.3class.distsim.crf.ser.gz'
st = StanfordNERTagger(model_filename=modelfile, path_to_jar=jarfile)

app = Flask(__name__)


'''
Strip HTML tags from a web site
'''


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


@app.route('/', methods=['GET', 'POST'])
def home():
    '''
    The application home page
    '''
    if request.method == 'POST':
        selectedValue = request.form['selection']
        return redirect(url_for('click', selectedValue=selectedValue))
    return render_template('main.html')


@app.route('/map', methods=['GET', 'POST'])
def map1():
    '''
    The application results page
    '''
    return render_template('map.html')


@app.route('/<selectedValue>', methods=['GET', 'POST'])
def click(selectedValue):
    '''
    Route to a page template based on user's selection
    '''
    return render_template(selectedValue + '.html')


def process_locations(netagged_words):
    netagged_words = netagged_words
    '''
    Set up root for files paths
    '''
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    '''
    Chunk the tagged locartions and
    write them into an TXT file as input to map Visualization
    '''
    with open(ROOT_DIR + '/output/' + 'output1.txt', 'w') as f:
        for tag, chunk in groupby(netagged_words, lambda x: x[1]):
            if tag == 'LOCATION':
                f.write(u' '.join(c[0] for c in chunk).encode('utf-8').strip() + '\n')
    f.close()

    '''
    write the text and marked locations into an HTML file for text visualization
    '''
    with open(ROOT_DIR + '/templates/' + 'locations.html', 'w') as f1:
        f1.write('<html>' + '\n')
        f1.write('<head>' + '\n')
        f1.write('<link rel=\"stylesheet\" href=\"http://127.0.0.1:5000/static/style.css\">' + '\n')
        f1.write('</head>' + '\n')
        f1.write('<body>' + '\n')
        f1.write('<div class="entities">' + '\n')
        for tag, chunk in groupby(netagged_words, lambda x: x[1]):
            if tag == 'LOCATION':
                f1.write('<mark data-entity=\"loc\">' +
                         u' '.join(c[0] for c in chunk).encode('utf-8').strip() + '</mark>' + '\n')
            else:
                f1.write(u' '.join(c[0] for c in chunk).encode('utf-8').strip())
        f1.write('</div>' + '\n')
        f1.write('</body>' + '\n')
        f1.write('</html>' + '\n')
    f1.close()

    '''
    find and write the locations' coordinated into an TXT file for map visualization
    '''
    with open(ROOT_DIR + '/output/' + 'output1.txt', 'r') as filestream:
        with open(ROOT_DIR + '/templates/' + 'output_cor1.html', 'w') as filestreamtwo:
            for line in filestream:
                s = line.strip()
                print s
                geolocator = Nominatim()
                time.sleep(1)
                location = geolocator.geocode(s, timeout=None)
                if location is not None:
                    x = location.latitude
                    y = location.longitude
                    filestreamtwo.write(str(x) + "," + str(y) + "\n")
    return


@app.route('/R_txt', methods=['POST'])
def my_form_post():
    '''
    Get the text manually entered into the form
    Use NLTK to tokenize and tag the entity words in the input text
    Send the tagged words for processing
    Return the visualization
    '''
    text1 = request.form['myText']
    netagged_words = st.tag(nltk.word_tokenize(text1))
    process_locations(netagged_words)
    return render_template('map.html')


@app.route('/R_file', methods=['POST'])
def my_form_post1():
    '''
    Read the text from the file entered into the form
    Use NLTK to tokenize and tag the entity words in the input text
    Send the tagged words for processing
    Return the visualization
    '''
    text = request.form['myFile']
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(ROOT_DIR + '/dataset/' + text, "r") as myfile:
        doc = myfile.read().replace('\n', ' ').decode('unicode-escape')
    myfile.close()
    netagged_words = st.tag(nltk.word_tokenize(doc))
    process_locations(netagged_words)
    return render_template('map.html')


@app.route('/R_url', methods=['POST'])
def my_form_post2():
    '''
    try to strip html tags for better visualization of text using strip_tags(html)
    not working well... need web scraping.
    '''
    text = request.form['myurl']
    netagged_words = st.tag(nltk.word_tokenize(
        strip_tags(urllib2.urlopen(str(text)).read().decode('unicode-escape'))))
    process_locations(netagged_words)
    return render_template('map.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
