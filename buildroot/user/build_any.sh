#!/usr/bin/env bash

#
# shared build functions
#

set -e -u

# script location
here_dir=$(cd $(dirname $0) && pwd)
root_dir=$(cd $here_dir/../.. && pwd)

# convert KEY to -DKEY 
function parse_define() {
	local define_keys="$1"
	local define_list=($define_keys)
	local option_list=("${define_list[@]/#/-D}")
	echo "${option_list[@]}"
}

# invoke platformio
function platformio_build() {
	
	echo "### environment=$environment"
	echo "### define_keys=$define_keys"
	
	local option_list=$(parse_define $define_keys)

	cd $root_dir
	export PLATFORMIO_BUILD_FLAGS="$option_list"
	platformio run --environment $environment --project-dir $root_dir
	
}
