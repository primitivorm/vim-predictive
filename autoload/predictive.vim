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

let s:plugin_path = escape(expand('<sfile>:p:h'), '\')

function! predictive#enable()
    call predictive#load_dict()
    let g:predictive#disable_plugin=0
    let g:predictive#old_completefunc = &completefunc
    let &completefunc = 'predictive#complete'
    for key in keys(g:predictive#file_types)
        call add(g:predictive#file_types[key], {
            \   'command'      : "\<C-x>\<C-u>",
            \   'completefunc' : 'predictive#complete',
            \   'meets'        : 'predictive#meets_for_predictive',
            \   'repeat'       : '0',
        \})
    endfor
    if !exists("g:acp_behavior")
        let g:acp_behavior = {}
    endif
    call extend(g:acp_behavior, g:predictive#file_types, 'keep')
endfunction

function! predictive#disable()
    if !exists("g:predictive#words")
        let g:predictive#words = {}
    endif
    call predictive#save_dict()
    if &completefunc == 'predictive#complete'
        let &completefunc = g:predictive#old_completefunc
    endif
    let g:predictive#disable_plugin=1
endfunction

function s:getCurrentText()
  return strpart(getline('.'), 0, col('.') - 1)
endfunction

function s:getCurrentWord()
  return matchstr(s:getCurrentText(), '\k*$')
endfunction

function! predictive#complete(findstart, base)
    if a:findstart
        let line = s:getCurrentText()
        let word = s:getCurrentWord()
        let start = stridx(line, word)
        return start
    else
        if a:base!=''
            return predictive#find_word(a:base)
        endif
    endif
endfunction

function! predictive#meets_for_predictive(context)
    if g:predictive#disable_plugin
        return 0
    endif
    if empty(a:context)
        return 0
    endif
    if g:predictive#behaviorLength < 0
        return 0
    endif
    let matches = matchlist(a:context, '\(\k\{' . g:predictive#behaviorLength . ',}\)$')
    if empty(matches)
        return 0
    endif
    return 1
endfunction

function! predictive#load_dict()
    Python import predictive
    Python predictive.load_dict()
endfunction

function! predictive#add_to_dict()
    if g:predictive#add_to_dict_ask
        let response = confirm("Add word to the dictionary?", "&Yes\n&No")
        if response
            Python import predictive
            Python predictive.add_to_dict()
        endif
    else
        Python import predictive
        Python predictive.add_to_dict()
    endif
    return ''
endfunction

function! predictive#remove_from_dict(word)
    Python import predictive
    Python predictive.remove_from_dict()
endfunction

function! predictive#reset_weight(...)
    let s:word = ''
    let s:weight = 0
    if a:0 > 0
        if a:1 != '""' && a:1 != "''"
            let s:word = a:1
        endif
    endif
    if a:0 > 1
        if a:2 > 0
            let s:weight = a:2
        endif
    endif
    Python import predictive
    Python predictive.reset_weight()
endfunction

function! predictive#save_dict()
    Python import predictive
    Python predictive.save_dict()
endfunction

function! predictive#find_word(word)
    "echoerr a:word
    let s:__predictive_complete_lookup_result =[]
    Python import predictive
    Python predictive.find_word()
    return s:__predictive_complete_lookup_result
endfunction

function! predictive#dictree_size()
    echomsg len(g:predictive#words)
endfunction

function! predictive#learn_from_buffer()
    Python import predictive
    Python predictive.learn_from_buffer()
endfunction

" ----------- Python prep
if has('python')
    command! -nargs=1 Python python <args>
elseif has('python3')
    command! -nargs=1 Python python3 <args>
else
    echoerr "No Python support found"
endif

Python << PYTHONEOF
import sys, os, vim
sys.path.insert(0, os.path.join(vim.eval("expand('<sfile>:p:h:h')"), 'python'))
PYTHONEOF
