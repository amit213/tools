#!/bin/sh

#check if this link already exists.
ln -s -f ~/tools/env/myshellrc.rc ~/.myshellrc.rc
ln -s -f ~/tools/env/for-vim/vimrc.rc ~/.vimrc

echo source ~/.myshellrc.rc >> ~/.bashrc
echo source ~/.myshellrc.rc >> ~/.shrc
echo source ~/.myshellrc.rc >> ~/.cshrc

