class Utterance:
    """ Parsed Utterance with metainformation
    """

    def __init__(self, book, location, text):
        assert(isinstance(book, int))
        assert(isinstance(location, str))
        assert(isinstance(text, str))
        self.book = book
        self.location = location
        self.text = text

class DialogMetaHelper:

    # Substring that separates the metainformation for the line
    # related to each utterance of the dialog and the actual contents
    # of the line.
    _sep = '[METASEP] '

    @staticmethod
    def try_parse_utterance(line):
        """ Parsing meta-information from utterance.
        """
        args = line.split(DialogMetaHelper._sep)
        if len(args) != 2:
            return None
        [book_meta, text] = args
        book, dialog_location = book_meta.split('.txt')
        return Utterance(book=int(book), location=dialog_location, text=text.strip('\n'))

    @staticmethod
    def serialize_uterance(utt):
        """ combine utterance with meta-information
        """
        assert(isinstance(utt, Utterance))
        return str(utt.book) + '.txt' + utt.location + DialogMetaHelper._sep + utt.text
