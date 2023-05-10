class Lang:
    def __init__(self, cfg):
        self.cfg = cfg
        self.dialogs = []

    def delimiters():
        raise NotImplementedError

    def process_line(self, paragraph_list, delimiter):
        raise NotImplementedError

    def clean_line(self, line):
        raise NotImplementedError


class Dialog:
    """ Description of the dialog.
    """

    # Substring that separates the metainformation for the line
    # related to each utterance of the dialog and the actual contents
    # of the line.
    META_SEPARATOR = 'line: '

    def __init__(self, ps, utts=None):
        """ Note: additionally establish connection with the paragraph.
        """
        assert(isinstance(ps, list))
        self.__paragraphs = ps
        self.__utterances = [] if utts == None else utts

    @classmethod
    def from_existed(cls, d, ind_from, ind_to):
        assert(isinstance(d, Dialog))
        instance = cls(d.__paragraphs)
        instance.__utterances = d.__utterances[ind_from:ind_to]
        return instance

    @property
    def Paragraphs(self):
        return self.__paragraphs

    @property
    def Bounds(self):
        mn = min([p.LineFrom for p in self.__paragraphs])
        mx = max([p.LineTo for p in self.__paragraphs])
        return (mn, mx)

    def iter_utterances(self):
        return iter(self.__utterances)

    def append_utterance(self, utt, p):
        self.__utterances.append(utt)
        self.__paragraphs.append(p)

    def __len__(self):
        return len(self.__utterances)

    def __iter__(self):
        return iter(self.__utterances)


class Paragraph:
    """ Description of the paragraph.
    """

    def __init__(self, file_name, line_ind):
        """ Create emtpy paragraph.
        """
        self.__file_name = file_name
        self.__line_from = line_ind
        self.__line_to = line_ind
        self.__text = ""

    @property
    def FileName(self):
        return self.__file_name

    @property
    def DisplayBounds(self):
        return "[{}-{}]".format(self.__line_from, self.__line_to)

    @property
    def Text(self):
        return self.__text

    @property
    def LineFrom(self):
        return self.__line_from

    @property
    def LineTo(self):
        return self.__line_to

    def extend(self, line, line_ind):
        assert(line_ind >= self.__line_from)
        self.__text += line
        self.__line_to = line_ind

    def num_words(self):
        return len(self.__text.split())

    def modify_text(self, f):
        assert(callable(f))
        self.__text = f(self.__text)

    def __contains__(self, item):
        return item in self.__text
