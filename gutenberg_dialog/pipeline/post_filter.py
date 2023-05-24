from collections import Counter
import os
import nltk
import importlib

from tqdm import tqdm

from gutenberg_dialog.pipeline.utils import DialogMetaHelper


def clean_dialogs(cfg, directory, lang):
    lang_module = importlib.import_module('gutenberg_dialog.languages.' + lang)
    lang_class = getattr(lang_module, lang.capitalize())(cfg)

    text = []
    path = os.path.join(directory, 'dialogs.txt')
    with open(path, encoding='utf-8') as f:
        for i, line in tqdm(enumerate(f), desc=path):
            if line != cfg.dialog_splitter_line and line != cfg.dialogs_separator:

                utt = DialogMetaHelper.try_parse_utterance(line)
                if utt is None:
                    continue

                line = utt.text.lower()
                line = lang_class.clean_line(line)
                words = nltk.word_tokenize(line)

                line = ' '.join(words)
                if len(words) == 0:
                    # Need this, so there are no empty lines.
                    line = '<PLACEHOLDER>'
                text.append(DialogMetaHelper.serialize_uterance(utt))
            else:
                text.append(line.strip())

    path = os.path.join(directory, 'dialogs_clean.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(text))


# Build vocab based on cleaned dialogs.
def build_vocab_dialogs(cfg, directory):
    vocab = Counter()
    print('Building vocabulary for filtering.')
    path = os.path.join(directory, 'dialogs_clean.txt')
    with open(path, encoding='utf-8') as f:
        for i, line in enumerate(f):
            if line != '\n':
                utt = DialogMetaHelper.try_parse_utterance(line)
                if utt is None:
                    continue
                vocab.update(utt.text.split())

    path = os.path.join(directory, 'dialogs_vocab.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for word, count in vocab.most_common():
            f.write(word + '<SEP>' + str(count) + '\n')

    return vocab


def post_filter(cfg):
    directory = cfg.directory
    for lang in cfg.languages:
        print('Filtering dialogs based on vocab for ' + lang + ' language.')
        path = os.path.join(directory, lang)

        clean_dialogs(cfg, path, lang)
        vocab = build_vocab_dialogs(cfg, path)

        # Fast replacement of OOV words
        swap_vocab = {}
        for i, (word, count) in enumerate(vocab.most_common()):
            swap_vocab[word] = word
            if i >= 100000:
                swap_vocab[word] = '<unk>'

        swap_vocab['<PLACEHOLDER>'] = '<unk>'

        dialogs = [[]]
        dialog_path = os.path.join(path, 'dialogs_clean.txt')
        with open(dialog_path, encoding='utf-8') as f:
            for line in f:
                if line == '\n':
                    dialogs.append([])

                else:
                    utt = DialogMetaHelper.try_parse_utterance(line)
                    if utt is None:
                        continue
                    dialogs[-1].append(utt.text)

        indices = []
        for i, d in enumerate(dialogs):
            text = []
            for u in d:
                text.extend([swap_vocab[word] for word in u.split()])

            # If <unk> percentage is lower than 20% we can keep the dialog.
            if len(text) * cfg.vocab_threshold > text.count('<unk>'):
                indices.append(str(i))

            if i % 100000 == 0:
                print('Filtered ' + str(i) + ' dialogs.')

        indices_path = os.path.join(path, 'indices.txt')
        with open(indices_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(indices))
