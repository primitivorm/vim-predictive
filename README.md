vim-predictive
--------------
Given the first few letters of a word, for instance, it’s not too difficult to predict what should come next.

Like android phone text completion:
![primitivorm android](https://raw.githubusercontent.com/primitivorm/vim-predictive/master/dict_sample/predictive_android.jpg "predictive android")

With vim-predictive plugin:
![predictive vim](https://raw.githubusercontent.com/primitivorm/vim-predictive/master/dict_sample/predictive_vim.png "predictive vim")


install
--------------
1. this plugin requires numpy, install with pip:

`$pip install numpy`

2. add to Bundle list or install with pathogen:

`Plugin 'primitivorm/vim-predictive'`

options
--------------

These options can be configured in your
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
Default = ''

    let g:predictive#dict_path = expand($HOME . '/dict')

View {dict_sample} directory for samples. The file must be file read/write
permissions

NOTE:
--------------
Pull requests welcome!
