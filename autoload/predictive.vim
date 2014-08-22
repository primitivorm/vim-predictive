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
endfunction

function! predictive#disable()
    call predictive#save_dict()
    if &completefunc == 'predictive#complete'
        let &completefunc=''
    endif
    let g:predictive#disable_plugin=1
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
        if a:base!=''
            return predictive#find_word(a:base)
        else
            return predictive#add_to_dict(a:base)
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
    return 1
endfunction

function! predictive#load_dict()
    Python import predictive
    Python predictive.load_dict()
endfunction

function! predictive#add_to_dict(word)
    Python import predictive
    Python predictive.add_to_dict()
    return s:__predictive_complete_lookup_result
endfunction

function! predictive#save_dict()
    Python import predictive
    Python predictive.save_dict()
endfunction

function! predictive#find_word(word)
    Python import predictive
    Python predictive.find_word()
    return s:__predictive_complete_lookup_result
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
