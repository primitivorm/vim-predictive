" vim-predictive: Given the first few letters of a word, for instance, it's not too difficult to
"                   predict what should come next.
"        Author: Primitivo Roman
"        Email: primitivo.roman.montero@gmail.com
"        Date: 22-10-2014
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

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"basic configuration: add next lines to your .vimrc
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"let g:predictive#dict_path        = expand($HOME . '/quick_references/predictive_dict.txt')
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

if exists("g:loaded_predictive")
    finish
endif

if exists("g:predictive#disable_plugin") && g:predictive#disable_plugin
    finish
endif

if !exists("g:predictive#dict_path")
     echomsg 'you must specify g:predictive#dict_path'
     finish
endif

let s:__predictive_complete_lookup_result=[]

if !exists("g:predictive#OriginNotePredictive")
    let g:predictive#OriginNotePredictive="    << predictive"
endif

if !exists("g:predictive#behaviorLength")
    let g:predictive#behaviorLength=3
endif

if !exists("g:predictive#ShowOriginNote")
    let g:predictive#ShowOriginNote=1
endif

if !exists("g:predictive#max_candidates")
    let g:predictive#max_candidates=25
endif

if !exists("g:predictive#prefer_python3")
    let g:predictive#prefer_python3=0
endif

if !exists("g:predictive#fuzzy_completion_enable")
    let g:predictive#fuzzy_completion_enable=1
endif

if !exists("g:predictive#fuzzy_completion_min_chars")
    let g:predictive#fuzzy_completion_min_chars=5
endif

if !exists("g:predictive#fuzzy_completion_min_distance")
    let g:predictive#fuzzy_completion_min_distance=4
endif

if !exists("g:predictive#auto_save_dict")
    let g:predictive#auto_save_dict=1
endif

if !exists("g:predictive#min_chars_suggestion")
    let g:predictive#min_chars_suggestion=3
endif

if !exists("g:predictive#auto_load")
    let g:predictive#auto_load=1
endif

if !exists("g:predictive#keyword_patterns")
    let g:predictive#keyword_patterns = '^[a-zA-Z]+$'
endif

"Controls automatic word frequency learning. When non-nil (the default), the
"weight for a word in is incremented each time it is accepted as a completion,
"making the word more likely to be offered higher up the list of completions in
"the future. Words that are not already in the dictionary are ignored unless
"predictive#auto_add_to_dict is set.
if !exists("g:predictive#auto_learn")
    let g:predictive#auto_learn=1
endif

"Controls automatic adding of new words to dictionaries. If nil (the default),
"new words are never automatically added to a dictionary. If t, new words are
"automatically added to the active dictionary. If set to a dictionary name, new
"words are automatically added to that dictionary instead of the active one.
if !exists("g:predictive#auto_add_to_dict")
    let g:predictive#auto_add_to_dict=1
endif

"If non-nil (the default), auto-learnt and auto-added words are cached, and only
"actually added to the dictionary when Vim has been idle for predictiveflush-
"auto-learn-delay seconds or the buffer is killed (it has no effect unless
"at least one of predictive-auto-learn or predictive-auto-add-to-dict is
"also set). This avoids small but sometimes noticeable delays when typing. New
"words or word weights will not be taken into account until the cache is fully
"flushed.
if !exists("g:predictive#use_auto_learn_cache")
    let g:predictive#use_auto_learn_cache=1
endif

"Minimum length of words auto-added to the dictionary. When enabled, words
"shorter than this will be ignored when auto-add is used.
if !exists("g:predictive#auto_add_min_chars")
    let g:predictive#auto_add_min_chars=3
endif

"If non-nil, predictive mode will ask for confirmation before automatically adding
"any word to a dictionary. Enabled by default. This has no effect unless
"predictive-auto-add-to-dict is also set.
if !exists("g:predictive#add_to_dict_ask")
    let g:predictive#add_to_dict_ask=0
endif

"Whether to ignore initial capital letters when completing
"words. If non-nil, completions for the uncapitalized string are
"also found.
"Note that only the *first* capital letter of a string is
"ignored. Thus typing \"A\" would find \"and\", \"Alaska\" and
"\"ANSI\", but typing \"AN\" would only find \"ANSI\", whilst
"typing \"a\" would only find \"and\"."
if !exists("predictive#ignore_initial_caps")
    let g:predictive#ignore_initial_caps=1
endif

"start predictive
let g:predictive#disable_plugin=0

func! s:init_config()
    if has('python')
        " Define the default options.
        if g:predictive#auto_save_dict
            autocmd bufwrite * call predictive#save_dict()
        endif
        if g:predictive#auto_load
            autocmd bufread * call predictive#enable()
        endif
        "default key bindings
        inoremap <expr><cr> predictive#add_to_dict() . "\<cr>"
        inoremap <expr><space> predictive#add_to_dict() . "\<space>"
        inoremap <expr><esc> predictive#add_to_dict() . "\<esc>"
    endif
endfunc

func! s:init_commands()
    if has('python')
        " Add in the Ex commands.
        command! -nargs=0 PredictiveEnable call predictive#enable()
        command! -nargs=0 PredictiveDisable call predictive#disable()
        command! -nargs=0 PredictiveDictreeSize call predictive#dictree_size()
        command! -nargs=1 PredictiveRemoveFromDict call predictive#remove_from_dict(<f-args>)
        command! -nargs=* PredictiveResetWeight call predictive#reset_weight(<f-args>)
        "Learn word weights from BUFFER (defaults to the current buffer).
        "The word weight of each word in dictionary DICT is incremented by
        "the number of occurences of that word in the buffer.
        command! -nargs=0 PredictiveLearnFromBuffer call predictive#learn_from_buffer()
    endif
endfunc

if !exists("g:loaded_predictive")
  call s:init_commands()
  call s:init_config()
  let g:loaded_predictive=1
endif
