WriteBetter
===========
A [Flask](http://flask.pocoo.org/) app to analyze writing samples, powered by [NLTK](http://www.nltk.org/) for analysis 
and [Bootstrap](https://getbootstrap.com/) for UI.

It has the following features:
- Show adjectives and adverbs
- Show all parts of speech
- Count words and characters

Visit [WriteBetter on Google Cloud](https://bsravan.in/write-better) to try it yourself.

![Demo](https://drive.google.com/uc?id=1VR5f-32TcnjOz5-Y9B2P0sbte4Dmq3yY)

Installation
------------
1. Clone or download [the code](https://github.com/bsravanin/WriteBetter).
1. Run the following commands from a terminal:
   1. `cd WriteBetter`
   1. `tox`
   1. `source .tox/py37/bin/activate`
   1. `FLASK_APP=./write_better/write_better.py flask run`
1. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in a browser.

*NOTE*: I wrote this using Python v3.7.0, but I suspect it will work fine for any Python that can install 
[the requirements](https://github.com/bsravanin/WriteBetter/blob/master/requirements.txt) with trivial changes.

Security
--------
1. To style the analyzed text, the Flask template uses a "|safe" filter, assuming that the generated text is safe to
   be interpreted as is. This assumption may be false under certain unusual circumstances that I cannot elaborate
   on (due to my ignorance). If the writing sample is plain English, I wouldn't worry about it. Otherwise, I hope you
   know what you are doing.
1. The secret key of this Flask app has been hard-coded to "not_really_secret". This is safe if you are both running
   the app and using it. If someone else is running it (like, online), I would think twice about submitting my novel
   that I hope to profit from some day.

Related
-------
- [NLTK Demos](http://text-processing.com/demo)
- [iA Writer](https://ia.net/writer)
- [English Syntax Highlighter](https://english.edward.io)
- [Parts-of-speech.info](https://parts-of-speech.info)
