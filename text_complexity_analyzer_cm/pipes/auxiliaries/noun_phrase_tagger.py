from spacy.language import Language
from spacy.tokens import Doc
from spacy.tokens import Span
from spacy.util import filter_spans

from text_complexity_analyzer_cm.constants import ACCEPTED_LANGUAGES
from typing import List


class NounPhraseTagger:
    '''
    This tagger has the task to find all noun phrases in a document. It needs to go after the 'Parser' pipeline component.
    '''
    name = 'noun_phrase_tagger'

    def __init__(self, nlp: Language) -> None:
        '''
        This constructor will initialize the object that tags noun phrases.

        Parameters:
        language: The language that this pipeline will be used in.

        Returns:
        None.
        '''
        self._nlp = nlp

        Doc.set_extension('noun_phrases', force=True, default=[])
        Span.set_extension('noun_phrase_modifiers_count', default=0) # Count of adjectives in a noun phrase

    def __call__(self, doc: Doc) -> Doc:
        '''
        This method will find all noun phrases and store them in an iterable.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The spacy document analyzed.
        '''
        noun_phrases = set(
            np
            for nc in doc.noun_chunks
            for np in [nc, doc[nc.root.left_edge.i:nc.root.right_edge.i+1]]
        )
        # Find the amount of modifiers for each noun phrase
        for np in noun_phrases:
            np._.noun_phrase_modifiers_count = sum(1 for token in np if token.pos_ == 'ADJ')

        doc._.noun_phrases = [span for span in filter_spans(noun_phrases)] # Save the noun phrases found
        
        return doc