# -*- coding: utf-8 -*-
#!/usr/bin/python

# vim-predictive: Given the first few letters of a word, for instance,
#                   it's not too difficult to
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

import re
import codecs
import locale
import os
from collections import OrderedDict
import numpy as np

def read_file(_path, _encoding):
    _dict = {}
    lines = []
    if os.path.exists(_path):
        infile = open(_path, "r")
        lines = [x.strip().split() for x in infile.readlines()]
        infile.close()
        _dict = list_to_dict(lines)
    else:
        codecs.open(_path, 'w', encoding=_encoding).close()
    return _dict

def write_file(_path, _dict, _encoding):
    outfile = open(_path, "w")
    outfile.write('\n'.join(dict_to_list(_dict)))
    outfile.close()

def list_to_dict(_list):
    d = {}
    for key, value in _list:
        d.setdefault(key, int(value))
    return d

def ordered_dict(_dict):
    #order by weight descending
    od = OrderedDict(sorted(_dict.items(), key=lambda t: t[1]))
    items = od.items()
    items.reverse()
    return OrderedDict(items)

def dict_to_list(_dict):
    list_return = []
    for key, value in _dict.iteritems():
        list_return.append(key + ' ' + str(value))
    return list_return

def is_valid_word(_word, _regex):
    rb = False
    locale.getdefaultlocale()
    try:
        try:
            reg_ex = re.compile(_regex)
        except:
            reg_ex = re.compile('^[a-zA-Z]+$')
        rb = re.match(reg_ex, _word)
    except:
        pass
    return rb

def dict_reset_all_values(_dict, _val=0):
    return dict.fromkeys(_dict.iterkeys(), _val)

def dict_reset_value(_dict, _key, _val=0):
    if _key in _dict:
        _dict[_key] = _val
    return _dict

def most_common(_dict, _len, _count):
    results = []
    od = ordered_dict(_dict)
    for k, y in od.iteritems():
        if len(k) >= _len:
            results.append(k)
        if len(results) >= _count:
            break
    return results

def levenshtein(source, target):
    """
    Calculates the Levenshtein distance between a and b."
    http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    """
    if len(source) < len(target):
        return levenshtein(target, source)

    # So now we have len(source) >= len(target).
    if len(target) == 0:
        return len(source)

    # We call tuple() to force strings to be used as sequences
    # ('c', 'a', 't', 's') - numpy uses them as values by default.
    source = np.array(tuple(source))
    target = np.array(tuple(target))

    # We use a dynamic programming algorithm, but with the
    # added optimization that we only need the last two rows
    # of the matrix.
    previous_row = np.arange(target.size + 1)
    for s in source:
        # Insertion (target grows longer than source):
        current_row = previous_row + 1

        # Substitution or matching:
        # Target and source items are aligned, and either
        # are different (cost of 1), or are the same (cost of 0).
        current_row[1:] = np.minimum(
            current_row[1:],
            np.add(previous_row[:-1], target != s))

        # Deletion (target grows shorter than source):
        current_row[1:] = np.minimum(
                current_row[1:],
                current_row[0:-1] + 1)

        previous_row = current_row

    return previous_row[-1]

def fuzzy_completion(_dict, word, MIN_DISTANCE=3, MAX_RESULTS=10):
    _list = list(_dict)
    results = []
    try:
        first_char = word[0]
    except:
        first_char = ''
    word_len = len(word)
    endwalk = False
    #create a generator
    new_list = (wr for wr in _list if len(wr) >= word_len)
    for w in new_list:
        wl = w.lower()
        if wl.startswith(word[0:len(word)]):
            results.append(w)
            if len(results) >= MAX_RESULTS:
                break
        else:
            d = levenshtein(word, w[0:len(w)])
            if d <= MIN_DISTANCE:
                results.append(w)
            if len(results) >= MAX_RESULTS:
                break
    return results

def produce_result_value(matches_list, origin_note, want_show_origin):
    """
    Translate the list of matches passed as argument, into a list of
    dictionaries accepted as completion function result.
    For possible entries see the Vim documentation *complete-items*
    """
    s = ''
    s = '['
    if want_show_origin:
        for match in matches_list:
            s += '{"word": "' + match + '", "menu":"' + origin_note +'"},'
    else:
        for match in matches_list:
            s += '{"word": "' + match + '"},'
    s += ']'
    s = s.replace('},]', '}]')
    return s

def python_dict_to_vim_str(_dict):
    s = '{'
    for key in _dict:
        s += '"' + key + '":' + str(_dict[key]) + ','
    s += '}'
    s = s.replace(',}', '}')
    return s
