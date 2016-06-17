execute pathogen#infect()

set expandtab
set shiftwidth=4
set softtabstop=4
set autoindent

set number
autocmd BufNewFile,BufRead * set relativenumber

set background=dark

set showcmd

map D :syntax on<ENTER>
map S s<SPACE>
map M lxi<ENTER>
map Q Oimport pdb; pdb.set_trace()<Esc>
map  o

map - /^\(class\\|def\)<ENTER>zt
map _ ?^\(class\\|def\)<ENTER>zt

let mapleader="\<Space>"

"Move quicker between windows
map <Leader>h <c-w>h
map <Leader>l <c-w>l
map <Leader>j <c-w>j
map <Leader>k <c-w>k

"python magic
map <Leader>gc o^iclass ():	passk^f(i
map <Leader>gm o^i	def (self):	passk^f(i
map <Leader>gp O@property?property 

"Move quicker between tabs
map <Leader>u :tabprevious<ENTER>
map <Leader>o :tabnext<ENTER>

"Save quicker
map <Leader>d :w<ENTER>

"Quit the insert mode quicker
imap jj <Esc>

"open this file in vim
tabedit ~/.vimrc
tabprevious

"highlight the 80th line in black and wrap text before it
autocmd BufNewFile,BufRead *.py set colorcolumn=80
autocmd BufNewFile,BufRead *.py hi ColorColumn ctermbg=white

"fold on indent for a python file
set fdm=indent

"syntax highlighting
syntax on

"highlight word under cursor
autocmd CursorMoved * exe printf('match IncSearch /\V\<%s\>/', escape(expand('<cword>'), '/\'))

"vim-gitgutter configuration
set updatetime=250

"vim-flake8
let g:flake8_show_in_gutter=1
let g:flake8_show_in_file=1
autocmd BufWritePost *.py call Flake8()
