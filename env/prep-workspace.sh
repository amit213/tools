#!/bin/sh
#!/bin/bash
#ss

#### this is prep work 

sudo apt-get install git -y
git clone https://github.com/amit213/tools.git
git clone https://amit213@bitbucket.org/amit213/mytools.git

ln -s -f ./tools/env/myshellrc.rc ~/.myshellrc.rc
echo "source ~/.myshellrc.rc" >> ~/.bashrc
source ~/.bashrc


