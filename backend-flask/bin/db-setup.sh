#! /usr/bin/bash
-e # stop if it fails at any point

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-setup"
printf "${CYAN}==== ${LABEL}${NO_COLOR}\n"

bin_path="$(realpath .)/bin"

source "$bin_path/db-drop.sh"
source "$bin_path/db-create.sh"
source "$bin_path/db-schema-load.sh"
source "$bin_path/db-seed.sh"
