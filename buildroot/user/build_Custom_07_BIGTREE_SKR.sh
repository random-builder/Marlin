#!/usr/bin/env bash

#
# printer definition
#

# printer hardware
environment="LPC1768"

# hardware variation
define_keys="USER_Custom_07_BIGTREE_SKR"

this_dir=$(cd $(dirname $0) && pwd)

source $this_dir/build_Any.sh

platformio_build
