# -*- coding: utf-8 -*-
#!/usr/bin/python

# vim-predictive: Given the first few letters of a word, for instance, it's not too difficult to
#         predict what should come next.
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

import codecs
import itertools
import os
import re
import string
import utils
import vim
from collections import Counter

DICT_PATH=vim.eval('g:predictive#dict_path')
MAX_CANDIDATES=int(vim.eval('g:predictive#max_candidates'))
AUTO_LEARN=vim.eval('g:predictive#auto_learn')
AUTO_ADD_TO_DICT=vim.eval('g:predictive#auto_add_to_dict')
SAVE_IDENTIFIERS=vim.eval('g:predictive#save_identifiers')
FUZZY_COMPLETION_ENABLE=vim.eval('g:predictive#fuzzy_completion_enable')
FUZZY_COMPLETION_MIN_CHARS=int(vim.eval('g:predictive#fuzzy_completion_min_chars'))
ORIGIN_NOTE = vim.eval("g:predictive#OriginNotePredictive")
AUTO_ADD_MIN_CHARS=int(vim.eval('g:predictive#auto_add_min_chars'))
MIN_CHARS_SUGGESTION=int(vim.eval('g:predictive#min_chars_suggestion'))
WANT_SHOW_ORIGIN = int(vim.eval("g:predictive#ShowOriginNote"))
VIM_COMMAND_PREDICTIVE_COMPLETE = 'silent let s:__predictive_complete_lookup_result = %s'

def load_dict():
    words = utils.read_file(DICT_PATH)
    vim.command('let g:predictive#words = %s' % words)

def save_dict():
    """
    Save dictionary DICT to its associated file.
    Use `predictive-write-dict' to save to a different file.
    See also `predictive-dict-compilation'.
    """
    words = vim.eval('g:predictive#words')
    utils.write_file(DICT_PATH, words)

def find_word():
    words = vim.eval('g:predictive#words')
    encoding = vim.eval("&encoding")
    word = vim.eval("a:word").decode(encoding)
    found_matches=[]
    #predictive search
    od = utils.ordered_dict(words)
    for k,y in od.iteritems():
        if k.startswith(word):
            found_matches.append(k)
        if len(found_matches) >= MAX_CANDIDATES:
            break
    #fuzzy search
    if FUZZY_COMPLETION_ENABLE:
        if len(word) >= FUZZY_COMPLETION_MIN_CHARS:
            found_matches.extend(utils.fuzzy_completion(list(words), word, MAX_CANDIDATES))
    vim.command(VIM_COMMAND_PREDICTIVE_COMPLETE
                % repr(utils.produce_result_value(
                found_matches,
                ORIGIN_NOTE,
                WANT_SHOW_ORIGIN)))

def add_to_dict():
    """
    Insert a word into a dictionary. The dictionary name and word are read from
    the mini-buffer (defaults to the word at the point). An optional prefix argument
    specifies the weight. If the word is not already in the dictionary, it will be added
    to it with that initial weight (or 0 if none is supplied). If the word is already
    in the dictionary, its weight will be incremented by the weight value (or by 1 if
    none is supplied).
    """
    words = vim.eval('g:predictive#words')
    (r, c) = vim.current.window.cursor
    ws = vim.current.line[:c]
    l = ws.split()
    if len(l) > 1:
        w = ws.split()[-2]
        if w in words:
            if AUTO_LEARN:
                words[w] = int(words[w]) + 1
        else:
            if AUTO_ADD_TO_DICT:
                if utils.is_valid_word(w, SAVE_IDENTIFIERS):
                    if len(w) >= AUTO_ADD_MIN_CHARS:
                        words.setdefault(w, 0)
        vim.command('let g:predictive#words = %s' % words)
    found_matches=[]
    found_matches = utils.most_common(words, MIN_CHARS_SUGGESTION, MAX_CANDIDATES)
    vim.command(VIM_COMMAND_PREDICTIVE_COMPLETE
                % repr(utils.produce_result_value(
                found_matches,
                ORIGIN_NOTE,
                WANT_SHOW_ORIGIN)))

def reset_weight(_dict, word='', weight=0):
    """
    Reset the weight of a word in a dictionary to 0. The dictionary name and word
    are read from the mini-buffer. If no word is supplied, reset the weights of all
    words in the dictionary. If a prefix argument is supplied, reset weight(s) to that
    value, rather than 0.
    """
    if word=='':
        utils.dict_reset_all_values(_dict, weight)
    else:
        utils.dict_reset_value(_dict, word, weight)
    return _dict
