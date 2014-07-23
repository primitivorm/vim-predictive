" vim-predictive: Given the first few letters of a word, for instance, it's not too difficult to
"         predict what should come next.
"      Author: Primitivo Roman
"      Email: primitivo.roman.montero@gmail.com
"      Date: 21-07-2014
"      Version: 1.0
" vim-predictive is free software: you can redistribute it and/or modify
" it under the terms of the GNU General Public License as published by
" the Free Software Foundation, either version 2 of the License, or
" (at your option) any later version.
"
" vim-predictive is distributed in the hope that it will be useful,
" but WITHOUT ANY WARRANTY; without even the implied warranty of
" MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
" GNU General Public License for more details.

function! predictive#suggest(base)
    let l:matches = []
    if a:base!=''
        "find fuzzy completion word
        let l:matches = predictive#find_word(a:base)
    else
        :call predictive#new_word()
        let l:matches = g:predictive#dict_new_words[0:g:predictive#max_suggests]
    endif
    let l:matches_return = []
    for m in l:matches
        let pdict={"word": split(m, ",")[0]}
        if exists("g:predictive#menu_message")
            let pdict.menu = g:predictive#menu_message
        else
            let pdict.menu = ""
        endif
        :call add(l:matches_return, pdict)
    endfor
    "return l:matches_return[0:g:predictive#max_suggests - 1]
    return l:matches_return
endfunction

function! predictive#new_word()
    "add previous word to predictive file
    let l:word=''
    let l:words = split(getline('.'))
    if len(l:words) > 0
        let l:word = l:words[-1]
        if predictive#is_valid_word(l:word)
            if predictive#exists_word(l:word)
                let s:tmp_words = []
                for w in g:predictive#dict_new_words
                if match(split(w, ',')[0], l:word) != '-1'
                    :call add(s:tmp_words, l:word . ',' . (split(w, ',')[1] + 1))
                else
                    :call add(s:tmp_words, w)
                endif
                endfor
                let g:predictive#dict_new_words = s:tmp_words
                if filewritable(g:predictive#file_dict_new)
                    let g:predictive#dict_new_words = sort(g:predictive#dict_new_words, "predictive#compare")
                    :call writefile(g:predictive#dict_new_words, g:predictive#file_dict_new)
                else
                    echoerr "can not write to the file:" . g:predictive#file_dict_new
                endif
            else
                :call add(g:predictive#dict_new_words, l:word . ',1')
                if filewritable(g:predictive#file_dict_new)
                    let g:predictive#dict_new_words = sort(g:predictive#dict_new_words, "predictive#compare")
                    :call writefile(g:predictive#dict_new_words, g:predictive#file_dict_new)
                else
                    echoerr "can not write to the file:" . g:predictive#file_dict_new
                endif
            endif
        endif
    endif
endfunction

function! predictive#find_word(word)
    let l:matches = []
    let l:count = 0
    "find in dict.new.txt
    for n in g:predictive#dict_new_words
        if match(n, '^' . a:word) != '-1'
            :call add(l:matches, split(n, ',')[0])
            let l:count = l:count + 1
        endif
        if l:count > g:predictive#max_suggests
            return l:matches
        endif
    endfor
    find in dict.txt
    for d in g:predictive#dict_words
        if match(d, '^' . a:word) != '-1'
            :call add(l:matches, d)
            let l:count = l:count + 1
        endif
        if l:count > g:predictive#max_suggests
            return l:matches
        endif
    endfor
    return l:matches
endfunction

function! predictive#exists_word(word)
    for w in g:predictive#dict_new_words
        if match(split(w, ',')[0], '^' . a:word . '$' ) != '-1'
            return 1
        endif
    endfor
    return 0
endfunction

function! predictive#compare(i1, i2)
    "order by number descending
    return split(a:i2, ',')[1] - split(a:i1, ',')[1]
endfunc

function! predictive#is_valid_word(word)
  if a:word == '' || a:word =~ '^\d\+$' || a:word =~ '\W'
    return 0
  endif
  return 1
endfunction
