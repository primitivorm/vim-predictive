# -*- coding: utf-8 -*-
#!/usr/bin/python

# vim-predictive: Given the first few letters of a word, for instance,
#                   it's not too difficult to predict what should come next.
#      Author: Primitivo Roman
#      Email: primitivo.roman.montero@gmail.com
#      Date: 20-08-2014
#      Version: 1.0
# vim-predictive is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# vim-predictive is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import utils
import vim
import logging

DICT_PATH = vim.eval('g:predictive#dict_path')
MAX_CANDIDATES = int(vim.eval('g:predictive#max_candidates'))
AUTO_LEARN = vim.eval('g:predictive#auto_learn')
AUTO_ADD_TO_DICT = vim.eval('g:predictive#auto_add_to_dict')
IGNORE_INITIAL_CAPS = vim.eval('g:predictive#ignore_initial_caps')
FUZZY_COMPLETION_ENABLE = vim.eval('g:predictive#fuzzy_completion_enable')
FUZZY_COMPLETION_MIN_CHARS = int(vim.eval(
    'g:predictive#fuzzy_completion_min_chars'))
FUZZY_COMPLETION_MIN_DISTANCE = int(vim.eval(
    'g:predictive#fuzzy_completion_min_distance'))
ORIGIN_NOTE = vim.eval("g:predictive#OriginNotePredictive")
AUTO_ADD_MIN_CHARS = int(vim.eval('g:predictive#auto_add_min_chars'))
MIN_CHARS_SUGGESTION = int(vim.eval('g:predictive#min_chars_suggestion'))
WANT_SHOW_ORIGIN = int(vim.eval("g:predictive#ShowOriginNote"))
VIM_COMMAND_PREDICTIVE_COMPLETE = "silent let s:__predictive_complete_lookup_result = "
KEYWORD_PATTERNS = vim.eval("g:predictive#keyword_patterns")
DEBUG = vim.eval("g:predictive#debug")

ENCODING = vim.eval("&encoding")

def load_dict():
    """
    Load a dictionary by name, and add it to the list of dictionaries used by
    the current buffer. The dictionary will be included when learning from the
    buffer, and if its autosave flag is set, it will automatically be saved
    when the buffer is killed. The dictionary file must be in your loadpath.
    You should never normally need to use this command interactively, since
    predictive mode loads and unloads dictionaries automatically, as needed.
    """
    log("inicia load_dict")
    words = utils.read_file(DICT_PATH, ENCODING)
    vim.command('let g:predictive#words = ' + utils.python_dict_to_vim_str(words))
    log("finaliza load_dict")

def save_dict():
    """
    Save dictionary DICT to its associated file.
    Use `predictive-write-dict' to save to a different file.
    """
    log("inicia save_dict")
    words = vim.eval('g:predictive#words')
    utils.write_file(DICT_PATH, words, ENCODING)
    log("finaliza save_dict")

def find_word():
    log("inicia find_word")
    words = vim.eval('g:predictive#words')
    word = vim.eval("a:word")
    if len(word) > 0 and IGNORE_INITIAL_CAPS:
        word = word[0].lower() + word[1:]
    found_matches = []
    #predictive search
    ord = utils.ordered_dict(words)
    for k, y in ord.iteritems():
        if k.startswith(word):
            found_matches.append(k)
        if len(found_matches) >= MAX_CANDIDATES:
            break
    #fuzzy search
    if FUZZY_COMPLETION_ENABLE:
        if len(word) >= FUZZY_COMPLETION_MIN_CHARS:
            found_matches.extend(
                utils.fuzzy_completion(
                    list(words),
                    word,
                    FUZZY_COMPLETION_MIN_DISTANCE,
                    MAX_CANDIDATES))
    result = utils.produce_result_value(
        found_matches,
        ORIGIN_NOTE,
        WANT_SHOW_ORIGIN)
    vim.command(VIM_COMMAND_PREDICTIVE_COMPLETE + result)
    log("finaliza find_word")

