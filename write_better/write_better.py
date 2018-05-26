"""Entry point into the app."""
from flask import Flask, render_template, request
from wtforms import Form, SelectField, TextAreaField

from write_better.analyze import Analysis


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'not_really_secret'


class WriterForm(Form):
    submitted = TextAreaField('Submitted')
    analyzed = TextAreaField('Analyzed')
    show = SelectField(choices=[('show_ads', 'Adjectives & Adverbs'), ('show_pos', 'All Parts of Speech')])


@app.route('/', methods=['GET', 'POST'])
def submit_manuscript():
    app.logger.debug(request.form)
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


if __name__ == '__main__':
    app.run()
