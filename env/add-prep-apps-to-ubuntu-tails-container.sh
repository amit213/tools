#!/bin/bash -eu


function add_general_apps() {
	touch /tmp/rambozebra321.txt;
	echo "howdy zebra 321" >> /tmp/rambozebra321.txt;
}


function entrypoint_add_prep_apps_to_ubuntu_tails_container() {
	add_general_apps

}


entrypoint_add_prep_apps_to_ubuntu_tails_container
