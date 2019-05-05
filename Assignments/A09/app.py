from flask import Flask,request
from datetime import datetime
import re
from flask import render_template
import youtube_dl

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('extensionhome.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    name = request.form['name']
    extension = request.form['extension']
    ydl_opts = {
        'format': 'bestaudio/best',       
        'outtmpl': '%s.%s'%(name,extension),        
        'noplaylist' : True, 
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([text])
    #downloadVid('https://www.youtube.com/watch?v=P88dK4BRYN4','Got Your Back','mp3')

    processed_text = text.upper()
    return processed_text
    '''now = datetime.now()
    formatted_now = now.strftime("%a, %d %b, %y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content
    '''