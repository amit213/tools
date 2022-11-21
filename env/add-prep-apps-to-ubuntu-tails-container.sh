#!/bin/bash -eu


function install_telegram_utils() {
	mkdir -p /home/vmuser/scratch/tools-utils/telegram.sh;
	git clone https://github.com/fabianonline/telegram.sh.git /home/vmuser/scratch/tools-utils/telegram.sh;
	sudo ln -s -f /home/vmuser/scratch/tools-utils/telegram.sh/telegram /usr/local/bin/telegram
	sudo ln -s -f /home/vmuser/scratch/tools-utils/telegram.sh/test.sh /usr/local/bin/test.sh
}


function add_general_apps() {
	#touch /tmp/rambozebra321.txt;
	#echo "howdy zebra 321" >> /tmp/rambozebra321.txt;
	install_telegram_utils
}


function entrypoint_add_prep_apps_to_ubuntu_tails_container() {
	add_general_apps

}


entrypoint_add_prep_apps_to_ubuntu_tails_container