def add_to_dict():
    """
    Insert a word into a dictionary. The dictionary name and word are read from
    the mini-buffer (defaults to the word at the point). An optional prefix
    argument specifies the weight. If the word is not already in the dictionary,
    it will be added to it with that initial weight
    (or 0 if none is supplied). If the word is already in the dictionary,
    its weight will be incremented by the weight value (or by 1 if none is supplied).
    """
    log("inicia add_to_dict")
    words = vim.eval('g:predictive#words')
    (r, c) = vim.current.window.cursor
    ws = vim.current.line[:c]
    l = ws.split()
    w = ''
    if len(l) > 1:
        w = l[-1]
    elif len (l) == 1:
        w = l[0]
    if w!='':
        if w in words:
            if AUTO_LEARN:
                words[w] = int(words[w]) + 1
        else:
            if AUTO_ADD_TO_DICT:
                if utils.is_valid_word(w, KEYWORD_PATTERNS):
                    if len(w) >= AUTO_ADD_MIN_CHARS:
                        words.setdefault(w, 0)
        vim.command('let g:predictive#words = ' + utils.python_dict_to_vim_str(words))
    log("finaliza add_to_dict")
    return ''

def remove_from_dict():
    """
    Completely remove a word from a dictionary. The dictionary name and word
    are read from the mini-buffer (defaults to the word at the point).
    """
    log("inicia remove_from_dict")
    words = vim.eval('g:predictive#words')
    word = vim.eval("a:word")
    if word in words:
        del words[word]
        msg = 'predictive: the word (' + word + ') has been deleted'
        vim.command('echohl ErrorMsg | echomsg "%s" | echohl None' % msg)
        vim.command('let g:predictive#words = ' + utils.python_dict_to_vim_str(words))
    log("finaliza remove_from_dict")

def reset_weight():
    """
    Reset the weight of a word in a dictionary to 0. The dictionary name and
    word are read from the mini-buffer. If no word is supplied, reset the
    weights of all words in the dictionary. If a prefix argument is supplied,
    reset weight(s) to that value, rather than 0.
    """
    log("inicia reset_weight")
    word=vim.eval("s:word")
    weight = vim.eval("s:weight")
    words = vim.eval('g:predictive#words')
    if word == '':
        words = utils.dict_reset_all_values(words, weight)
    else:
        words = utils.dict_reset_value(words, word, weight)
    vim.command('let g:predictive#words = ' + utils.python_dict_to_vim_str(words))
    log("finaliza reset_weight")

def learn_from_buffer():
    """
    Learns weights for words in a dictionary from text in a buffer. If no explicit
    dictionary is specified, this learns word weights for all dictionaries used by the
    current buffer.
    Each occurrence of a word increments its weight in the dictionary. By default,
    only occurrences that occur in a region where the dictionary is active are
    counted. If an explicit
    dictionary is specified, this can be overridden by supplying a prefix argument,
    in which case all occurrences are counted, irrespective of whether the dictionary
    is active at the word occurrence. Note that you cannot use this command
    to add words to a dictionary, only to train the weights of words already in a
    dictionary.
    """
    log("inicia learn_from_buffer")
    words = vim.eval('g:predictive#words')
    for line in vim.current.buffer:
        for w in line.split():
            if w in words:
                if AUTO_LEARN:
                    words[w] = int(words[w]) + 1
            else:
                if AUTO_ADD_TO_DICT:
                    if utils.is_valid_word(w, KEYWORD_PATTERNS):
                        if len(w) >= AUTO_ADD_MIN_CHARS:
                            words.setdefault(w, 0)
    vim.command('let g:predictive#words = ' + utils.python_dict_to_vim_str(words))
    log("finaliza learn_from_buffer")

def log(msg):
    if DEBUG:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt=None, #'%m-%d %H:%M',
            filename=DICT_PATH + '.log',
            filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        logging.debug(msg)
