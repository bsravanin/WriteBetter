"""Entry point into the app."""
from flask import Flask, render_template, request
from wtforms import Form, BooleanField, TextAreaField

from write_better import analyze


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'not_really_secret'


class WriterForm(Form):
    submitted = TextAreaField('Submitted')
    analyzed = TextAreaField('Analyzed')
    show_ads = BooleanField('Show Adjectives & Adverbs', default=False)
    pos_tag = BooleanField('Show all POS', default=False)


@app.route('/', methods=['GET', 'POST'])
def submit_manuscript():
    app.logger.debug(request.form)
    form = WriterForm(request.form)
    if request.method == 'POST':
        submitted = request.form.get('submitted')
        show_ads = request.form.get('show_ads', False)
        pos_tag = request.form.get('pos_tag', False)
        analyzed = analyze.get_analyzed_text(submitted=submitted, show_ads=show_ads, pos_tag=pos_tag)
        return render_template('form.html', form=form, submitted=submitted, analyzed=analyzed)
    else:
        return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run()
