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
else
    let g:predictive#disable_plugin=0
    au vimenter * call predictive#init()
    au vimleave * call predictive#write_dict_new()
    "for completefunc
    set completefunc=predictive#complete
    "for acp integration
    let g:acp_behaviorUserDefinedFunction = 'predictive#complete'
    let g:acp_behaviorUserDefinedMeets = 'predictive#meets_for_predictive'

"let jsbehavs = { 'javascript': [] }
    "call add(jsbehavs.javascript, {
        "\   'command'      : "\<C-x>\<C-u>",
        "\   'completefunc' : 'acp#completeSnipmate',
        "\   'meets'        : 'acp#meetsForSnipmate',
        "\   'onPopupClose' : 'acp#onPopupCloseSnipmate',
        "\   'repeat'       : 0,
    "\})
    "call add(jsbehavs.javascript, {
        "\   'command' : g:acp_behaviorKeywordCommand,
        "\   'meets'   : 'acp#meetsForKeyword',
        "\   'repeat'  : 0,
        "\ })
    "call add(jsbehavs.javascript, {
        "\    'command'  : "\<C-x>\<C-o>",
        "\    'meets'   : 'acp#meetsForKeyword',
        "\    'repeat'   : 0,
    "\})
"let g:acp_behavior = {}
"call extend(g:acp_behavior, jsbehavs, 'keep')
endif

let g:loaded_predictive = 1
let g:predictive#dict_path = expand("<sfile>:p:h:h") . "/dict/dict.predictive.txt"
let g:predictive#dict_words = []

if !exists("g:predictive#disable_keybinding")
    let g:predictive#disable_keybinding=0
endif

if !exists("g:predictive#menu_message")
    let g:predictive#menu_message ="    << predictive"
endif

if !exists("g:predictive#max_suggests")
    let g:predictive#max_suggests=10
endif

if !exists("g:predictive#only_words")
    let g:predictive#only_words=1
endif
