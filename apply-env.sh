#!/bin/sh
#

#global vars
shellrcfile=.myshellrc.rc
vimrcfile=.vimrc

# detect if already installed.
#
   is_debug_mode_on() {
     #turn ON / off debug mode
     return 0
   }
   dbg_print() {
     is_debug_mode_on
     dbg=$?
     [ $dbg -eq 1 ] && $@
   }
   # check if file exists
   is_file_present() {
     flag=0
     dbg_print echo "checking if file: $1 exists."
     if [  -L $1 ] 
     then
        dbg_print echo "$1 is a link and was found."
        flag=1
     elif [ -f $1 ]
     then
        dbg_print echo "$1 is a file and was found."
        flag=1
     elif [ -s $1 ]; then
        dbg_print echo "file $1 found."
     fi
     return $flag 
   }

   # Install on this host.
   apply_env() {
     is_file_present ~/$shellrcfile
     already_installed=$?
     #if [[ $already_installed == 1 ]] 
     if [ $already_installed -eq 1 ] 
     then
      echo "Previous installation detected. Links updated."
      #create_symlinks
     else
      create_symlinks
      insert_into_login_rc
      echo "Env config applied. Enjoy."
     fi    
   }

   create_symlinks() {
     ln -s -f ~/tools/env/myshellrc.rc ~/.myshellrc.rc
     ln -s -f ~/tools/env/for-vim/vimrc.rc ~/.vimrc    
   }

   #should be done only if its is a FRESH install.
   insert_into_login_rc() {
     echo source ~/.myshellrc.rc >> ~/.bashrc
     echo source ~/.myshellrc.rc >> ~/.shrc
     echo source ~/.myshellrc.rc >> ~/.cshrc    
   }

apply_env


