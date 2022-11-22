#!/bin/bash -eu


function install_telegram_utils() {
	mkdir -p /home/vmuser/scratch/tools-utils/telegram.sh;
	git clone https://github.com/fabianonline/telegram.sh.git /home/vmuser/scratch/tools-utils/telegram.sh;
	sudo ln -s -f /home/vmuser/scratch/tools-utils/telegram.sh/telegram /usr/local/bin/telegram
	sudo ln -s -f /home/vmuser/scratch/tools-utils/telegram.sh/test.sh /usr/local/bin/test.sh
}

function install_system_apps() {
	sudo apt install -y ncdu; 

}


function install_google_chrome_browser() {
	sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb;
	sudo apt install ./google-chrome-stable_current_amd64.deb -y;
    sudo apt -f install -y;	
}

function install_chromium_app() {
	sudo apt install software-properties-common -y; 
	sudo add-apt-repository ppa:phd/chromium-browser -y; 
	sudo apt update -y; sudo add-apt-repository ppa:system76/pop -y; 
	sudo apt-get update -y; sudo apt install chromium -y;
}

function install_nodejs() {
	sudo apt install nodejs -y;
	sudo apt install npm -y;
}

function install_cronicle_app() {
	#sudo curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
	#source ~/.bashrc
	#nvm install v18.12.1
	curl -s https://raw.githubusercontent.com/jhuckaby/Cronicle/master/bin/install.js | node
}


function add_general_apps() {
	#touch /tmp/rambozebra321.txt;
	#echo "howdy zebra 321" >> /tmp/rambozebra321.txt;
	install_telegram_utils
	install_system_apps
	install_chromium_app
	install_nodejs
	install_cronicle_app
}


function entrypoint_add_prep_apps_to_ubuntu_tails_container() {
	add_general_apps

}


entrypoint_add_prep_apps_to_ubuntu_tails_container
