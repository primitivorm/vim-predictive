" vim-predictive: Given the first few letters of a word, for instance, it's not too difficult to
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

if exists("g:loaded_predictive")
    finish
endif

if exists("g:predictive#disable_plugin") && g:predictive#disable_plugin
    finish
endif

let g:loaded_predictive = 1
if !exists("g:predictive#dict_path")
    let g:predictive#dict_path = expand("<sfile>:p:h:h") . "/dict/en_US.txt"
endif

let g:predictive#dict_words = []

if !exists("g:predictive#disable_keybinding")
    let g:predictive#disable_keybinding=0
endif

if !exists("g:predictive#menu_message")
    let g:predictive#menu_message ="    << predictive"
endif

if !exists("g:predictive#max_suggests")
    let g:predictive#max_suggests=25
endif

if !exists("g:predictive#only_words")
    let g:predictive#only_words=1
endif

"start predictive
let g:predictive#disable_plugin=0
call predictive#enable()
au vimleave * call predictive#disable()
