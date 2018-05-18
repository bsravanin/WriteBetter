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
    show_adjectives = BooleanField('Show Adjectives', default=False)


@app.route('/', methods=['GET', 'POST'])
def submit_manuscript():
    app.logger.debug(request.form)
    form = WriterForm(request.form)
    if request.method == 'POST':
        submitted = request.form.get('submitted')
        show_adjectives = request.form.get('show_adjectives', False)
        analyzed = analyze.get_analyzed_text(submitted=submitted, show_adjectives=show_adjectives)
        return render_template('form.html', form=form, submitted=submitted, analyzed=analyzed)
    else:
        return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run()
