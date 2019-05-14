#!/usr/bin/env python

#
# setup scons build
#

# https://github.com/SCons/scons/blob/master/src/engine/SCons/Environment.py

import os
import subprocess

import SCons

from SCons.Script import Import
from SCons.Script import AlwaysBuild

Import("env")


def shell(cmd, check=False):
    result = subprocess.run(cmd, shell=True, capture_output=True)
    if check:
        assert result.returncode == 0
    return result


def report_args(*args, **kwargs):
    for entry in args:
        print(f"{entry}")
    for key, value in sorted(kwargs.items()):
        print(f"{key}={value}")


def report_env_var():
    for key, value in sorted(os.environ.items()):
        print(f"{key}={value}")


def report_dir_list(root):
        for path in sorted(os.listdir(root)):
            print(path)


def disk_find(label="MKS-BASE") -> str:
    result = shell(f"sudo lsblk -n -l -o name,label | grep {label} | head -n 1")
    if result.returncode == 0:
        stdout = result.stdout
        stdparts = stdout.split()
        if len(stdparts) == 2:
            disk_name = stdparts[0].decode('utf-8')
            return disk_name
        else:
            return None
    else:
        return None


def disk_has_point(disk_point):
    result = shell(f"mountpoint -q {disk_point}")
    return result.returncode == 0


def disk_point_mount(disk_point, disk_path):
    if disk_has_point(disk_point) is False:
        shell(f"sudo mount {disk_path} {disk_point} -o uid=$USER,gid=$USER", check=True)


def disk_point_unmount(disk_point):
    if disk_has_point(disk_point) is True:
        shell(f"sudo umount {disk_point}", check=True)


def disk_setup(disk_name, firmware):
    if disk_name is None:
        return
    disk_path = f"/dev/{disk_name}"
    disk_point = f"/tmp/pio-setup/{disk_name}"
    shell(f"mkdir -p {disk_point}", check=True)
    disk_point_unmount(disk_point)
    disk_point_mount(disk_point, disk_path)
    shell(f"cp {firmware} {disk_point}", check=True)
    disk_point_unmount(disk_point)
    shell(f"rm -rf {disk_point}", check=True)


def setup_invoke(
        env,
        source:SCons.Node.FS.File,
        target:SCons.Node.Alias.Alias):
    firmware = source[0].abspath
    print(f"### firmware={firmware}")
    disk_name = disk_find()
    print(f"### disk_name={disk_name}")
    disk_setup(disk_name, firmware)


print('====================================')
print('extra_script')
print('------------------------------------')

setup_target = env.Alias("setup", "$BUILD_DIR/firmware.bin", setup_invoke)
env.AlwaysBuild(setup_target)

print('====================================')
