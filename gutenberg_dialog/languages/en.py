import re
import unicodedata
from gutenberg_dialog.languages.lang import Lang, Dialog


class En(Lang):
    def delimiters(self):
        def d1(delimiter, line):
            return line.count(delimiter)

        def d2(delimiter, line):
            return line.count(delimiter) * 2

        def d3(delimiter, line):
            if line[0] == delimiter:
                return 1
            return 0

        # Dictionary of delimiters and their respective counting functions.
        return {'"': d1, '“': d2, '‘': d2, '_': d3}

    def process_file_(self, paragraph_list):
        # After some amount of characters interpret utterance as new dialog.
        chars_since_dialog = self.cfg.dialog_gap + 1
        for p in paragraph_list:
            # If the paragraph potentially contains dialog.
            if len(p.Text) > 1:
                if '_' == p.Text[0]:
                    # If max chars exceeded start new dialog.
                    if chars_since_dialog > self.cfg.dialog_gap:
                        self.dialogs.append(Dialog(ps=[p]))

                    utt = ''
                    # Augment the segment so the splitting will be correct.
                    segments = ('YXC' + p.Text).split('_')

                    # Join into a single utterance since we are in a paragraph.
                    if len(segments) > 2:
                        utt = ' '.join(segments[2:])
                        self.dialogs[-1].append_utterance(utt=' '.join(utt.split()), p=p)

                    chars_since_dialog = 0
                else:
                    # Add the whole paragraph since there were no dialog.
                    chars_since_dialog += len(p.Text)

    # Extract the dialogs from one file.
    def process_file(self, paragraph_list, delimiter):

        if delimiter == '_':
            self.process_file_(paragraph_list)
            return

        # We have to deal with single quatation marks.
        if delimiter == '‘':
            for p in paragraph_list:
                p.modify_text(lambda t: t.replace('’ ', '‘ '))
        # Unify the later processing.
        if delimiter == '“':
            for p in paragraph_list:
                p.modify_text(lambda t: t.replace('”', '“'))

        # After some amount of characters interpret utterance as new dialog.
        chars_since_dialog = self.cfg.dialog_gap + 1
        for p in paragraph_list:
            # If the paragraph potentially contains dialog.
            if delimiter in p:
                # If max chars exceeded start new dialog.
                if chars_since_dialog > self.cfg.dialog_gap:
                    self.dialogs.append(Dialog(ps=[p]))

                utt_segments = []
                # Augment the segment so the splitting will always be correct.
                segments = ('YXC' + p.Text + 'YXC').split(delimiter)

                good_segment = True
                # Join into a single utterance since we are inside a paragraph.
                if len(segments) > 2 and len(segments) % 2 == 1:
                    for i, segment in enumerate(segments):
                        if i == 1 and len(segment):
                            # 1st utt should be upper-case to avoid artifacts.
                            if segment[0] == segment[0].lower():
                                good_segment = False
                                break
                        if i % 2 == 1:
                            utt_segments.append(segment)

                    utt = ' [USEP] '.join(utt_segments)

                    if good_segment:
                        self.dialogs[-1].append_utterance(utt=' '.join(utt.split()), p=p)

                # Add chars after last comma.
                if good_segment:
                    chars_since_dialog = len(segments[-1]) - 3
                else:
                    chars_since_dialog += len(p.Text)
            else:
                # Otherwise add the whole paragraph since there was no dialog.
                chars_since_dialog += len(p.Text)

    def clean_line(self, line):
        line = re.sub(' \' ', '\'', line)
        line = unicodedata.normalize('NFKD', line)

        # Keep some special tokens.
        line = re.sub('[^a-z .,-:?!"\'0-9]', '', line)
        line = re.sub('[.]', ' . ', line)
        line = re.sub('[?]', ' ? ', line)
        line = re.sub('[!]', ' ! ', line)
        line = re.sub('[-]', ' - ', line)
        line = re.sub('["]', ' " ', line)
        line = re.sub('[:]', ' : ', line)
        line = re.sub('[,]', ' , ', line)
        return line
