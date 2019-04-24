#!/usr/bin/env bash

#
# shared build functions
#

set -e -u

# script location
this_dir=$(cd $(dirname $0) && pwd)
root_dir=$(cd $this_dir/../.. && pwd)

# convert KEY to -DKEY 
function define_to_option() {
	local define_keys="$1"
	local define_list=($define_keys)
	local option_list=("${define_list[@]/#/-D}")
	echo "${option_list[@]}"
}

# invoke platformio
function platformio_build() {
	
	echo "### environment=$environment"
	echo "### define_keys=$define_keys"
	
	local define_list=($define_keys)
	local option_list=$(define_to_option $define_keys)
	local printer_name="${define_list[0]}"

	# work around #13801 - TODO
	#export PLATFORMIO_EXTRA_SCRIPTS="/bin/true"
	
	# activate configuration override
	export PLATFORMIO_BUILD_FLAGS="$option_list"
	echo "### build_flags=$PLATFORMIO_BUILD_FLAGS"
	
	# use per-printer build location
	export PLATFORMIO_BUILD_DIR="$root_dir/.pioenvs/$printer_name"
	echo "### build_dir=$PLATFORMIO_BUILD_DIR"
	
	cd $root_dir
	platformio run --environment $environment --project-dir $root_dir
	
}
