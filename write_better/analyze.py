"""The core of the manuscript analysis."""
import logging

from io import StringIO

from nltk import pos_tag
from nltk.tokenize import word_tokenize


logging.basicConfig(format='%(asctime)s %(levelname)s [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s',
                    level=logging.DEBUG)


class Analysis(object):
    def __init__(self, submitted: str):
        self.submitted = submitted
        self._tokens = None
        self._tags = None

    @property
    def tokens(self) -> list:
        if self._tokens is None:
            self._tokens = word_tokenize(self.submitted)
        return self._tokens

    @property
    def tags(self) -> list:
        if self._tags is None:
            self._tags = pos_tag(self.tokens)
        return self._tags

    @property
    def token_count(self) -> int:
        return len(self.tokens)

    @property
    def char_count(self) -> int:
        return len(self.submitted)

    def recombine(self, show_adjectives: bool=False) -> str:
        with StringIO() as sfd:
            index = 0
            for tnum, token in enumerate(self.tokens):
                if token in ['``', "''"]:
                    # Refer https://stackoverflow.com/a/32197336.
                    token = '"'
                while True:
                    if index >= self.char_count:
                        logging.error('Index: %s, token: "%s"', index, token)
                        break
                    elif token.startswith(self.submitted[index]):
                        if show_adjectives and self.tags[tnum][1] in ['JJ', 'JJR', 'JJS']:
                            sfd.write('<span class="{}">{}</span>'.format(self.tags[tnum][1], token))
                        else:
                            sfd.write(token)
                        index += len(token)
                        break
                    else:
                        sfd.write(self.submitted[index].replace('\n', '<br>'))
                        index += 1
            sfd.write(self.submitted[index:])
            return sfd.getvalue()


def get_analyzed_text(submitted: str, show_adjectives: bool=False) -> str:
    logging.debug('Submitted: %s\nshow_adjectives: %s', submitted, show_adjectives)
    analysis = Analysis(submitted)
    result = analysis.recombine(show_adjectives=show_adjectives)
    logging.debug('Result: %s', result)
    return result
