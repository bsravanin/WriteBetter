"""Entry point into the app."""
import os
import nltk

from flask import Flask, render_template, request
from wtforms import Form, SelectField, TextAreaField

from write_better.analyze import Analysis


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'not_really_secret'

NLTK_ROOT = os.path.join(os.path.dirname(__file__), 'static', 'nltk_data')


class WriterForm(Form):
    submitted = TextAreaField('Submitted')
    analyzed = TextAreaField('Analyzed')
    show = SelectField(choices=[('show_ads', 'Adjectives & Adverbs'), ('show_pos', 'All Parts of Speech')])


@app.route('/', methods=['GET', 'POST'])
def submit_manuscript():
    if nltk.data.path[-1] != NLTK_ROOT:
        app.logger.info('Adding %s to NLTK data path.', NLTK_ROOT)
        nltk.data.path.append(NLTK_ROOT)

    # app.logger.debug(request.form)
    form = WriterForm(request.form)
    if request.method == 'POST':
        submitted = request.form.get('submitted')
        show_ads = request.form.get('show') == 'show_ads'
        show_pos = request.form.get('show') == 'show_pos'
        analysis = Analysis(submitted)
        analyzed = analysis.recombine(show_ads=show_ads, show_pos=show_pos)
        return render_template('form.html', form=form, submitted=submitted, analyzed=analyzed,
                               word_count=analysis.token_count, char_count=analysis.char_count,
                               show_ads=show_ads, show_pos=show_pos)
    else:
        return render_template('form.html', form=form)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
