"""The core of the manuscript analysis."""
import logging

from io import StringIO

from nltk import pos_tag
from nltk.tokenize import word_tokenize


logging.basicConfig(
    format='%(asctime)s %(levelname)s [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s', level=logging.DEBUG
)
ADJECTIVES = frozenset({'JJ', 'JJR', 'JJS'})
ADVERBS = frozenset({'RB', 'RBR', 'RBS', 'WRB'})
NOUNS = frozenset({'NN', 'NNS', 'NNP', 'NNPS'})
PRONOUNS = frozenset({'PRP', 'PRP$', 'WP', 'WP$'})
VERBS = frozenset({'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'})
CONJUNCTIONS = frozenset({'CC'})
DETERMINERS = frozenset({'DT', 'PDT', 'WDT'})
PREPOSITIONS = frozenset({'IN'})
PARTICLES = frozenset({'RP'})
INTERJECTIONS = frozenset({'UH'})
NUMBERS = frozenset({'CD'})
FOREIGN_WORDS = frozenset({'FW'})
ADS = ADJECTIVES | ADVERBS
POS_TAGS = (
    ADJECTIVES
    | ADVERBS
    | NOUNS
    | PRONOUNS
    | VERBS
    | CONJUNCTIONS
    | DETERMINERS
    | PREPOSITIONS
    | PARTICLES
    | INTERJECTIONS
    | NUMBERS
    | FOREIGN_WORDS
)


class Analysis(object):
    def __init__(self, submitted: str):
        self.submitted = submitted
        self._tokens = None
        self._tags = None
        self._token_count = None

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
        if self._token_count is None:
            self._token_count = len([tag for tag in self.tags if tag[0] != tag[1]])
        return self._token_count

    @property
    def char_count(self) -> int:
        return len(self.submitted)

    def recombine(self, show_ads: bool = False, show_pos: bool = False) -> str:
        with StringIO() as sfd:
            index = 0
            for tnum, token in enumerate(self.tokens):
                if token in ['``', "''"]:
                    # Refer https://stackoverflow.com/a/32197336.
                    token = '"'
                while True:
                    if index >= self.char_count:
                        # logging.debug('Index: %s, token: "%s"', index, token)
                        logging.error('Something went wrong. Index: %s, char_count: %s.', index, self.char_count)
                        break
                    elif token.startswith(self.submitted[index]):
                        if (show_pos and self.tags[tnum][1] in POS_TAGS) or (show_ads and self.tags[tnum][1] in ADS):
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
