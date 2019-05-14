#!/usr/bin/env python

#
# setup scons build
#

import os

from SCons.Script import Import
from SCons.Script import AlwaysBuild

Import("env")


def report_env_var():
    for key, value in sorted(os.environ.items()):
        print(f"{key}={value}")


def report_dir_list(root):
        for path in sorted(os.listdir(root)):
            print(path)

# def upload_pre(source, target, env):
#     print("upload_pre")

# def upload_post(source, target, env):
#     print ("upload_post")


print('====================================')
print('extra_script')
print('------------------------------------')

build_dir = os.environ['PLATFORMIO_BUILD_DIR']
environment = os.environ['PLATFORMIO_ENVIRONMENT']
output_dir = os.path.join(build_dir, environment)
firmware_path = os.path.join(output_dir, 'firmware.bin')

print(f'build_dir={build_dir}')
print(f'output_dir={output_dir}')

# env.AddPreAction("upload", upload_pre)
# env.AddPostAction("upload", upload_post)

# report_dir_list(output_dir)

# report_env_var()

# assert os.path.isfile(firmware_path), 'missing firmware'

target_setup = env.Alias("setup", "$BUILD_DIR/firmware.bin", ["ls -las"])
env.AlwaysBuild(target_setup)

print('====================================')
