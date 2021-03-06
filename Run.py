import os
import nltk
import urllib.request as ur
from pathlib import Path
from nltk.tag import StanfordNERTagger
from flask import Flask, render_template, request, redirect, url_for
from itertools import groupby
from nltk import ne_chunk, pos_tag, word_tokenize
from geopy.geocoders import Nominatim


java_path = "/Program Files/Java/jre1.8.0_40/bin/java.exe"
os.environ['JAVAHOME'] = java_path

# path to local directory where Stanfprd-NER is installed
# stanford_dir = '/Users/<username>/stanford-ner-2017-06-09/'
stanford_dir = '/Users/grant/stanford-ner-2017-06-09/'
jarfile = stanford_dir + 'stanford-ner.jar'
modelfile = stanford_dir + 'classifiers/english.all.3class.distsim.crf.ser.gz'
st = StanfordNERTagger(modelfile, path_to_jar=jarfile)


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selectedValue = request.form['selection']
        return redirect(url_for('click', selectedValue=selectedValue))
    return render_template('main.html')

@app.route('/main', methods=['GET', 'POST'])
def home1():
    if request.method == 'POST':
        selectedValue = request.form['selection']
        return redirect(url_for('click', selectedValue=selectedValue))
    return render_template('main.html')



@app.route('/<selectedValue>', methods=['GET', 'POST'])
def click(selectedValue):
    return render_template(selectedValue + '.html')


@app.route('/R_txt', methods = ['POST'])
def my_form_post():
  text1 = request.form['myText']
  ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
  home = str(Path.home())
  if request.form['options'] == "option1":

        ne_text=[]
   
        with open(home +'/anaconda3/lib/site-packages/flask/LocationViz/output/'+ 'output1.txt','w') as f:
           for sent in nltk.sent_tokenize(text1):
               for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                 if hasattr(chunk, 'label'):
	             #print(chunk.label(), ' '.join(c[0] for c in chunk))
                    f.write(' '.join(c[0] for c in chunk)+ "\n")
                    ne_text.append (' '.join(c[0] for c in chunk))     
        return str(ne_text) 

  if request.form['options'] == "option2":
        with open(home +'/anaconda3/lib/site-packages/flask/LocationViz/output/'+ 'output1.txt', 'r') as filestream:
            with open(home +'/anaconda3/lib/site-packages/flask/LocationViz/templates/'+ 'output_cor1.html', 'w') as filestreamtwo:
              for line in filestream:
                try:
                  s=line.strip()
                  geolocator = Nominatim()
                  location = geolocator.geocode(s)
                  ad = location.address               
                  x = location.latitude
                  y = location.longitude
                  print (location.address)
                  print(location.latitude, location.longitude)
                  #filestreamtwo.write(str(ad)+ "," + str(x) + "," + str(y) + "," + "\n") 
                  filestreamtwo.write(str(x) + "," + str(y) + "\n") 
                except: 
                  #print ('error, skipping address...')
                  filestreamtwo.write('error, skipping address' + "\n")   
        return ("Map is ready, please click Fresh button")        
      

@app.route('/R_file', methods=['POST'])
def my_form_post1():
  text = request.form['myFile']
  home = str(Path.home())

  if request.form['options'] == "option1":
    fname = os.path.basename(text)
    fdir1 = os.path.dirname (text)
    fpath1= os.path.realpath(text)       
    file = open(home +'/anaconda3/lib/site-packages/flask/LocationViz/dataset'+ '/'+ fname, 'r')
    my_sent = file.read()
    file.close()
    ne_text1=[]

  
    with open(home +'/anaconda3/lib/site-packages/flask/LocationViz/output/' + 'output2.txt','w') as f:
        for sent in nltk.sent_tokenize(my_sent):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            #if hasattr(chunk, 'label'):
               if hasattr(chunk,'label') and chunk.label() == 'GPE':
               #print(chunk.label(), ' '.join(c[0] for c in chunk))
                #print(''.join(c[0] for c in chunk))
                 f.write(' '.join(c[0] for c in chunk)+ "\n")            
                 ne_text1.append (' '.join(c[0] for c in chunk))     
    return str(ne_text1)
    
  if request.form['options'] == "option2":
        
        with open(home +'/anaconda3/lib/site-packages/flask/LocationViz/output/'+ 'output2.txt','r') as filestream:
            with open(home +'/anaconda3/lib/site-packages/flask/LocationViz/templates/'+ 'output_cor2.html', 'w') as filestreamtwo:
              for line in filestream:
                try:
                  s=line.strip()
                  geolocator = Nominatim()
                  location = geolocator.geocode(s)
                  ad = location.address               
                  x = location.latitude
                  y = location.longitude
                  print (location.address)
                  print(location.latitude, location.longitude)
                  #filestreamtwo.write(str(ad)+ "," + str(x) + "," + str(y) + "," + "\n") 
                  filestreamtwo.write(str(x) + "," + str(y) + "\n") 
                except: 
                  #print ('error, skipping address...')
                  filestreamtwo.write('error, skipping address' + "\n")   
        return ("Map is ready, please click Fresh button")             

@app.route('/R_url', methods=['POST'])
def my_form_post2():
    text = request.form['myurl']
    home = str(Path.home())
    ne_text2 = []
    netagged_words = st.tag(ur.urlopen(str(text)).read().decode('unicode-escape').split())
    
    if request.form['options'] == "option1":
      with open(home +'/anaconda3/lib/site-packages/flask/LocationViz/output/'+ 'output3.txt','w') as f:     
        for tag, chunk in groupby(netagged_words, lambda x: x[1]):
        	if tag == "LOCATION":  
        	  add_text = "".join(w for w, t in chunk)  
        	  f.write(add_text + "\n")
        	  ne_text2.append(add_text)
        return str(ne_text2)
        	  
        	  
    if request.form['options'] == "option2":
      with open(home +'/anaconda3/lib/site-packages/flask/LocationViz/output/'+ 'output3.txt', 'r') as filestream:
        with open(home +'/anaconda3/lib/site-packages/flask/LocationViz/templates/'+ 'output_cor3.html', 'w') as filestreamtwo:
              for line in filestream:
                try:
                  s=line.strip()
                  geolocator = Nominatim()
                  location = geolocator.geocode(s)
                  ad = location.address               
                  x = location.latitude
                  y = location.longitude
                  print (location.address)
                  print(location.latitude, location.longitude)
                  #filestreamtwo.write(str(ad)+ "," + str(x) + "," + str(y) + "," + "\n") 
                  filestreamtwo.write(str(x) + "," + str(y) + "\n") 
                except: 
                  #print ('error, skipping address...')
                  filestreamtwo.write('error, skipping address' + "\n")   
      return ("Map is ready, please click Fresh button")        
 
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)