set expandtab
set shiftwidth=2
set softtabstop=2
set autoindent

set relativenumber
set number

set background=dark

set showcmd

map D :syntax on<ENTER>
map S s<SPACE>
map M lxi<ENTER>

let mapleader="\<Space>"

"Move quicker between tabs
map <Leader>h <c-w>h
map <Leader>l <c-w>l
map <Leader>j <c-w>j
map <Leader>k <c-w>k

"Save quicker
map <Leader>w :w<ENTER>

"Quit the insert mode quicker
imap jj <Esc>

tabedit ~/.vimrc
tabprevious
