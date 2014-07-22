" vim-predictive: Given the first few letters of a word, for instance, it’s not too difficult to
"                   predict what should come next.
"        Author: Primitivo Roman
"        Email: primitivo.roman.montero@gmail.com
"        Date: 17-07-2014
"        Version: 1.0
" vim-predictive is free software: you can redistribute it and/or modify
" it under the terms of the GNU General Public License as published by
" the Free Software Foundation, either version 2 of the License, or
" (at your option) any later version.
"
" vim-predictive is distributed in the hope that it will be useful,
" but WITHOUT ANY WARRANTY; without even the implied warranty of
" MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
" GNU General Public License for more details.

if exists("g:predictive#load")
    finish
endif
""save cpo options
"let s:keepcpo = &cpo
"set cpo&vim

let g:predictive#load = 1
"TODO: remove this var
let g:predictive#plugin_path = expand("<sfile>:p:h:h")
let g:predictive#dictionary = g:predictive#plugin_path . "/dict/dict.txt"
let g:predictive#file_dict_new = g:predictive#plugin_path . "/dict/dict.new.txt"

if !exists("g:predictive#max_suggests")
    let g:predictive#max_suggests=3
endif

let g:predictive#dict_words = []
let g:predictive#dict_new_words = []

function! predictive#init()
    "get words from dict
    if filereadable(g:predictive#dictionary)
        let g:predictive#dict_words = readfile(g:predictive#dictionary)
    endif
    "get words from dict.new
    if filereadable(g:predictive#file_dict_new)
        let g:predictive#dict_new_words = readfile(g:predictive#file_dict_new)
    endif
endfunction

function! predictive#complete(findstart, base)
    if a:findstart
        let line = getline(".")
        let start = col(".") - 1
        while start > 0 && line[start - 1] =~ '\a\|_'
            let start -= 1
        endwhile
        return start
    else
        return predictive#suggest(a:base)
    endif
endfunction

set completefunc=predictive#complete

if !exists("g:predictive#disable_keybinding")
    let g:predictive#disable_keybinding=0
endif

if !exists("g:predictive#menu_message")
    let g:predictive#menu_message ="    << predictive"
endif

if !g:predictive#disable_keybinding
    "imap <space> <space><C-x><C-u>
endif

call predictive#init()

""restore cpo options
"let &cpo= s:keepcpo
"unlet s:keepcpo