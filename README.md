vim-predictive
--------------
Given the first few letters of a word, for instance, it’s not too difficult to predict what should come next.

install
--------------
you only need add to Bundle list or install with pathogen

Bundle 'primitivorm/vim-predictive'

options
--------------

All options have reasonable defaults so if the plug-in works after installation
you don't need to change any options. These options can be configured in your
[vimrc script][vimrc] by including a line like this:

    let g:predictive#disable_plugin

Note that after changing an option in your [vimrc script] [vimrc] you have to
restart Vim for the changes to take effect.

###The `g:predictive#disable_plugin` option

Turns off/on the plugin at statup.
Default = 0 (enabled)

    let g:predictive#disable_plugin = 1


###The `g.predictive#dict_path` option

Specify the path file for the dictionary.
Default = {bundle_path}/vim-predictive/dict_sample/en_US

    let g:predictive#dict_path = expand($HOME . '/dict')

View {dict_sample} directory for saples.

###The `g:predictive#file_types` option

Specify file types that uses the plugin
Default = 'text'

    let g:predictive#file_types = { 'vim' : [],
            \ 'text': [],
            \ 'python' : []
            \}

NOTE:
--------------
This is a experimental version. Pull requests welcome!
