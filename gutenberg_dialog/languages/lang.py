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

    def __init__(self, p):
        """ Note: additionally establish connection with the paragraph.
        """
        assert(isinstance(p, Paragraph))
        self.__paragraph = p
        self.__utterances = []

    @classmethod
    def from_existed(cls, d, ind_from, ind_to):
        instance = cls(d.Paragraph)
        instance.__utterances = d[ind_from:ind_to]

    @property
    def Paragraph(self):
        return self.__paragraph

    @property
    def ParagraphBounds(self):
        return (self.__paragraph.LineFrom, self.__paragraph.LineTo)

    def iter_utterances(self):
        return iter(self.__utterances)

    def append_utterance(self, utt):
        self.__utterances.append(utt)

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
    def Bounds(self):
        return (self.__line_from, self.__line_to)

    @property
    def Text(self):
        return self.__text

    @property
    def LineFrom(self):
        return self.__line_from

    @property
    def LineTo(self):
        return self.__line_to

    def extend(self, line):
        self.__text += line
        self.__line_to += 1

    def num_words(self):
        return len(self.__text.split())

    def modify_text(self, f):
        assert(callable(f))
        self.__text = f(self.__text)

    def __contains__(self, item):
        return item in self.__text
