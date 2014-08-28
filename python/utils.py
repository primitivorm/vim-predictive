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

import re
import codecs
import locale
import os
import sys
import string
import thirdparty
from collections import Counter
from collections import OrderedDict

def read_file(_path, _encoding):
    #infile = codecs.open(_path, "r", encoding='latin1')
    #lines = [x.encode('latin1').strip().split() for x in infile.readlines()]
    _dict = {}
    lines = []
    if os.path.exists(_path):
        infile = codecs.open(_path, "r", encoding=_encoding)
        lines = [x.encode(_encoding).strip().split() for x in infile.readlines()]
        #infile = open(_path, "r")
        #lines = [x.strip().split() for x in infile.readlines()]
        infile.close()
        _dict = list_to_dict(lines)
    else:
        #open(_path, 'w').close()
        codecs.open(_path, 'w', encoding=_encoding).close()
    return _dict

def write_file(_path, _dict, _encoding):
    outfile = codecs.open(_path, "w", encoding=_encoding)
    outfile.write(str('\n'.join(dict_to_list(_dict)).decode(_encoding)))
    #outfile = open(_path, "w")
    #outfile.write('\n'.join(dict_to_list(_dict)))
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

def is_valid_word(_word, _save_id =0):
    rb = False
    locale.getdefaultlocale()
    try:
        if _save_id:
            #reg_ex = re.compile(r"^[^\d\W]\w*\Z", re.UNICODE)
            reg_ex = re.compile(r"^[^\d\W]\w*\Z")
        else:
            #reg_ex = re.compile(r"^[a-zA-Z]+$", re.UNICODE)
            reg_ex = re.compile(r"^[a-zA-Z]+$")
        rb = re.match(reg_ex,_word)
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
    results=[]
    od = ordered_dict(_dict)
    for k,y in od.iteritems():
        if len(k) >= _len:
            results.append(k)
        if len(results) >= _count:
            break
    return results

def levenshtein(a,b):
    #from http://hetland.org/coding/python/levenshtein.py
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
    return current[n]

def fuzzy_completion(_list, word, MAX_RESULTS=10):
    results=[]
    distances = None
    distances_1 = {}
    distances_2 = {}
    try:
        first_char=word[0].lower()
    except:
        first_char=''
    word_len=len(word)
    word_lower=word.lower()
    endwalk=False
    for w in _list:
        wl=w.lower()
        if wl.startswith(word_lower[0:len(word_lower)]):
            results.append(w)
            if len(results) >= MAX_RESULTS:
                endwalk=True
                break
        else:
            if wl.startswith(first_char):
                distances=distances_1
                distances_2={}
            elif not distances_1:
                distances=distances_2
            if distances!=None:
                w_len=len(w)
                if word_len < w_len:
                    w_len=word_len
                d = levenshtein(w[0:w_len],word)
                try:
                    distancesList=distances[d]
                except:
                    distancesList =[]
                    distances[d]=distancesList
                distancesList.append(w)
            distances=None
        if endwalk:
            break
    if distances_1:
        distances=distances_1
    else:
        distances=distances_2
    results.sort(
        lambda a,b: \
            (0 if len(a)==len(b) else {True:-1,False:1}[len(a) < len(b)]))
    keys=list(distances.keys())
    keys.sort()
    fuzzylen=int(MAX_RESULTS)-len(results)
    if fuzzylen >=0:
        for k in keys:
            distancesList=distances[k]
            results.extend(distancesList)
            del distances[k]
            if len(results) >= MAX_RESULTS:
                results=results[0:MAX_RESULTS]
                break
    return results

def produce_result_value(matches_list, origin_note, want_show_origin):
    """
    Translate the list of matches passed as argument, into a list of
    dictionaries accepted as completion function result.
    For possible entries see the Vim documentation *complete-items*
    """
    result_list = []
    for match in matches_list:
        #new_match_dict = {"word": thirdparty.PythonToVimStr(match)}
        new_match_dict = {"word": match}
        if want_show_origin:
            new_match_dict["menu"] = origin_note
        result_list.append(new_match_dict)
    return result_list
