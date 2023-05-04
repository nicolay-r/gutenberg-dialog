import os

current_dir = os.path.dirname(os.path.realpath(__file__))


class Config:
    dialog_gap = 150
    max_length = 100  # max number of words in 1 utterance (100)
    max_books = 100000  # limit size of the dataset
    min_delimiters = 150  # per 10.000 words (150)
    kl_threshold = 2  # (2)
    size_threshold = 20000  # minimum number of words in a book for filtering
    vocab_threshold = 0.2  # (0.2)
    min_double_delim = 40  # for latin languages and hungarian
    clean_dialogs = False  # if True, run preprocessing on dialogs
    languages = ['hu']
    download = False
    pre_filter = False
    extract = False
    post_filter = False
    create_dataset = False
    run_all = False
    directory = os.path.join('data', 'filtered')
    indices_dev = os.path.join(current_dir, 'dev_indices.txt')
    indices_train = os.path.join(current_dir, 'train_indices.txt')
    indices_test = os.path.join(current_dir, 'test_indices.txt')
    metadata = os.path.join(current_dir, 'metadata.txt')
